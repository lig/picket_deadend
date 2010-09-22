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

from mongoengine import *
from mongoengine.django.auth import User
from mongoengine.fields import BaseField

from django.db.models import permalink

from .mail_utils import text_from_part
    

def sorted(doc_cls, queryset):
    return queryset.order_by('name')

def to_choices(doc_cls, queryset):
    return tuple(map(lambda item: (item.id, item.name,), queryset))

    
class Group(Document):

    name = StringField(required=True, unique=True)
    users = ListField(ReferenceField(User))


class Scope(Document):

    name = StringField(required=True, unique=True)
    read_access = ListField(ReferenceField(Group))
    write_access = ListField(ReferenceField(Group))
    anonymous_access = BooleanField(default=False)

    sorted = queryset_manager(sorted)
    to_choices = queryset_manager(to_choices)

    def __unicode__(self):
        return u'%s' % self.name


class Category(Document):

    name = StringField(required=True, unique=True)
    handler = ReferenceField(User)

    sorted = queryset_manager(sorted)
    to_choices = queryset_manager(to_choices)

    def __unicode__(self):
        return u'%s' % self.name

    @permalink
    def get_absolute_url(self):
        return ('picket-category', [str(self.id)])
    

class Attachment(EmbeddedDocument):
    
    title = StringField()
    """ @todo: use FileField from mongoengine 0.4 when it will be released """
    file = BinaryField(required=True)


class Project(Document):

    name = StringField(required=True, unique=True)
    """ @todo: possible project status values setting """ 
    status = StringField()
    enabled = BooleanField(default=True)
    """ @todo: set required=True on scope after scope admin is ready """
    scope = ReferenceField(Scope)
    url = URLField()
    description = StringField()
    parent = ReferenceField('self')
    categories = ListField(ReferenceField(Category))
    attachments = ListField(EmbeddedDocumentField(Attachment))

    sorted = queryset_manager(sorted)
    to_choices = queryset_manager(to_choices)

    @queryset_manager
    def get_enabled(self, qs):
        return qs(enabled=True)

    def is_permited(self, user, required_rights='r'):
        """ @todo: implement permission handling via mongoengine """
        return True

    def __unicode__(self):
        return u'%s' % self.name

    @permalink
    def get_absolute_url(self):
        return ('picket-project', [str(self.id)])


class BugHistory(EmbeddedDocument):

    user = ReferenceField(User)
    date = DateTimeField()
    field_name = StringField()
    old_value = BaseField()
    new_value = BaseField()
    """ @todo: possible history entry type values setting """ 
    type = StringField()


class Bug(Document):

    number = IntField(required=True, unique=True)
    project = ReferenceField(Project, required=True)
    reporter = ReferenceField(User)
    handler = ReferenceField(User)
    """ @todo: possible priority values setting """ 
    priority = StringField()
    """ @todo: possible severity values setting """ 
    severity = StringField()
    """ @todo: possible reproducibility values setting """ 
    reproducibility = StringField()
    """ @todo: possible status values setting """ 
    status = StringField()
    """ @todo: possible resolution values setting """ 
    resolution = StringField()
    """ @todo: possible projection values setting """ 
    projection = StringField()
    category = ReferenceField(Category, required=True)
    date_submitted = DateTimeField(required=True)
    last_updated = DateTimeField(required=True)
    """ @todo: possible ETA values setting """ 
    eta = StringField()
    scope = ReferenceField(Scope, required=True)
    summary = StringField(max_length=255, required=True)
    description = StringField(required=True)
    steps_to_reproduce = ListField(StringField())
    additional_information = StringField()
    sponsorship_total = IntField()
    sticky = BooleanField(default=False)
    history = ListField(EmbeddedDocumentField(BugHistory))
    """ @todo: add reporters, handlers and commentators as monitorers
        automatically """
    monitorers = ListField(ReferenceField(User))
    related_bugs = ListField(ReferenceField('self'))
    child_bugs = ListField(ReferenceField('self'))
    duplicates = ListField(ReferenceField('self'))
    num_bugnotes = IntField(default=0)
    attachments = ListField(EmbeddedDocumentField(Attachment))

    def save(self, *args, **kwargs):
        """ @todo: bug number generation """
        if self.number is None:
            from random import randint
            self.number = randint(1, 1000000000)
        if self.project is None:
            self.project = self.category.project
        if self.scope is None:
            self.scope = self.project.scope
        super(Bug, self).save(*args, **kwargs)

    def is_permited(self, user, required_rights='r'):
        """ @todo: implement permission handling via mongoengine """
        return True

    def __unicode__(self):
        return u'%s: %s' % (self.id, self.summary)

    @permalink
    def get_absolute_url(self):
        return ('picket-bug', [str(self.number)])

    def add_monitor(self, user):
        """ @todo: add_monitor """
        raise NotImplementedError()

    def get_status_color(self):
        """ @todo: get_status_color """
        raise NotImplementedError()

    def get_priority_icon(self):
        """ @todo: get_priority_icon """
        raise NotImplementedError()

    def get_id_display(self):
        """ @todo: get_id_display """
        raise NotImplementedError()

    def get_handler_id_display(self):
        """ @todo: get_handler_id_display """
        raise NotImplementedError()

    def get_category_id_display(self):
        """ @todo: get_category_id_display """
        raise NotImplementedError()

    def get_project_id_display(self):
        """ @todo: get_project_id_display """
        raise NotImplementedError()

    def get_duplicate_id_display(self):
        """ @todo: get_duplicate_id_display """
        raise NotImplementedError()
    
    def get_description_display(self):
        """ @todo: get_description_display """
        raise NotImplementedError()
    
    def get_steps_to_reproduce_display(self):
        """ @todo: get_steps_to_reproduce_display """
        raise NotImplementedError()
    
    def get_additional_information_display(self):
        """ @todo: get_additional_information_display """
        raise NotImplementedError()
    
    def is_resolved(self):
        """ @todo: is_resolved """
        raise NotImplementedError()

    @staticmethod
    def has_field(field):
        """ @todo: has_field """
        raise NotImplementedError()

    @staticmethod
    def has_custom_sorter(field):
        """ @todo: has_custom_sorter """
        raise NotImplementedError()

    @staticmethod
    def field_is_sortable(field):
        """ @todo: field_is_sortable """
        raise NotImplementedError()

    @staticmethod
    def from_message(category, reporter, message):
        """ @todo: from_message """
        raise NotImplementedError()


class Bugnote(Document):
    
    bug = ReferenceField(Bug, required=True)
    reporter = ReferenceField(User, required=True)
    text = StringField(required=True)
    scope = ReferenceField(Scope)
    """ @todo: autoupdate dates """
    date_submitted = DateTimeField()
    last_modified = DateTimeField()

    def save(self, *args, **kwargs):
        """ @todo: autoupdate Bug num_bugnotes property """
        super(Bugnote, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s: %s at %s' % (
            self.bug, self.reporter, self.date_submitted)

    def get_absolute_url(self):
        return '%s#bugnote%s' % (self.bug.get_absolute_url(), self.id)

    @staticmethod
    def from_message(bug, reporter, message):
        bugnote = Bugnote(bug=bug, reporter=reporter)

        if message.get_content_maintype() == 'text':
            bugnote.text = text_from_part(message)
        elif message.get_content_maintype() == 'multipart':
            bugnote.text = ''
            for part in message.walk():
                if part['Content-Disposition'] == 'inline':
                    bugnote.text += text_from_part(part)
                elif part['Content-Disposition'] and \
                  part['Content-Disposition'].startswith('attachment;'):
                    """ @todo: attachment saving """
                    #BugFile.from_message_part(bug, part).save()

        """ cleanup quotes from reply and save bugnote """
        bugnote_lines = []
        for line in bugnote.text.splitlines():
            if not line.startswith('>'):
                bugnote_lines.append(line)
        bugnote.text = '\n\r'.join(bugnote_lines)
        bugnote.save()

        return bugnote


class UserInfo(User):
    
    current_project = ReferenceField(Project)
