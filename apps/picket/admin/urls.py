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

from django.conf.urls.defaults import *

from views import *


urlpatterns = patterns('%s.views' % __package__,

    # Projects
    (r'^projects/$', ProjectsView.as_view(), {}, 'picket-admin-projects'),
    (r'^projects/new/$', ProjectView.as_view(), {},
        'picket-admin-project-new'),
    (r'^projects/(?P<project_id>\w+)/$', ProjectView.as_view(), {},
        'picket-admin-project'),
    
    # Departments
    (r'^departments/$', DepartmentsView.as_view(), {},
        'picket-admin-departments'),
    (r'^departments/new/$', DepartmentView.as_view(), {},
        'picket-admin-department-new'),
    (r'^departments/(?P<department_id>\w+)/$', DepartmentView.as_view(), {},
        'picket-admin-department'),
    
    # Stages
    (r'^stages/$', StagesView.as_view(), {},
        'picket-admin-stages'),
    (r'^stages/new/$', StageView.as_view(), {},
        'picket-admin-stage-new'),
    (r'^stages/(?P<stage_id>\w+)/$', StageView.as_view(), {},
        'picket-admin-stage'),
    
    # Employees
    (r'^employees/$', EmployeesView.as_view(), {}, 'picket-admin-employees'),
    (r'^employees/new/$', 'new_employee', {}, 'picket-admin-employee-new'),
    (r'^employees/(?P<employee_id>\w+)/$', 'employee', {},
        'picket-admin-employee'),
    (r'^employees/(?P<employee_id>\w+)/department/$', 'employee_department',
        {}, 'picket-admin-employee-department'),
)
