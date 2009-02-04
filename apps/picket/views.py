"""
Copyright 2008 Serge Matveenko

This file is part of Picket.

Picket is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Picket is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Picket.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from apps.picket import custom
from apps.picket.forms import (BugForm, BugnoteForm, BugFileForm, AssignForm,
                               StatusForm, BugRelationshipForm)
from apps.picket.models import (Bug, Project, Category, Scope, BugRelationship,
                                BugHistory)
from apps.picket.settings import *

@login_required
def index(request):
    
    return render_to_response('picket/index.html', {},
        context_instance=RequestContext(request))
    
@login_required
def bugs(request, category_id=None, sort_field=None, sort_dir=None):
    """
    @note: Add order_by_field_name method to custom.py module to order by
        custom column name
    """
        
    project_id = request.session.get('project_id', None)
    project = get_object_or_404(Project, id=project_id) \
        if project_id is not None else None
    
    category = get_object_or_404(Category, id=category_id) \
        if category_id is not None else None
    
    bugs = Bug.objects.permited(request.user, project, category)
    
    if sort_field is not None:
        if Bug.has_field(sort_field):
            bugs = bugs.order_by('%s%s' % ('-' if sort_dir=='DESC' else '',
                sort_field))
        elif Bug.has_custom_sorter(sort_field):
            bugs = custom.__getattribute__('order_by_%s' % sort_field)(bugs,
                sort_dir)
        else:
            raise Http404
    
    
    sticky_bugs = bugs.filter(sticky=True)
    bugs = bugs.filter(sticky=False)
    
    return render_to_response('picket/bugs.html',
        {'bugs': bugs, 'sticky_bugs': sticky_bugs,
            'project': project, 'category': category,},
        context_instance=RequestContext(request))

@login_required
def filebug(request):
    
    if not 'project_id' in request.session:
        return HttpResponseRedirect(reverse('picket-choose-project-gonext',
            kwargs={'view_name': 'picket-filebug',}))
    
    scopes = Scope.objects.permited(request.user)
    
    if request.method == 'POST':
        bugForm = BugForm(request.POST)
        bugFileForm = BugFileForm(request.POST, request.FILES, prefix='bugfile')
        if bugForm.is_valid():
            bug = bugForm.save(commit=False)
            bug.reporter = request.user
            bug.project_id = bug.category.project_id
            """ @todo: automate default bug.scope from project.scope via
            signals """ 
            if bug.scope is None:
                bug.scope = bug.project.scope
            bug.save()
            request.user.message_set.create(message=_('bug filed'))
            if bugFileForm.is_valid():
                bugFile = bugFileForm.save(commit=False)
                bugFile.bug = bug
                bugFile.save()
                request.user.message_set.create(message=_('file for bug uploaded'))
            return HttpResponseRedirect(bug.get_absolute_url())
    else:
        bugForm = BugForm()
        bugFileForm = BugFileForm(prefix='bugfile')
    
    return render_to_response('picket/bug_form.html',
        {'bug_form': bugForm, 'bugfile_form': bugFileForm, 'scopes': scopes,},
        context_instance=RequestContext(request))

@login_required
def bug(request, bug_id):
    """
    View bug by its id
    """
    
    bug = get_object_or_404(Bug, id=bug_id)
    
    bugnoteForm = BugnoteForm()
    assignForm = AssignForm(instance=bug)
    statusForm = StatusForm(instance=bug)
    
    bugFileForm = BugFileForm()
    
    bugmonitor_users = bug.monitor.filter(bugmonitor__mute=False)
    is_bugmonitor_user = request.user in bugmonitor_users
    
    bugRelationshipForm = BugRelationshipForm()
    bugRelationships = BugRelationship.objects.select_related().filter(
        source_bug=bug)
    
    bugHistoryItems = BugHistory.objects.filter(bug=bug)
    
    return render_to_response('picket/bug.html',
        {'bug': bug, 'bugnote_form': bugnoteForm, 'assign_form': assignForm,
            'status_form': statusForm, 'bugmonitor_users': bugmonitor_users,
            'is_bugmonitor_user': is_bugmonitor_user,
            'bug_relationship_form': bugRelationshipForm,
            'bug_relationships': bugRelationships,
            'bug_file_form': bugFileForm,
            'bug_history_items': bugHistoryItems,},
        context_instance=RequestContext(request))

@login_required
def annotate(request, bug_id):
    
    bug = get_object_or_404(Bug, id=bug_id)
    
    if request.method == 'POST':
        bugnoteForm = BugnoteForm(request.POST)
        if bugnoteForm.is_valid():
            bugnote = bugnoteForm.save(commit=False)
            bugnote.bug, bugnote.reporter = bug, request.user
            """ @todo: automate default bugnote.scope from bug.scope via
            signals """ 
            if bugnote.scope is None:
                bugnote.scope = bug.scope
            bugnote.save()
            request.user.message_set.create(message=_('bugnote filed'))
            return HttpResponseRedirect(bugnote.get_absolute_url())
        else:
            return render_to_response('picket/bugnote_form.html',
                {'bugnote_form': bugnoteForm, 'bug': bug,},
                context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(bug.get_absolute_url())

@login_required
def project(request, project_id):
    return HttpResponseRedirect(reverse('picket-admin-project',
        args=(project_id,)))

@login_required
def choose_project(request, view_name='picket-bugs'):
    """
    form for choosing project 
    """
    return render_to_response('picket/choose_project.html',
        {'view_name': view_name,}, context_instance=RequestContext(request))

@login_required
def set_project(request, view_name='picket-bugs'):
    """
    writing project to session for other views could use it from there 
    """
    
    projectId = request.GET.get('project_id', None) or None
    
    if projectId is not None:
        project = get_object_or_404(Project, id=projectId)
        request.session['project_id'] = project.id
        return HttpResponseRedirect(reverse(view_name))
    else:
        if request.session.has_key('project_id'):
            del request.session['project_id']
        return HttpResponseRedirect(reverse(view_name))

@login_required
def jump_to_bug(request):
    """
    redirecting to bug
    """

    bug_id = request.GET['bug_id']
    
    if not bug_id.isdigit(): return HttpResponseNotFound()
    
    bug = get_object_or_404(Bug, id=bug_id)
    
    return HttpResponseRedirect(bug.get_absolute_url())

@login_required
def dummy(request):
    """
    just redirecting to bugs view now
    """
    
    return HttpResponseRedirect(reverse('picket-bugs'))

"""
TODO: make picket style interface for my view
TODO: make gnustyle changelog view from bug at some status from config
TODO: make roadmap view with mantis like functionality
"""
roadmap = changelog = my = dummy
