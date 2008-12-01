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

from django.contrib.auth.decorators import user_passes_test
from django.http                    import HttpResponseRedirect
from django.shortcuts               import render_to_response, get_object_or_404 
from django.template                import RequestContext
from django.utils.translation       import ugettext as _

from picketapp.forms    import ProjectForm
from picketapp.models   import Project

is_su = lambda user: user.is_superuser

@user_passes_test(is_su)
def index(req):
    return render_to_response('picket/admin/index.html', {},
        context_instance=RequestContext(req))

@user_passes_test(is_su)
def users(req):
    ## implement users administration interface
    return render_to_response('picket/admin/index.html', {},
        context_instance=RequestContext(req))

@user_passes_test(is_su)
def projects(req):
    
    projects = Project.objects.all()
    
    return render_to_response('picket/admin/projects.html',
        {'projects': projects,}, context_instance=RequestContext(req))

@user_passes_test(is_su)
def add_project(req):
    
    if req.method == 'POST':
        projectForm = ProjectForm(req.POST)
        if projectForm.is_valid():
            project = projectForm.save()
            req.user.message_set.create(message=_('Project created'))
            return HttpResponseRedirect(project.get_absolute_url())
    else:
        projectForm = ProjectForm()
    
    return render_to_response('picket/admin/project-form.html',
        {'project_form': projectForm,}, context_instance=RequestContext(req))

@user_passes_test(is_su)
def project(req, projectId):
    projectId = int(projectId)
    
    project = get_object_or_404(Project, pk=projectId)
    
    if req.method == 'POST':
        projectForm = ProjectForm(req.POST, instance=project)
        if projectForm.is_valid():
            project = projectForm.save()
            req.user.message_set.create(message=_('Project updated'))
            return HttpResponseRedirect(project.get_absolute_url())
    else:
        projectForm = ProjectForm(instance=project)
    
    return render_to_response('picket/admin/project-form.html',
        {'project_form': projectForm,}, context_instance=RequestContext(req))
