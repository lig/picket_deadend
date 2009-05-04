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
from django.contrib.auth.models import User
from django.db.models import Q

import filter as fltr

from models import Bug, Project, Category, Scope
from settings import *

class FilterableQ(Q):
    def filter(self, **kwargs):
        self = Q(self, Q(**kwargs))

class MultiCharFilter(fltr.Filter):
    field_class = forms.CharField
    
    def __init__(self, *args, **kwargs):
        self.field_names = kwargs.pop('field_names')
        super(MultiCharFilter, self).__init__(*args, **kwargs)
    
    def filter(self, qs, value):
        if value:
            my_name = self.name
            q = FilterableQ()
            for field_name in self.field_names:
                self.name = field_name
                q |= super(MultiCharFilter, self).filter(q, value)
            self.name = my_name
            qs = qs.filter(q).distinct()
        return qs

class BugFilter(fltr.FilterSet):
    
    project = fltr.ModelMultipleChoiceFilter(queryset=Project.objects.all())
    reporter = fltr.ModelMultipleChoiceFilter(
        queryset=User.objects.filter(is_active=True))
    handler = fltr.ModelMultipleChoiceFilter(
        queryset=User.objects.filter(is_active=True))
    priority = fltr.MultipleChoiceFilter(choices=PRIORITY_CHOICES)
    severity = fltr.MultipleChoiceFilter(choices=SEVERITY_CHOICES)
    reproducibility = fltr.MultipleChoiceFilter(
        choices=REPRODUCIBILITY_CHOICES)
    status = fltr.MultipleChoiceFilter(choices=BUG_STATUS_CHOICES)
    resolution = fltr.MultipleChoiceFilter(choices=RESOLUTION_CHOICES)
    projection = fltr.MultipleChoiceFilter(choices=PROJECTION_CHOICES)
    category = fltr.ModelMultipleChoiceFilter(queryset=Category.objects.all())
    date_submitted = fltr.DateRangeFilter()
    last_updated = fltr.DateRangeFilter()
    eta = fltr.MultipleChoiceFilter(choices=ETA_CHOICES)
    scope = fltr.ModelMultipleChoiceFilter(queryset=Scope.objects.all())
    search = MultiCharFilter(
        field_names=['summary', 'description', 'steps_to_reproduce',
            'additional_information',],
        lookup_type='contains')
    sponsorship_total = fltr.NumberFilter(lookup_type='gte')
    sticky = fltr.BooleanFilter()
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(BugFilter, self).__init__(*args, **kwargs)
        self.filters['project'].queryset = Project.objects.get_permited(user)
        self.filters['category'].queryset = Category.objects.filter(
            project__in=self.filters['project'].queryset)
        self.filters['scope'].queryset = Scope.objects.get_permited(user)
    
    class Meta:
        model = Bug
        fields = ['project', 'reporter', 'handler', 'priority', 'severity',
            'reproducibility', 'status', 'resolution', 'projection',
            'category', 'date_submitted', 'last_updated', 'eta', 'scope',
            'sponsorship_total', 'sticky',]
