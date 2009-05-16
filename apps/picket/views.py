"""
Copyright 2008-2009 Serge Matveenko

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
"""
@todo: write test cases for permissions
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import (HttpResponseRedirect, HttpResponseNotFound,
                         HttpResponseForbidden, Http404)
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic.simple import direct_to_template

import custom
from alerts import send_alerts
from filters import BugFilter
from forms import (BugForm, BugUpdateForm, BugnoteForm, BugFileForm,
                   AssignForm, StatusForm, BugRelationshipForm, ReminderForm)
from models import (Bug, Project, Category, Scope, BugRelationship, BugHistory,
                    BugMonitor, Bugnote)
from permissions import permited_project_required, permited_bug_required
from settings import *


@login_required
def index(request):
    
    return direct_to_template(request, 'picket/index.html', {})
    
@permited_project_required(required_rights='r')
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
    
    bugFilter = BugFilter(request.GET, queryset=bugs, user=request.user)
    
    sticky_bugs = bugFilter.qs.filter(sticky=True)
    bugs = bugFilter.qs.filter(sticky=False)
    
    return direct_to_template(request, 'picket/bugs.html',
        {'bugs': bugs, 'sticky_bugs': sticky_bugs, 'project': project,
            'category': category, 'bug_filter': bugFilter,
            'sort_field': sort_field, 'sort_dir': sort_dir,})

@permited_project_required(required_rights='w')
def filebug(request, clone=False, clone_id=None):
    """
    @todo: handle relationship with parent in case of cloning
    """
    view_name = not clone and 'picket-filebug' or 'picket-filebug-clone'
    
    if clone:
        cloningBug = get_object_or_404(Bug, id=clone_id)
    
    if not 'project_id' in request.session:
        if clone:
            request.session['project_id'] = cloningBug.project_id
        else:
            return HttpResponseRedirect(
                reverse('picket-choose-project-gonext',
                    kwargs={'view_name': view_name,}))
    
    scopes = Scope.objects.get_permited(request.user)
    
    if request.method == 'POST':
        bugForm = BugForm(request.POST)
        bugFileForm = BugFileForm(request.POST, request.FILES,
            prefix='bugfile')
        if clone:
            bugRelationshipForm = BugRelationshipForm(request.POST)
        if bugForm.is_valid():
            bug = bugForm.save(commit=False)
            bug.reporter = request.user
            bug.save()
            request.user.message_set.create(message=_('bug filed'))
            if bugFileForm.is_valid():
                bugFile = bugFileForm.save(commit=False)
                bugFile.bug = bug
                bugFile.save()
                request.user.message_set.create(
                    message=_('file for bug uploaded'))
            if bugRelationshipForm.is_valid():
                bugRelationship = bugRelationshipForm.save(commit=False)
                bugRelationship.source_bug = bug
                bugRelationship.save()
                request.user.message_set.create(
                    message=_('relationship added'))
            return HttpResponseRedirect(bug.get_absolute_url())
    else:
        if clone:
            bugForm = BugForm(instance=cloningBug)
            bugRelationshipForm = BugRelationshipForm(
                initial={'bugrelationship_type':
                    BUGRELATIONSHIP_TYPE_DEFAULT,})
        else:
            bugForm = BugForm()
        bugFileForm = BugFileForm(prefix='bugfile')
    
    return direct_to_template(request, 'picket/bug_form.html',
        {'bug_form': bugForm, 'bugfile_form': bugFileForm, 'scopes': scopes,
            'is_clone': clone, 'cloning_bug': cloningBug,
            'bug_relationship_form': bugRelationshipForm,})

@permited_bug_required(required_rights='r')
def bug(request, bug):
    """
    View bug by its id
    """
    
    bugnoteForm = BugnoteForm()
    assignForm = AssignForm(instance=bug)
    statusForm = StatusForm(instance=bug)
    
    bugFileForm = BugFileForm()
    
    bugmonitor_users = User.objects.filter(bugmonitor__bug=bug,
        bugmonitor__mute=False)
    is_bugmonitor_user = request.user in bugmonitor_users
    
    bugRelationshipForm = BugRelationshipForm()
    bugRelationships = BugRelationship.objects.select_related().filter(
        source_bug=bug)
    
    bugHistoryItems = BugHistory.objects.filter(bug=bug)
    
    return direct_to_template(request, 'picket/bug.html',
        {'bug': bug, 'bugnote_form': bugnoteForm, 'assign_form': assignForm,
            'status_form': statusForm, 'bugmonitor_users': bugmonitor_users,
            'is_bugmonitor_user': is_bugmonitor_user,
            'bug_relationship_form': bugRelationshipForm,
            'bug_relationships': bugRelationships,
            'bug_file_form': bugFileForm,
            'bug_history_items': bugHistoryItems,})

@permited_bug_required(required_rights='w')
def update(request, bug):
    
    if request.method == 'POST':
        bugUpdateForm = BugUpdateForm(instance=bug, data=request.POST)
        bugnoteForm = BugnoteForm(prefix='note', data=request.POST)
        if bugUpdateForm.is_valid():
            bug = bugUpdateForm.save(commit=True)
            request.user.message_set.create(
                message=_('bug #%(bug_id)s updated' % {'bug_id': bug.id,}))
            if bugnoteForm.is_valid():
                bugnote = bugnoteForm.save(commit=False)
                bugnote.bug, bugnote.reporter = bug, request.user
                bugnote.save()
                request.user.message_set.create(
                    message=_('bugnote #%(bugnote_id)s added' %
                        {'bugnote_id': bugnote.id,}))
            return HttpResponseRedirect(bug.get_absolute_url())

    else:
        bugUpdateForm = BugUpdateForm(instance=bug)
        bugnoteForm = BugnoteForm(prefix='note')
    
    return direct_to_template(request, 'picket/bug_update.html',
        {'bug': bug, 'bug_update_form': bugUpdateForm,
            'bugnote_form': bugnoteForm,})

@permited_bug_required(required_rights='w')
def update_field(request, bug, form_class):
    
    Form = __import__('apps.picket.forms', globals(), locals(),
        fromlist=[form_class,]).__getattribute__(form_class)
    
    if request.method == 'POST':
        form = Form(instance=bug, data=request.POST)
        if form.is_valid():
            bug = form.save(commit=True)
            request.user.message_set.create(message=form._message)
        return HttpResponseRedirect(bug.get_absolute_url())
    else:
        form = Form(instance=bug)
    
    return direct_to_template(request, 'picket/bug_update_field.html',
        {'field_form': form,})

@permited_bug_required(required_rights='r')
def update_monitor(request, bug, mute):
    
    if request.method == 'POST':
        bugMonitor, created = BugMonitor.objects.get_or_create(
            user=request.user, bug=bug)
        bugMonitor.mute = mute
        bugMonitor.save()
        request.user.message_set.create(message=_('Bug monitoring updated'))
        return HttpResponseRedirect(bug.get_absolute_url())
    else:
        raise Http404

@permited_bug_required(required_rights='w')
def add_relationship(request, bug):
        
    if request.method == 'POST':
        bugRelationshipForm = BugRelationshipForm(request.POST)
        if bugRelationshipForm.is_valid():
            bugRelationships = BugRelationship.objects.filter(
                source_bug=bug,
                destination_bug=bugRelationshipForm.cleaned_data[
                    'destination_bug'])
            if bugRelationships.count() > 0:
                bugRelationship = bugRelationships[0]
                bugRelationship.relationship_type = \
                    bugRelationshipForm.cleaned_data['relationship_type']
                bugRelationship.save()
                request.user.message_set.create(
                    message=_('Bug relationship updated'))
            else:
                bugRelationship = bugRelationshipForm.save(commit=False)
                bugRelationship.source_bug = bug
                bugRelationship.save()
                request.user.message_set.create(
                    message=_('Bug relationship added'))            
        else:
            request.user.message_set.create(
                message=_('Error: bug relationship not changed!'))
    
    return HttpResponseRedirect(bug.get_absolute_url())

@permited_bug_required(required_rights='w')
def bug_file_upload(request, bug):
    
    if request.method == 'POST':
        bugFileForm = BugFileForm(request.POST, request.FILES)
        if bugFileForm.is_valid():
            bugFile = bugFileForm.save(commit=False)
            bugFile.bug = bug
            bugFile.save()
            request.user.message_set.create(message=_('File uploaded'))
            return HttpResponseRedirect(bug.get_absolute_url())
    else:
        bugFileForm = BugFileForm()
    
    return direct_to_template(request, 'picket/bug_file_form.html',
        {'bug': bug, 'bug_file_form': bugFileForm,})

@permited_bug_required(required_rights='r')
def remind(request, bug):
    
    if request.method == 'POST':
        reminderForm = ReminderForm(request.POST, user=request.user)
        if reminderForm.is_valid():
            reminder_text = reminderForm.cleaned_data['text']
            reminder_recipients = reminderForm.cleaned_data['recipients']
            """ save note """
            bugnote = Bugnote(bug=bug, reporter=request.user,
                text='Reminder to %s: %s' %
                    (', '.join(map(str, reminder_recipients)), reminder_text),
                scope=reminderForm.cleaned_data['scope'])
            bugnote.save()
            """ send reminder """
            send_alerts(bug, reminder_recipients, reminder_text)
            request.user.message_set.create(message=_('Reminder(s) sent'))
            return HttpResponseRedirect(bug.get_absolute_url())
    else:
        reminderForm = ReminderForm(user=request.user)
    
    return direct_to_template(request, 'picket/reminder.html',
        {'bug': bug, 'reminder_form': reminderForm,})

@permited_bug_required(required_rights='r')
def annotate(request, bug):
    """
    @todo: handle bugnotes access rights
    """
    
    if request.method == 'POST':
        bugnoteForm = BugnoteForm(request.POST)
        if bugnoteForm.is_valid():
            bugnote = bugnoteForm.save(commit=False)
            bugnote.bug, bugnote.reporter = bug, request.user
            bugnote.save()
            request.user.message_set.create(message=_('Bugnote filed'))
            return HttpResponseRedirect(bugnote.get_absolute_url())
        else:
            return direct_to_template(request, 'picket/bugnote_form.html',
                {'bugnote_form': bugnoteForm, 'bug': bug,})
    else:
        return HttpResponseRedirect(bug.get_absolute_url())

@permited_bug_required(required_rights='d')
def delete(request, bug):
    """
    Delete bug by its id
    """
    
    bug.delete()
    
    request.user.message_set.create(message=_('Bug deleted'))
    
    return HttpResponseRedirect(reverse('picket-bugs'))

@permited_bug_required(required_rights='w')
def delete_relationship(request, bug_relationship_id):
    
    bugRelationship = get_object_or_404(BugRelationship,
        id=bug_relationship_id)
    
    bug = bugRelationship.source_bug
    
    bugRelationship.delete()
    
    request.user.message_set.create(message=_('Relationship deleted'))
    
    return HttpResponseRedirect(bug.get_absolute_url())

@permited_project_required(required_rights='r')
def project(request, project_id):
    return HttpResponseRedirect(reverse('picket-admin-project',
        args=(project_id,)))

@login_required
def choose_project(request, view_name='picket-bugs'):
    """
    form for choosing project 
    """
    return direct_to_template(request, 'picket/choose_project.html',
        {'view_name': view_name,})

@login_required
def set_project(request, view_name='picket-bugs'):
    """
    writing project to session for other views could use it from there 
    """
    
    projectId = request.GET.get('project_id', None) or None
    
    if projectId is not None:
        project = get_object_or_404(Project, id=projectId)
        if project.is_permited(request.user):
            request.session['project_id'] = project.id
        else:
            return HttpResponseForbidden()
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
@todo: make picket style interface for my view
@todo: make gnustyle changelog view from bug at some status from config
@todo: make roadmap view with mantis like functionality
"""
roadmap = changelog = my = dummy
