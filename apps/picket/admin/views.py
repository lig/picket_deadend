"""
Copyright 2010-2011 Serge Matveenko

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

from copy import copy

from django.conf import settings
from django.contrib.messages import success, error
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.base import TemplateResponseMixin
from mongoengine.django.auth import User

from ..decorators import render_to
from ..documents import Project, Department, Employee

from decorators import role_required
from forms import (ProjectForm, DepartmentForm, EmployeeCreationForm,
    EmployeeChangeForm)


class RoleRequiredMixin(object):
    
    role_required = ''
    
    def dispatch(self, request, *args, **kwargs):
        
        def test():
            return bool(request.user.is_superuser or {
                'manager': request.my_projects and
                    kwargs.get('project_id') and
                    Project.objects.filter(pk=kwargs['project_id'] #@UndefinedVariable
                        ).first() in request.my_projects, #@UndefinedVariable
                'head': request.my_departments and
                    kwargs.get('department_id') and
                    Department.objects.filter(pk=kwargs['department_id'] #@UndefinedVariable
                        ).first() in request.my_departments, #@UndefinedVariable
            }.get(self.role_required))
        
        if test():
            return super(RoleRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            error(request, _('Permission denied'))
            return redirect(settings.LOGIN_URL)

    
class ProjectsView(RoleRequiredMixin, ListView):
    
    role_required = 'su'
    queryset = Project.objects
    template_name = 'picket/admin/projects.html'
    context_object_name = 'projects'


class ProjectView(RoleRequiredMixin, UpdateView):
    
    role_required = 'manager'
    queryset = Project.objects
    template_name = 'picket/admin/project.html'
    context_object_name = 'project'
    form_class = ProjectForm
    
    def get_object(self):
        project_id = self.kwargs.get('project_id', None)
        return project_id and Project.objects(id=project_id).first()
    
    def get_template_names(self):
        return TemplateResponseMixin.get_template_names(self)


class DepartmentsView(RoleRequiredMixin, ListView):
    
    role_required = 'su'
    queryset = Department.objects
    template_name = 'picket/admin/departments.html'
    context_object_name = 'departments'


class DepartmentView(RoleRequiredMixin, UpdateView):
    
    role_required = 'head'
    queryset = Department.objects
    template_name = 'picket/admin/department.html'
    context_object_name = 'department'
    form_class = DepartmentForm
    
    def get_object(self):
        department_id = self.kwargs.get('department_id', None)
        return department_id and Department.objects(id=department_id).first()
    
    def get_template_names(self):
        return TemplateResponseMixin.get_template_names(self)


@role_required('su')
@render_to('picket/admin/employees.html')
def employees(request):

    # list to avoid circular dereference
    employees = list(Employee.all().order_by('department'))

    departments = Department.objects
    
    return {'employees': employees, 'departments': departments}


@role_required('su')
@render_to('picket/admin/employee.html')
def new_employee(request):
    
    if request.method == 'POST':
        employee_form = EmployeeCreationForm(request.POST)
        
        if employee_form.is_valid():
            employee = employee_form.save()
            success(request, _('Employee created'))
            return redirect(employee.get_absolute_url())
        
    else:
        employee_form = EmployeeCreationForm()
    
    return {'employee_form': employee_form}


@role_required('su')
@render_to('picket/admin/employee.html')
def employee(request, employee_id):
    
    employee = Employee.objects(id=employee_id).first()
    if not employee:
        user = User.objects(id=employee_id).first()
        if user:
            employee = Employee.from_user(user)
        else:
            raise Http404
    
    if request.method == 'POST':
        employee_form = EmployeeChangeForm(request.POST, instance=employee)
        
        if employee_form.is_valid():
            employee = employee_form.save()
            success(request, _('Employee updated'))
            return redirect(employee.get_absolute_url())
        
    else:
        employee_form = EmployeeChangeForm(instance=employee)
    
    return {'employee': employee, 'employee_form': employee_form}


@role_required('su')
def employee_department(request, employee_id):
    
    # @todo: respect DRY with employee method
    employee = Employee.objects(id=employee_id).first()
    if not employee:
        user = User.objects(id=employee_id).first()
        if user:
            employee = Employee.from_user(user)
        else:
            raise Http404
    
    if request.method == 'POST' and 'department' in request.POST:
        department_id = request.POST['department']
        
        if department_id:
            department = Department.objects(id=department_id).first()
        else:
            department = None
        
        employee.department = department
        employee.save()
        success(request, _('Department for employee changed'))
        return redirect('picket-admin-employees')
    else:
        return HttpResponseBadRequest()
