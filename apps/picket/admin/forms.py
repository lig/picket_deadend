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

from django import forms
from django.contrib.auth.models import User, Group

from ..models import Scope, ScopeGroup

class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups',]

class GroupForm(forms.ModelForm):
    class Meta():
        model = Group
        fields = ['name',]

class ScopeForm(forms.ModelForm):
    class Meta():
        model = Scope
        fields = ['name', 'anonymous_access',]

ScopegroupFormset = forms.models.inlineformset_factory(parent_model=Scope,
    model=ScopeGroup, fields=['group', 'rights',])
