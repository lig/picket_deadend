"""
Copyright 2009 Serge Matveenko

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

from django.http import HttpResponseForbidden, HttpResponseNotFound

from models import Project, Bug


def is_su(user):
    return user.is_superuser

def permited_project_required(required_rights='r'):
    def permited_project_view_decorator(fn):
        def permited_project_view(request, *args, **kwargs):
            def is_permited(project_id):
                return Project.objects.get(pk=project_id).is_permited(
                    request.user, required_rights)
            if ('project_id' in kwargs and is_permited(kwargs['project_id']) or
                not 'project_id' in request.session or
                is_permited(request.session['project_id'])):
                return fn(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        return permited_project_view
    return permited_project_view_decorator

def permited_bug_required(required_rights='r'):
    def permited_bug_view_decorator(fn):
        def permited_bug_view(request, bug_id, *args, **kwargs):            
            try:
                bug = Bug.objects.get(id=bug_id)
            except ValueError:
                return HttpResponseNotFound()
            if bug.is_permited(request.user, required_rights):
                return fn(request, bug, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        return permited_bug_view
    return permited_bug_view_decorator
