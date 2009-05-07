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

from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404 
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.simple import direct_to_template

from ..forms import ProjectForm, CategoryForm, CategoryQuickForm
from ..models import Project, Category
from ..permissions import is_su


@user_passes_test(is_su)
def index(request):
    return direct_to_template(request, 'picket/admin/index.html', {})

@user_passes_test(is_su)
def users(request):
    """ @todo: implement users administration interface """
    return direct_to_template(request, 'picket/admin/index.html', {})

@user_passes_test(is_su)
def projects(request):
    
    projects = Project.objects.all()
    
    return direct_to_template(request, 'picket/admin/projects.html',
        {'projects': projects,})

@user_passes_test(is_su)
def add_project(request):
    
    if request.method == 'POST':
        projectForm = ProjectForm(request.POST)
        if projectForm.is_valid():
            project = projectForm.save()
            request.user.message_set.create(message=_('Project created'))
            return HttpResponseRedirect(project.get_absolute_url())
    else:
        projectForm = ProjectForm()
    
    return direct_to_template(request, 'picket/admin/project_add.html',
        {'project_form': projectForm,})

@user_passes_test(is_su)
def project(request, projectId):
    
    project = get_object_or_404(Project, pk=projectId)
    
    if request.method == 'POST':
        projectForm = ProjectForm(request.POST, instance=project)
        if projectForm.is_valid():
            project = projectForm.save()
            request.user.message_set.create(message=_('Project updated'))
            return HttpResponseRedirect(project.get_absolute_url())
    else:
        projectForm = ProjectForm(instance=project)
    
    categoryForm = CategoryQuickForm()
    
    return direct_to_template(request, 'picket/admin/project_manage.html',
        {'project_form': projectForm, 'project': project,
            'category_form': categoryForm,})

@user_passes_test(is_su)
def remove_project(request, projectId):
    
    project = get_object_or_404(Project, pk=projectId)
    
    if request.method == 'POST':
        project.delete()
        request.user.message_set.create(message=_('Project deleted'))
        return HttpResponseRedirect(reverse('picket-admin-projects'))
    else:
        return HttpResponseRedirect(project.get_absolute_url())

@user_passes_test(is_su)
def add_category(request, projectId):
    
    project = get_object_or_404(Project, pk=projectId)
    
    if request.method == 'POST':
        categoryForm = CategoryQuickForm(request.POST)
        if categoryForm.is_valid():
            category = categoryForm.save(commit=False)
            category.project = project
            category.save()
            request.user.message_set.create(message=_('Category added'))
    
    return HttpResponseRedirect(project.get_absolute_url())

@user_passes_test(is_su)
def category(request, categoryId):
    
    category = get_object_or_404(Category, pk=categoryId)
    
    if request.method == 'POST':
        categoryForm = CategoryForm(request.POST, instance=category)
        if categoryForm.is_valid():
            category = categoryForm.save()
            request.user.message_set.create(message=_('Category updated'))
            return HttpResponseRedirect(category.project.get_absolute_url())
    else:
        categoryForm = CategoryForm(instance=category)
    
    return direct_to_template(request, 'picket/admin/category_manage.html',
        {'category': category, 'category_form': categoryForm,})

@user_passes_test(is_su)
def remove_category(request, categoryId):
    
    category = get_object_or_404(Category, pk=categoryId)
    
    if request.method == 'POST':
        project = category.project
        category.delete()
        request.user.message_set.create(message=_('Category deleted'))
    
    return HttpResponseRedirect(project.get_absolute_url())
