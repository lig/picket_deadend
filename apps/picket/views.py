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
from django.core.urlresolvers       import reverse
from django.http                    import HttpResponseRedirect
from django.shortcuts               import get_object_or_404, \
                                           render_to_response
from django.template                import RequestContext
from django.utils.translation       import ugettext as _

from apps.picket.forms import BugForm, BugnoteForm
from apps.picket.models import Bug, Project, Category

@login_required
def index(req):
    
    return render_to_response('picket/index.html', {},
        context_instance=RequestContext(req))
    
@login_required
def bugs(req, category_id=None, skip=0, limit=20):
    
    project_id = req.session.get('project_id', None)
    project = get_object_or_404(Project, id=project_id) \
        if project_id is not None else None

    category = get_object_or_404(Category, id=category_id) \
        if category_id is not None else None
    
    bugs = Bug.objects.permited(req.user, project, category)
    sticky_bugs = bugs.filter(sticky=True)
    bugs = bugs.filter(sticky=False)[skip:skip+limit]
    
    #bugs = [bug.column for column in Bug.Meta for bug in bugs]
    
    return render_to_response('picket/bugs.html',
        {'bugs': bugs, 'sticky_bugs': sticky_bugs, 'project': project,
            'category': category,},
        context_instance=RequestContext(req))

@login_required
def filebug(req):
    
    if req.method == 'POST':
        bugForm = BugForm(req.POST)
        if bugForm.is_valid():
            bug = bugForm.save(commit=False)
            bug.reporter = req.user
            bug.scope = bug.project.scope
            bug.save()
            req.user.message_set.create(message=_('bug filed'))
            return HttpResponseRedirect(bug.get_absolute_url())
    else:
        bugForm = BugForm()
    
    return render_to_response('picket/bug_form.html', {'bug_form': bugForm,},
        context_instance=RequestContext(req))

@login_required
def bug(req, project_id, category_id, bug_id):
    
    bug = get_object_or_404(Bug, id=bug_id)
    
    try:
        bug.check_place(project_id, category_id)
    except:
        return HttpResponseRedirect(bug.get_absolute_url())
    
    bugnoteForm = BugnoteForm()
    
    return render_to_response('picket/bug.html',
        {'bug': bug, 'bugnote_form': bugnoteForm,},
        context_instance=RequestContext(req))

@login_required
def annotate(req, bug_id):
    
    bug = get_object_or_404(Bug, id=bug_id)
    
    assert req.method == 'POST'
    
    bugnoteForm = BugnoteForm(req.POST)
    if bugnoteForm.is_valid():
        bugnote = bugnoteForm.save(commit=False)
        bugnote.bug, bugnote.reporter, bugnote.scope \
            = bug, req.user, bug.scope
        bugnote.save()
        req.user.message_set.create(message=_('bugnote filed'))
        return HttpResponseRedirect(bugnote.get_absolute_url())
    else:
        return render_to_response('picket/bugnote_form.html',
            {'bugnote_form': bugnoteForm, 'bug': bug,},
            context_instance=RequestContext(req))

@login_required
def project(req, project_id):
    return HttpResponseRedirect(reverse('picket-admin-project',
        args=(project_id,)))

@login_required
def set_project(req):
    """
    writing project to session for other views could use it from there 
    """
    
    projectId = req.GET.get('project_id', None)
    
    if projectId is not None:
        project = get_object_or_404(Project, id=projectId)
        req.session['project_id'] = project.id
        return HttpResponseRedirect(reverse('picket-bugs'))
    else:
        if req.session.has_key('project_id'):
            del req.session['project_id'] 
        return HttpResponseRedirect(reverse('picket-bugs'))

@login_required
def jump_to_bug(req):
    """
    redirecting to bug
    """
    
    bug = get_object_or_404(Bug, id=req.GET['bug_id'])
    
    return HttpResponseRedirect(bug.get_absolute_url())

@login_required
def dummy(req):
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
