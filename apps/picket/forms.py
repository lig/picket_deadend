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

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from mongoforms.forms import MongoForm

from documents import Project, Department, Issue, Employee


class AuthForm(AuthenticationForm):
    i_am_auth_form = forms.BooleanField(initial=True, widget=forms.HiddenInput)


class ProjectForm(MongoForm):
    
    class Meta:
        document = Project
        fields = ('name', 'manager',)


class DepartmentForm(MongoForm):
    
    class Meta:
        document = Department
        fields = ('name', 'head',)


class IssueForm(MongoForm):
    
    return_to_form = forms.BooleanField(required=False)
    
    def __init__(self, return_to_form=False, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.fields['return_to_form'].initial = return_to_form
    
    class Meta:
        document = Issue
        fields = ('subject', 'text',)


class EmployeeCreationForm(MongoForm):
    """
    A form that creates an emloyee, from the given username and password.
    """
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))
    
    class Meta:
        document = Employee
        fields = ("username",)
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        if Employee.objects._collection.find_one({'username': username}):
            raise forms.ValidationError(
                _("A user with that username already exists."))
        else:
            return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))
        return password2
    
    def save(self, commit=True):
        employee = super(EmployeeCreationForm, self).save(commit=False)
        employee.set_password(self.cleaned_data["password1"])
        if commit:
            employee.save()
        return employee


class EmployeeChangeForm(MongoForm):
    #@todo: password change form
    
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})

    class Meta:
        document = Employee
