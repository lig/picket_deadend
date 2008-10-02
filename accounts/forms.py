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
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from accounts.models import Validator

class RegForm(forms.ModelForm):
    
    def clean_username(self):
        if 0 < User.objects.filter(username=self.cleaned_data['username']).count():
            raise forms.ValidationError(_('Username already exists.'))
        return self.cleaned_data['username']

    """ don't know if people like to give ability to know that they are registered here...
    def clean_email(self):
        if 0 < User.objects.filter(email=self.cleaned_data['email']).count():
            raise forms.ValidationError(_('Email already exists.'))
    """

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
class ValForm(forms.Form):
    
    username    = forms.CharField()
    code        = forms.CharField()
    
    def clean(self):
        self.hash = Validator.get_hash(self.cleaned_data['username'],
            self.cleaned_data['code'])
        try:
            Validator.objects.get(hash=self.hash)
            return self.cleaned_data
        except Validator.DoesNotExist:
            raise forms.ValidationError(_('Wrong validation code for this username or user email already validated.'))

class PassForm(forms.Form):
    
    password    = forms.CharField(widget=forms.PasswordInput)
    password2   = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        if not self.cleaned_data['password']==self.cleaned_data['password2']:
            raise forms.ValidationError(_('Passwords do not match.'))
        return self.cleaned_data
