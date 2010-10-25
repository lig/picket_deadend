"""
Copyright 2008-2010 Serge Matveenko, TrashNRoll

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

from .decorators import render_to
from .documents import Bug, Project
from .forms import NewBugForm


@render_to('picket/index.html')
def index(request):
    return {}


@render_to('picket/new_bug.html')
def new_bug(request):

    current_project_id = request.session.get('current_project')

    if request.method == 'POST':
        newBugForm = NewBugForm(data=request.POST,
            project_id=current_project_id)
        if newBugForm.is_valid():
            bug = Bug(**newBugForm.cleaned_data)
            if request.user.is_authenticated():
                bug.reporter = request.user
            bug.project = current_project_id and Project.objects.with_id(
                current_project_id)
            bug.save()
            """ @todo: bug creation notice and successful redirect """
    else:
        newBugForm = NewBugForm(project_id=current_project_id)

    return {'new_bug_form': newBugForm}
