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
from django.utils.translation import ugettext_lazy as _

from ..models import Scope, ScopeGroup, Project, Category

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

class ProjectForm(forms.ModelForm):
    class Meta():
        model = Project
        fields = ['name', 'status', 'enabled', 'scope', 'url', 'description',]

class CategoryForm(forms.ModelForm):
    
    def clean_mail_addr(self):
        mail_addr = self.cleaned_data['mail_addr']
        if (mail_addr and
                Category.objects.filter(mail_addr=mail_addr).count() > 0):
            raise forms.ValidationError(_('Email address already in use'))
        return mail_addr
    
    class Meta():
        model = Category
        fields = ['name', 'handler', 'mail_addr',]

class CategoryQuickForm(forms.ModelForm):
    class Meta():
        model = Category
        fields = ['name',]

ScopegroupFormset = forms.models.inlineformset_factory(parent_model=Scope,
    model=ScopeGroup, fields=['group', 'rights',])
