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

from django.shortcuts   import render_to_response
from django.template    import RequestContext
from picketapp.models import Project

def index(req):
    return render_to_response('picket/admin/index.html', {},
        context_instance=RequestContext(req))

def users(req):
    ## implement users administration interface
    return render_to_response('picket/admin/index.html', {},
        context_instance=RequestContext(req))

def projects(req):
    
    projects = Project.objects.all()
    
    return render_to_response('picket/admin/projects.html',
        {'projects': projects,}, context_instance=RequestContext(req))

def add_project(req):
    
    return render_to_response('picket/admin/project-form.html', {},
        context_instance=RequestContext(req))
