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
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from models import (Bug, Bugnote, BugFile, BugRelationship, Scope, Category,
    PicketUser)


class BugForm(forms.Form):
    
    project = forms.IntegerField()
    reporter = forms.CharField()
    handler = forms.CharField()
    priority = forms.ChoiceField(choices=map(lambda x: (x, x,), ('high', 'normal', 'low',)))
    status = forms.ChoiceField(choices=map(lambda x: (x, x,), ('new', 'assigned', 'resolved',)))
    category = forms.CharField()
    date_submitted = forms.DateTimeField()
    last_updated = forms.DateTimeField()
    summary = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)


class AttachmentForm(forms.ModelForm):
    
    title = forms.CharField()
    file = forms.FileField()


class BugUpdateForm(forms.ModelForm):
    class Meta():
        model = Bug
        fields = ['category', 'severity', 'reproducibility', 'reporter',
            'scope', 'handler', 'priority', 'resolution', 'status', 'summary',
            'description', 'steps_to_reproduce', 'additional_information',]


class AssignStatusForm(forms.ModelForm):
    
    _message = _('Bug handler and status updated')
    
    def __init__(self, *args, **kwargs):
        super(AssignStatusForm, self).__init__(*args, **kwargs)
        self.fields['handler'].queryset = PicketUser.objects.have_permissions(
            'h', self.instance.scope)
    
    class Meta():
        model = Bug
        fields = ['handler', 'status',]
        

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
