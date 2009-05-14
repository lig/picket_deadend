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
from django.contrib.auth.forms import UserCreationForm, AdminPasswordChangeForm
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.generic.simple import direct_to_template

from ..forms import ProjectForm, CategoryForm, CategoryQuickForm
from ..models import Project, Category, Scope
from ..permissions import is_su
from ..settings import INTEGRATION_ENABLED

from forms import UserForm, GroupForm, ScopeForm, ScopegroupFormset

@user_passes_test(is_su)
def index(request):
    return redirect('picket-admin-users')

@user_passes_test(is_su)
def users(request):
    
    users = User.objects.all()
    groups = Group.objects.all()
    
    return direct_to_template(request, 'picket/admin/users.html',
        {'users': users, 'groups': groups,})

@user_passes_test(is_su)
def add_user(request):
    
    if INTEGRATION_ENABLED:
        return redirect('users-add')
    else:    
        if request.method == 'POST':
            userForm = UserCreationForm(request.POST)
            if userForm.is_valid():
                user = userForm.save()
                request.user.message_set.create(message=_('User created'))
                return redirect('picket-admin-user', userId=user.id)
        else:
            userForm = UserCreationForm()
        
        return direct_to_template(request, 'picket/admin/user_add.html',
            {'user_form': userForm, 'user': user,})

@user_passes_test(is_su)
def edit_user(request, userId):
    
    user = get_object_or_404(User, id=userId)
    
    if INTEGRATION_ENABLED:
        return redirect('user-edit', user=user.pk)
    else:
        if request.method == 'POST':
            userForm = UserForm(request.POST, instance=user)
            if userForm.is_valid():
                user = userForm.save()
                request.user.message_set.create(message=_('User updated'))
                return redirect('picket-admin-users')
        else:
            userForm = UserForm(instance=user)
        
        return direct_to_template(request, 'picket/admin/user_edit.html',
            {'user_form': userForm,})

@user_passes_test(is_su)
def add_group(request):
    
    if request.method == 'POST':
        groupForm = GroupForm(request.POST)
        if groupForm.is_valid():
            group = groupForm.save()
            request.user.message_set.create(message=_('Group created'))
            return redirect('picket-admin-users')
    else:
        groupForm = GroupForm()
    
    return direct_to_template(request, 'picket/admin/group_add.html',
        {'group_form': groupForm,})

@user_passes_test(is_su)
def edit_group(request, groupId):
    
    group = get_object_or_404(Group, id=groupId)
    
    if request.method == 'POST':
        groupForm = GroupForm(request.POST, instance=group)
        if groupForm.is_valid():
            group = groupForm.save()
            request.user.message_set.create(message=_('Group updated'))
            return redirect('picket-admin-users')
    else:
        groupForm = GroupForm(instance=group)
    
    return direct_to_template(request, 'picket/admin/group_edit.html',
        {'group_form': groupForm,})

@user_passes_test(is_su)
def change_user_password(request, userId):
    
    user = get_object_or_404(User, id=userId)
    
    if INTEGRATION_ENABLED:
        return redirect('user-password', user=user.pk)
    else:
        if request.method == 'POST':
            passwordForm = AdminPasswordChangeForm(user, request.POST)
            if passwordForm.is_valid():
                user = passwordForm.save()
                request.user.message_set.create(message=_('Password updated'))
                return redirect('picket-admin-users')
        else:
            passwordForm = AdminPasswordChangeForm(user=user)
        
        return direct_to_template(request, 'picket/admin/user_password.html',
            {'password_form': passwordForm,})

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
            return redirect(project.get_absolute_url())
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
            return redirect(project.get_absolute_url())
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
        return redirect('picket-admin-projects')
    else:
        return redirect(project.get_absolute_url())

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
    
    return redirect(project.get_absolute_url())

@user_passes_test(is_su)
def category(request, categoryId):
    
    category = get_object_or_404(Category, pk=categoryId)
    
    if request.method == 'POST':
        categoryForm = CategoryForm(request.POST, instance=category)
        if categoryForm.is_valid():
            category = categoryForm.save()
            request.user.message_set.create(message=_('Category updated'))
            return redirect(category.project.get_absolute_url())
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
    
    return redirect(project.get_absolute_url())

@user_passes_test(is_su)
def scopes(request):
    
    scopes = Scope.objects.all()
    groups = Group.objects.all()
    
    return direct_to_template(request, 'picket/admin/scopes.html',
        {'scopes': scopes, 'groups': groups,})

@user_passes_test(is_su)
def add_scope(request):
    
    if request.method == 'POST':
        scopeForm = ScopeForm(request.POST)
        if scopeForm.is_valid():
            scope = scopeForm.save()
            request.user.message_set.create(message=_('Scope created'))
            return redirect('picket-admin-scope', scopeId=scope.id)
    else:
        scopeForm = ScopeForm()
    
    return direct_to_template(request, 'picket/admin/scope_add.html',
        {'scope_form': scopeForm,})

@user_passes_test(is_su)
def scope(request, scopeId):
    
    scope = get_object_or_404(Scope, id=scopeId)
    
    if request.method == 'POST':
        scopeForm = ScopeForm(request.POST, instance=scope)
        scopegroupFormset = ScopegroupFormset(request.POST, instance=scope)
        if scopeForm.is_valid() and scopegroupFormset.is_valid():
            scope = scopeForm.save()
            scopegroups = scopegroupFormset.save()
            request.user.message_set.create(message=_('Scope updated'))
            return redirect('picket-admin-scopes')
    else:
        scopeForm = ScopeForm(instance=scope)
        scopegroupFormset = ScopegroupFormset(instance=scope)
    
    return direct_to_template(request, 'picket/admin/scope_edit.html',
        {'scope_form': scopeForm, 'scopegroup_formset': scopegroupFormset,})
