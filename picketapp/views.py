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

from picketapp.forms import BugForm, BugnoteForm
from picketapp.models import Bug, Project, Category

@login_required
def index(req):
    
    return render_to_response('picket/index.html', {},
        context_instance=RequestContext(req))
    
@login_required
def bugs(req, projectId=None, categoryId=None):
    
    project = get_object_or_404(Project, id=projectId) \
        if projectId is not None else None

    category = get_object_or_404(Category, id=categoryId) \
        if categoryId is not None else None

    bugs = Bug.objects.permited(req.user, project, category)
    
    return render_to_response('picket/bugs.html',
        {'bugs': bugs, 'project': project, 'category': category,},
        context_instance=RequestContext(req))

@login_required
def filebug(req):
    
    if req.method == 'POST':
        bugForm = BugForm(req.POST)
        if bugForm.is_valid():
            bug = bugForm.save(commit=False)
            bug.reporter = req.user
            bug.view_state = bug.project.view_state
            bug.save()
            req.user.message_set.create(message=_('bug filed'))
            return HttpResponseRedirect(bug.get_absolute_url())
    else:
        bugForm = BugForm()
    
    return render_to_response('picket/bug_form.html', {'bug_form': bugForm,},
        context_instance=RequestContext(req))

@login_required
def bug(req, projectId, categoryId, bugId):
    
    bug = get_object_or_404(Bug, id=bugId)
    
    try:
        bug.check_place(projectId, categoryId)
    except:
        return HttpResponseRedirect(bug.get_absolute_url())
    
    bugnoteForm = BugnoteForm()
    
    return render_to_response('picket/bug.html',
        {'bug': bug, 'bugnote_form': bugnoteForm,},
        context_instance=RequestContext(req))

@login_required
def annotate(req, bugId):
    
    bug = get_object_or_404(Bug, id=bugId)
    
    assert req.method == 'POST'
    
    bugnoteForm = BugnoteForm(req.POST)
    if bugnoteForm.is_valid():
        bugnote = bugnoteForm.save(commit=False)
        bugnote.bug, bugnote.reporter, bugnote.view_state \
            = bug, req.user, bug.view_state
        bugnote.save()
        req.user.message_set.create(message=_('bugnote filed'))
        return HttpResponseRedirect(bugnote.get_absolute_url())
    else:
        return render_to_response('picket/bugnote_form.html',
            {'bugnote_form': bugnoteForm, 'bug': bug,},
            context_instance=RequestContext(req))
