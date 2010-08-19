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


class Scope(Document):

    name = StringField(required=True, unique=True)
    read_access = ListField(ReferenceField(Group))
    write_access = ListField(ReferenceField(Group))
    anonymous_access = BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.name


class Category(Document):

    name = StringField(required=True, unique=True)
    handler = ReferenceField(User)

    def __unicode__(self):
        return u'%s' % self.name

    @permalink
    def get_absolute_url(self):
        return ('picket-category', [str(self.id)])

    class Meta():
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        unique_together = (('project', 'name'),)
    

class Project(Document):

    name = StringField(required=True, unique=True)
    """ @todo: possible project status values setting """ 
    status = StringField()
    enabled = BooleanField(default=True)
    scope = ReferenceField(Scope, required=True)
    url = URLField()
    description = StringField()
    parent = ReferenceField('self')
    categories = ListField(ReferenceField(Category))
    inherit_categories = BooleanField(default=True)

    def is_permited(self, user, required_rights='r'):
        """ @todo: implement permission handling via mongoengine """
        return True

    def __unicode__(self):
        return u'%s' % self.name

    @permalink
    def get_absolute_url(self):
        return ('picket-project', [str(self.id)])


class BugHistory(Document):

    user = ReferenceField(User)
    bug = ReferenceField(Bug)
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
    steps_to_reproduce = ListField(StringField)
    additional_information = StringField()
    sponsorship_total = IntField()
    sticky = BooleanField(default=False)
    history = ListField(ReferenceField(BugHistory))
    """ @todo: add reporters, handlers and commentators as monitorers
        automatically """
    monitorers = ListField(ReferenceField(User))
    related_bugs = ListField(ReferenceField('self'))
    child_bugs = ListField(ReferenceField('self'))
    duplicates = ListField(ReferenceField('self'))
    num_bugnotes = IntField(default=0)

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


class PicketUser(User):
    objects = PicketUserManager()
    
    class Meta:
        proxy = True
        ordering = ["username"]


class ScopeGroup(models.Model):
    objects = models.Manager()

    rights = models.CharField(_('rights'), choices=RIGHTS,
        max_length=max(len(right[0]) for right in RIGHTS))
    scope = models.ForeignKey('Scope', verbose_name=_('scope'))
    group = models.ForeignKey(Group, verbose_name=_('group'))


class BugFile(models.Model):
    bug = models.ForeignKey(Bug, verbose_name=_('bug'))
    title = models.CharField(_('bug file title'), max_length=750)
    file = models.FileField(_('bug file'), upload_to='bugs/%Y/%m/%d-%H')
    date_added = models.DateTimeField(_('bug file date added'),
        auto_now_add=True, editable=False)

    def __unicode__(self):
        return u'%s' % self.title

    def get_file_icon(self):
        """ returns path of the file icon by file extension """

        fileicons_path = os.path.join(settings.MEDIA_ROOT, 'images',
            'fileicons')
        fileicons_url = os.path.join(settings.MEDIA_URL, 'images', 'fileicons')

        ext = os.path.splitext(self.file.path)[1][1:]
        icon_name = '%s.gif' % ext
        if len(ext) == 0:
            icon_name = 'generic.gif'
        elif not os.path.exists(os.path.join(fileicons_path, icon_name)):
            icon_name = 'unknown.gif'
        return os.path.join(fileicons_url, icon_name)

    @staticmethod
    def from_message_part(bug, part):
        filename = part.get_filename()

        bugFile = BugFile(bug=bug, title=filename)

        file = File(NamedTemporaryFile())
        file.write(part.get_payload(decode=True))

        bugFile.file.save(filename, file, save=False)

        return bugFile

    class Meta():
        verbose_name = _('bug file')
        verbose_name_plural = _('bug files')
        ordering = ['date_added',]

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('project'))
    title = models.CharField(_('project file title'), max_length=750)
    file = models.FileField(_('project file'),
        upload_to='projects/%Y/%m/%d-%H')
    date_added = models.DateTimeField(_('project file date added'),
        auto_now_add=True, editable=False)
    description = models.TextField(_('project file description'), blank=True)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta():
        verbose_name = _('project file')
        verbose_name_plural = _('project files')
        ordering = ['date_added',]


class Bugnote(models.Model):
    bug = models.ForeignKey(Bug, verbose_name=_('bugnote bug'))
    reporter = models.ForeignKey(User, verbose_name=_('bugnote user'))
    text = models.TextField(_('bugnote text'))
    scope = models.ForeignKey(Scope,
        verbose_name=_('bugnote scope'), null=True, blank=True)
    date_submitted = models.DateTimeField(_('bugnote date submitted'),
        auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_('bugnote last modified'),
        auto_now=True, editable=False)
    note_type = models.IntegerField(_('bugnote type'),
        null=True, blank=True)
    note_attr = models.CharField(_('bugnote attr'),
        max_length=750, blank=True)

    def save(self, *args, **kwargs):
        if self.scope is None:
            self.scope = self.bug.scope
        self.bug.num_bugnotes = self.bug.bugnote_set.all().count()
        self.bug.save()
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
                    BugFile.from_message_part(bug, part).save()

        """ cleanup quotes from reply and save bugnote """
        bugnote_lines = []
        for line in bugnote.text.splitlines():
            if not line.startswith('>'):
                bugnote_lines.append(line)
        bugnote.text = '\n\r'.join(bugnote_lines)
        bugnote.save()

        return bugnote

    class Meta():
        verbose_name = _('bugnote')
        verbose_name_plural = _('bugnotes')
        ordering = ['date_submitted',]
