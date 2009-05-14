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

from django.conf.urls.defaults  import *

urlpatterns = patterns('apps.picket.admin.views',
    (r'^$', 'index', {}, 'picket-admin',),
    (r'^users/$', 'users', {}, 'picket-admin-users',),
    (r'^users/add/$', 'add_user', {}, 'picket-admin-users-add',),
    (r'^user/(?P<userId>\d+)/edit/$', 'edit_user', {}, 'picket-admin-user',),
    (r'^user/(?P<userId>\d+)/password/$', 'change_user_password', {},
        'picket-admin-user-password',),
    (r'^groups/add/$', 'add_group', {}, 'picket-admin-groups-add',),
    (r'^group/(?P<groupId>\d+)/edit/$', 'edit_group', {}, 'picket-admin-group',),
    (r'^projects/$', 'projects', {}, 'picket-admin-projects',),
    (r'^projects/add/$', 'add_project', {}, 'picket-admin-projects-add',),
    (r'^project/(?P<projectId>\d+)/$', 'project', {}, 'picket-admin-project',),
    (r'^project/(?P<projectId>\d+)/delete/$', 'remove_project', {},
        'picket-admin-project-delete',),
    (r'^project/(?P<projectId>\d+)/category_add/$', 'add_category', {},
        'picket-admin-categories-add',),
    (r'^category/(?P<categoryId>\d+)/edit/$', 'category', {},
        'picket-admin-category-edit',),
    (r'^category/(?P<categoryId>\d+)/delete/$', 'remove_category', {},
        'picket-admin-category-delete',),
    (r'^scopes/$', 'scopes', {}, 'picket-admin-scopes',),
    (r'^scopes/add/$', 'add_scope', {}, 'picket-admin-scopes-add',),
    (r'^scope/(?P<scopeId>\d+)/$', 'scope', {}, 'picket-admin-scope',),
)
