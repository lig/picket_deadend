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
from django.shortcuts               import get_object_or_404, \
                                           render_to_response
from django.template                import RequestContext

from picketapp.models import Bug, Project, Category

@login_required
def index(req, projectId=None):
    
    project = get_object_or_404(Project, id=projectId) \
        if projectId is not None else None
    
    return render_to_response('picket/index.html', {},
        context_instance=RequestContext(req))
    
@login_required
def bugs(req, projectId=None):
    
    project = get_object_or_404(Project, id=projectId) \
        if projectId is not None else None

    bugs = Bug.objects.permited(req.user, project)
    
    return render_to_response('picket/bugs.html', {'bugs': bugs,},
        context_instance=RequestContext(req))

@login_required
def bug(req, bugId, projectId=None):
    
    project = get_object_or_404(Project, id=projectId) \
        if projectId is not None else None
    
    bug = get_object_or_404(Bug, id=bugId)
    
    return render_to_response('picket/bug.html', {'bug': bug,},
        context_instance=RequestContext(req))

@login_required
def category(req, categoryId, projectId=None):
    
    project = get_object_or_404(Project, id=projectId) \
        if projectId is not None else None
    
    category = get_object_or_404(Category, id=categoryId)
    
    return render_to_response('picket/category.html',
        {'category': category,},
        context_instance=RequestContext(req))
