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
from ..documents import Project
from ..forms import ProjectForm


@render_to('picket/admin/index.html')
def index(request):
    return {}


@render_to('picket/admin/projects.html')
def projects(request):
    
    projects = Project.sorted
    
    return {'projects': projects}


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

    return {'projects': True, 'project_form': projectForm}
