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

from datetime import datetime

from django.db.models import permalink
from mongoengine import *
from mongoengine.django.auth import User

from sequences import get_next_pk


class Employee(User):
    
    department = ReferenceField('Department')
    
    def __unicode__(self):
        if self.first_name or self.last_name:
            return u' '.join((self.first_name, self.last_name,)).strip()
        else:
            return self.username
    
    @permalink
    def get_absolute_url(self):
        return 'picket-admin-employee', (self.pk,)
    
    @queryset_manager
    def all(self, qs):
        return User.objects
    
    @classmethod
    def from_user(cls, user, commit=True):
        employee = Employee(pk=user.pk, **user.to_mongo())
        if commit:
            employee.save()
        return employee


class Project(Document):
    
    name = StringField(max_length=255, required=True, unique=True)
    manager = ReferenceField(User)
    
    def __unicode__(self):
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return 'picket-admin-project', (self.id,)


class Department(Document):
    
    name = StringField(max_length=255, required=True, unique=True)
    head = ReferenceField(User)
    
    def save(self, *args, **kwargs):
        super(Department, self).save(*args, **kwargs)
        self.head.department = self
        self.head.save()
    
    def __unicode__(self):
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return 'picket-admin-department', (self.id,)


class Group(Document):
    
    department = ReferenceField(Department, required=True)
    project = ReferenceField(Project, required=True)
    employees = ListField(ReferenceField(User))


class Stage(Document):
    
    name = StringField(required=True)
    department = ReferenceField(Department)
    order = IntField()
    first = GenericReferenceField() # Status, Stage


class Milestone(EmbeddedDocument):
    
    stage = ReferenceField(Stage, required=True)
    deadline = DateTimeField(required=True)


class Release(Document):
    
    name = StringField(required=True)
    project = ReferenceField(Project, required=True)
    deadline = DateTimeField()
    current_stage = ReferenceField(Stage)
    milestones = SortedListField(EmbeddedDocumentField(Milestone),
        ordering='deadline')


class Status(Document):
    
    name = StringField(required=True)
    department = ReferenceField(Department, required=True)
    handler = GenericReferenceField() # Employee, Group, Department
    next = ListField(GenericReferenceField()) # Status, Stage


class Comment(EmbeddedDocument):
    
    submitted = DateTimeField(required=True)
    author = ReferenceField(User)
    text = StringField(required=True)

    
class Issue(Document):
    
    meta = {
        'ordering': ('-submitted',),
    }
    
    number = IntField(primary_key=True)
    subject = StringField(max_length=1024, required=True)
    submitted = DateTimeField(required=True)
    author = ReferenceField(User)
    text = StringField(required=True)
    project = ReferenceField(Project, required=True)
    status = ReferenceField(Status)
    handler = GenericReferenceField() # Employee, Group, Department
    comments = SortedListField(EmbeddedDocumentField(Comment),
        ordering='submitted')
    
    def __unicode__(self):
        return '[%s] %s' % (self.number, self.subject)

    @permalink
    def get_absolute_url(self):
        return 'picket-issue', (self.number,)
    
    def save(self):
        #@todo: status and other logic handling
        
        self.number = self.number or get_next_pk('issue')
        self.submitted = self.submitted or datetime.utcnow()
        
        super(Issue, self).save()
