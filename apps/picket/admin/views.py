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
from ..documents import Project, Department
from ..forms import ProjectForm, DepartmentForm

from decorators import superuser_required


@superuser_required
@render_to('picket/admin/index.html')
def index(request):
    return {}


@superuser_required
@render_to('picket/admin/projects.html')
def projects(request):
    
    projects = Project.objects()
    
    return {'projects': projects}


@superuser_required
@render_to('picket/admin/project.html')
def project(request, project_id=None):
    
    project = project_id and Project.objects(id=project_id).first()
    
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        
        if project_form.is_valid():
            project = project_form.save()
            
            if project_id:
                messages.success(request, _('Project updated'))
            else:
                messages.success(request, _('Project created'))
            
            return redirect(project.get_absolute_url())
        
    else:
        project_form = ProjectForm(instance=project)
    
    return {'project': project, 'project_form': project_form}


@superuser_required
@render_to('picket/admin/departments.html')
def departments(request):
    
    departments = Department.objects()
    
    return {'departments': departments}


@superuser_required
@render_to('picket/admin/department.html')
def department(request, department_id=None):
    
    department = department_id and Department.objects(id=department_id).first()
    
    if request.method == 'POST':
        department_form = DepartmentForm(request.POST, instance=department)
        
        if department_form.is_valid():
            department = department_form.save()
            
            if department_id:
                messages.success(request, _('Department updated'))
            else:
                messages.success(request, _('Department created'))
            
            return redirect(department.get_absolute_url())
        
    else:
        department_form = DepartmentForm(instance=department)
    
    return {'department': department, 'department_form': department_form}
