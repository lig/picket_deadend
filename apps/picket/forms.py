"""
Copyright 2008 Serge Matveenko

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

from django import forms

from apps.picket.models import Bug, Bugnote, Project

class BugForm(forms.ModelForm):
    class Meta():
        model = Bug
        fields = ['category', 'reproducibility', 'severity', 'priority',
            'summary', 'description', 'steps_to_reproduce',
            'additional_information', 'scope',]
""" @todo: inline form for bugfile """

class BugnoteForm(forms.ModelForm):
    class Meta():
        model = Bugnote
        fields = ['text',]

class ProjectForm(forms.ModelForm):
    class Meta():
        model = Project
        fields = ['name', 'status', 'enabled', 'scope', 'url', 'description', '', '', '', '', '', '', '', '', ]
