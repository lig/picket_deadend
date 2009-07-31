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

from django import forms
from django.utils.translation import ugettext as _

from models import (Bug, Bugnote, BugFile, BugRelationship, Scope, Category,
    User)


class BugForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super(BugForm, self).__init__(*args, **kwargs)
        if project_id is not None:
            self.fields['category'].queryset = Category.objects.filter(
                project=project_id)
    
    class Meta():
        model = Bug
        fields = ['category', 'reproducibility', 'severity', 'priority',
            'summary', 'description', 'steps_to_reproduce',
            'additional_information', 'scope',]

class BugUpdateForm(forms.ModelForm):
    class Meta():
        model = Bug
        fields = ['category', 'severity', 'reproducibility', 'reporter',
            'scope', 'handler', 'priority', 'resolution', 'status', 'summary',
            'description', 'steps_to_reproduce', 'additional_information',]


class AssignForm(forms.ModelForm):
    
    _message = _('Bug handler updated')
    
    def __init__(self, *args, **kwargs):
        super(AssignForm, self).__init__(*args, **kwargs)
        self.fields['handler'].queryset = User.objects.have_permissions('h',
            self.instance.scope)
    
    class Meta():
        model = Bug
        fields = ['handler',]
        

class StatusForm(forms.ModelForm):
    _message = _('Bug status updated')
    class Meta():
        model = Bug
        fields = ['status',]

class BugMoveForm(forms.ModelForm):
    _message = _('Bug moved')
    class Meta():
        model = Bug
        fields = ['project',]

class BugRelationshipForm(forms.ModelForm):
    destination_bug = forms.ModelChoiceField(queryset=Bug.objects.all(),
        widget=forms.TextInput)
    class Meta():
        model = BugRelationship
        fields = ['relationship_type', 'destination_bug',]

class BugFileForm(forms.ModelForm):
    class Meta():
        model = BugFile
        fields = ['title', 'file',]

class BugnoteForm(forms.ModelForm):
    class Meta():
        model = Bugnote
        fields = ['text', 'scope',]

class ReminderForm(forms.Form):
    
    recipients = forms.ModelMultipleChoiceField(label=_('Reminder recipients'),
        queryset=User.objects.filter(is_active=True),
        widget=forms.SelectMultiple(attrs={'size': '10',}))
    text = forms.CharField(label=_('Reminder text'),
        widget=forms.Textarea(attrs={'cols': '65', 'rows': '10',}))
    scope = forms.ModelChoiceField(label=_('Reminder note scope'),
        queryset=Scope.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ReminderForm, self).__init__(*args, **kwargs)
        self.fields['scope'].queryset = Scope.objects.get_permited(user)
