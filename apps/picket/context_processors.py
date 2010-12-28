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

from django.contrib.auth import login
from mongoengine.base import ValidationError

from . import COPYING
from .documents import Project
from .forms import AuthForm


def picket(request):

    # set or get current project
    if 'set_project' in request.GET:
        try:
            current_project = Project.objects.with_id(
                request.GET['set_project'])
            # current_project could be None after lookup
            request.session['current_project'] = (current_project and
                current_project.id)
        except ValidationError:
            current_project = None
    else:
        try:
            current_project = Project.objects.with_id(
                request.session.get('current_project'))
        except ValidationError:
            current_project = None

    # get projects
    projects = Project.objects()

    # authentication
    if not request.user.is_authenticated():
        if request.method == 'POST' and request.POST.get('i_am_auth_form'):
            auth_form = AuthForm(data=request.POST)
            if auth_form.is_valid():
                login(request, auth_form.get_user())
        else:
            auth_form = AuthForm()
    else:
        auth_form = None

    return {'copying': COPYING, 'current_project': current_project,
        'projects': projects, 'auth_form': auth_form}
