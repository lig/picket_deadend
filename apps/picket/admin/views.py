"""
Copyright 2010 Serge Matveenko

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

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from ..decorators import render_to
from ..documents import Project, Scope
from ..forms import ProjectForm, ScopeForm

from decorators import superuser_required


@superuser_required
@render_to('picket/admin/index.html')
def index(request):
    return {}


@superuser_required
@render_to('picket/admin/projects.html')
def projects(request):
    
    projects = Project.sort
    
    return {'projects': projects}


@superuser_required
@render_to('picket/admin/new_project.html')
def new_project(request):
    
    if request.method == 'POST':
        projectForm = ProjectForm(request.POST)
        if projectForm.is_valid():
            project = Project(
                status=projectForm.cleaned_data['status'],
                name=projectForm.cleaned_data['name'],
                # @todo: handle project parent
                enabled=projectForm.cleaned_data['enabled'],
                # @todo: handle project scope
                # @todo: handle project categories
                description=projectForm.cleaned_data['description']
            )
            if projectForm.cleaned_data['url']:
                project.url = projectForm.cleaned_data['url']
            project.save()
            messages.success(request, _('Project created.'))
            return redirect('picket-admin-projects')
    else:
        projectForm = ProjectForm()

    return {'project_form': projectForm}


@superuser_required
@render_to('picket/admin/project.html')
def project(request, project_id):
    
    project = Project.get_enabled.get(id=project_id)
    
    return {'project': project}


@superuser_required
@render_to('picket/admin/edit_project.html')
def edit_project(request, project_id):
    """
    @todo: edit project page
    """
    project = Project.get_enabled.get(id=project_id)
    
    return {'project': project}


@superuser_required
@render_to('picket/admin/delete_project.html')
def delete_project(request, project_id):
    """
    @todo: delete project page
    """
    project = Project.get_enabled.get(id=project_id)
    
    return {'project': project}


@superuser_required
@render_to('picket/admin/scopes.html')
def scopes(request):
    
    scopes = Scope.sort
    
    return {'scopes': scopes}


@superuser_required
@render_to('picket/admin/new_scope.html')
def new_scope(request):
    
    if request.method == 'POST':
        scopeForm = ScopeForm(request.POST)
        if scopeForm.is_valid():
            scope = Scope(
                name=scopeForm.cleaned_data['name'],
                # @todo: handle scope read_access
                # @todo: handle scope write_access
                anonymous_access=scopeForm.cleaned_data['anonymous_access'],
            )
            scope.save()
            messages.success(request, _('Scope created.'))
            return redirect('picket-admin-scopes')
    else:
        scopeForm = ScopeForm()

    return {'scope_form': scopeForm}


@superuser_required
@render_to('picket/admin/scope.html')
def scope(request, scope_id):
    
    scope = Scope.objects.get(id=scope_id)
    
    return {'scope': scope}


@superuser_required
@render_to('picket/admin/edit_scope.html')
def edit_scope(request, scope_id):
    """
    @todo: edit scope page
    """
    scope = Scope.objects.get(id=scope_id)
    
    return {'scope': scope}


@superuser_required
@render_to('picket/admin/delete_scope.html')
def delete_scope(request, scope_id):
    """
    @todo: delete scope page
    """
    scope = Scope.get_enabled.get(id=scope_id)
    
    return {'scope': scope}
