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

from django.db.models import permalink


class Bug(Document):
    
    number = IntField(required=True, unique=True)
    project = ReferenceField(Project, required=True)
    reporter = ReferenceField(User)
    handler = ReferenceField(User)
    duplicate = ReferenceField(User)
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
    monitor = ListField(ReferenceField(BugMonitor))
    relationship = ListField(ReferenceField(BugRelationship))
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
        """ @todo: implement permission handling via mongoengine
        
        if user.is_superuser:
            return True
        elif self.scope.anonymous_access and required_rights == 'r':
            return True
        elif user.is_anonymous():
            return False
        else:
            permission = ScopeGroup.objects.get(
                scope=self.project.scope, group__in=user.groups.all())
            return self in Bug.objects.permited(user) and all(
                (right in permission.rights for right in required_rights))
        """
        return True

    def __unicode__(self):
        return u'%s: %s' % (self.id, self.summary)

    @models.permalink
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


class ScopeManager(models.Manager):

    def get_permited(self, user):

        if user.is_superuser:
            return self.all()
        else:
            q = models.Q(anonymous_access=True)

            if not user.is_anonymous():
                q |= models.Q(groups__user=user)

            return self.filter(q)

class ProjectManager(models.Manager):
    def get_permited(self, user):
        if user.is_superuser:
            return self.all()
        else:
            return self.filter(scope__in=Scope.objects.get_permited(user))

class BugManager(models.Manager):

    def permited(self, user, project=None, category=None):

        if user.is_superuser:
            bugs = self.select_related()
        else:
            bugs = self.select_related().filter(
                scope__in=Scope.objects.get_permited(user),
                project__in=Project.objects.get_permited(user))

        bugs = bugs.filter(project=project) if project is not None else bugs
        bugs = bugs.filter(category=category) if category is not None else bugs

        return bugs

class BugMonitorManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(mute=False)


class PicketUserManager(models.Manager):
    def have_permissions(self, permissions, scope):
        rights_q = reduce(lambda q1, q2: q1 | q2,
            map(lambda char: models.Q(
                    groups__scopegroup__rights__contains=char),
                permissions))
        return self.filter(rights_q, groups__scope=scope).distinct()


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

class Scope(models.Model):
    objects = ScopeManager()

    name = models.CharField(_('scope name'),
        unique=True, max_length=255)
    groups = models.ManyToManyField(Group,
        verbose_name=_('scope groups'),
        help_text=_('groups allowed to view items in this scope'),
        through=ScopeGroup)

    anonymous_access = models.BooleanField(_('anonymous users allowed to view \
        items in this scope'))

    def __unicode__(self):
        return u'%s' % self.name

    class Meta():
        verbose_name = _('scope')
        verbose_name_plural = _('scopes')

class Project(models.Model):
    objects = ProjectManager()

    name = models.CharField(_('project name'),
        unique=True, max_length=255)
    status = models.PositiveIntegerField(_('project status'),
        choices=PROJECT_STATUS_CHOICES,
        default=PROJECT_STATUS_CHOICES_DEFAULT)
    enabled = models.BooleanField(_('project enabled'), default=True)
    scope = models.ForeignKey(Scope,
        verbose_name=_('project scope'))
    url = models.URLField(_('project url'), verify_exists=False, blank=True)
    description = models.TextField(_('project description'),
        blank=True)
    parent = models.ForeignKey('Project',
        verbose_name=_('project parent'), blank=True, null=True)

    def is_permited(self, user, required_rights='r'):
        def check_permissions():
            permission = ScopeGroup.objects.get(
                scope=self.scope, group__in=user.groups.all())
            return all(
                (right in permission.rights for right in required_rights))
        return (user.is_superuser or self.scope.anonymous_access or
            self in Project.objects.get_permited(user) and check_permissions())

    def __unicode__(self):
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        if INTEGRATION_ENABLED and INTEGRATION_PROJECT_VIEW:
            return reverse(INTEGRATION_PROJECT_VIEW,
                kwargs={'mantis_project': self.pk})
        else:
            return ('picket-project', [str(self.id)])

    class Meta():
        verbose_name = _('project')
        verbose_name_plural = _('projects')

class Category(models.Model):
    objects = models.Manager()

    project = models.ForeignKey(Project,
        verbose_name=_('category project'))
    name = models.CharField(_('category name'), max_length=192)
    handler = models.ForeignKey(User,
        verbose_name=_('category handler'), blank=True, null=True)
    mail_addr = models.EmailField(_('category email'), blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('picket-category', [str(self.project_id), str(self.id)])

    class Meta():
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        unique_together = (('project', 'name'),)


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

class BugHistory(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(User,
        verbose_name=_('bug history entry user'))
    bug = models.ForeignKey(Bug, verbose_name=_('bug'))
    date_modified = models.DateTimeField(_('bug history entry date'),
        auto_now=True)
    field_name = models.CharField(_('bug history entry field'),
        max_length=96, blank=True)
    old_value = models.CharField(
        _('bug history entry old field value'),
        max_length=255, blank=True, null=True)
    new_value = models.CharField(
        _('bug history entry new field value'),
        max_length=255, blank=True, null=True)
    type = models.PositiveIntegerField(_('bug history entry type'),
        choices=(
            (0,_('bug created'),),
            (1,_('field changed'),),
            (2,_('relationship added'),),
            (3,_('relationship changed'),),
            (4,_('relationship removed'),),
        ))
    class Meta():
        verbose_name = _('bug history entry')
        verbose_name_plural = _('bug history entries')
        ordering = ['date_modified',]

    def get_old_value_display(self):
        b = Bug()
        setattr(b, self.field_name, self.old_value)
        return get_attr_display(b, self.field_name)

    def get_new_value_display(self):
        b = Bug()
        setattr(b, self.field_name, self.new_value)
        return get_attr_display(b, self.field_name)


class BugMonitor(models.Model):
    objects = BugMonitorManager()

    user = models.ForeignKey(User, verbose_name=_('bug monitor user'))
    bug = models.ForeignKey(Bug, verbose_name=_('bug'))
    mute = models.BooleanField(_('bug monitor mute'), default=False)

    class Meta():
        verbose_name = _('bug monitor entry')
        verbose_name_plural = _('bug monitor entries')
        unique_together = ('user', 'bug',)

class BugRelationship(models.Model):
    objects = models.Manager()

    source_bug = models.ForeignKey(Bug,
        verbose_name=_('bug relationship source'),
        related_name='source')
    destination_bug = models.ForeignKey(Bug,
        verbose_name=_('bug relationship destination'),
        related_name='destination')
    relationship_type = models.IntegerField(_('bug relationship type'),
        choices=BUGRELATIONSHIP_TYPE_CHOICES,
        default=BUGRELATIONSHIP_TYPE_DEFAULT, blank=True)
    is_reverse = models.BooleanField(_('is it reverse bug relationship'),
        default=False, editable=False)

    class Meta():
        verbose_name = _('bug relationship entry')
        verbose_name_plural = _('bug relationship entries')

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
