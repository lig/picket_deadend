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

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from .decorators import render_to
from .documents import Project
from .forms import IssueForm, Issue


@render_to('picket/index.html')
def index(request):
    return {}


@render_to('picket/new_issue.html')
def new_issue(request):

    current_project_id = request.session.get('current_project')

    if request.method == 'POST':
        issue_form = IssueForm(data=request.POST)
        
        if issue_form.is_valid():
            request.session['return_to_form'] = issue_form.cleaned_data[
                'return_to_form']
            issue = issue_form.save(commit=False)
            
            if request.user.is_authenticated():
                issue.reporter = request.user
            
            issue.project = current_project_id and Project.objects.with_id(
                current_project_id)
            issue.save()
            messages.success(request, _('Bug submitted'))
            return redirect(issue_form.cleaned_data['return_to_form'] and
                'picket-issue-new' or issue.get_absolute_url())
    else:
        issue_form = IssueForm(
            return_to_form=request.session.get('return_to_form'))

    return {'issue_form': issue_form}


@render_to('picket/issue.html')
def issue(request, issue_number):

    issue = Issue.objects.with_id(int(issue_number))
    if not issue: raise Http404
    
    return {'issue': issue}


@render_to('picket/issues.html')
def issues(request):

    issues = Issue.objects()
    
    return {'issues': issues}
