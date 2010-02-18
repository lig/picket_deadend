"""
Copyright 2008-2009 Serge Matveenko, TrashNRoll, Alexey Smirnov

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

from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, post_init
from django.utils.translation import ugettext_lazy as _

from alerts import send_alerts
from models import BugRelationship, BugHistory, Bugnote, Bug
from settings import BUGRELATIONSHIP_TYPE_REVERSE_MAP


def bugrelationship_reverse_update(*args, **kwargs):
    """
    @author: lig
    """
    relationship = kwargs.pop('instance')
    
    if not relationship.is_reverse:
        
        reverse_relationship_type = \
            BUGRELATIONSHIP_TYPE_REVERSE_MAP[relationship.relationship_type]
        
        reverse_relationship, created = BugRelationship.objects.get_or_create(
            source_bug=relationship.destination_bug,
            destination_bug=relationship.source_bug,
            defaults={'relationship_type': reverse_relationship_type})
        
        """ force correct relationship type """
        reverse_relationship.relationship_type = reverse_relationship_type
        
        """ force correct direction value """
        reverse_relationship.is_reverse = True
        
        reverse_relationship.save()

post_save.connect(bugrelationship_reverse_update, BugRelationship)


def bugrelationship_reverse_remove(*args, **kwargs):
    """
    @author: lig
    """
    relationship = kwargs.pop('instance')
    
    try:
        reverse_relationship = BugRelationship.objects.get(
            source_bug=relationship.destination_bug,
            destination_bug=relationship.source_bug)
    except BugRelationship.DoesNotExist:
        """
        just proceed silently if there is no reverse relationship
        """
        pass
    else:
        reverse_relationship.delete()

post_delete.connect(bugrelationship_reverse_remove, BugRelationship)


def bugmonitor_update_from_bughistory(*args, **kwargs):
    """
    @author: lig, TrashNRoll
    """
    history_entry = kwargs.pop('instance')
    
    """ process appropriate field if changed reporter, handler, or author or
        all possible fields if bug just created """
    bug = history_entry.bug

    if history_entry.type == 0:
        bug.add_monitor(bug.reporter)
        bug.add_monitor(bug.handler)
    elif history_entry.field_name == 'handler_id' and bug.handler:
        bug.add_monitor(bug.handler)

post_save.connect(bugmonitor_update_from_bughistory, BugHistory)


def bugmonitor_update_from_bugnote(*args, **kwargs):
    """
    @author: lig
    """
    bugnote = kwargs.pop('instance')
    bugnote.bug.add_monitor(bugnote.reporter)

post_save.connect(bugmonitor_update_from_bugnote, Bugnote)


def bug_notify_change(*args, **kwargs):
    """
    @author: lig
    """
    history_entry = kwargs.pop('instance')
    bug = history_entry.bug
    
    recipients = User.objects.filter(bugmonitor__bug=bug)
    
    """ @todo: handle relationship change """
    if history_entry.type == 0:
        """ bug created """
        message = _('''Bug #%(bug_id)s is created''' %
            {'bug_id': bug.get_id_display(),})
    elif history_entry.type == 1:
        """ bug changed """
        message = _('''Bug #%(bug_id)s is changed:
field %(field_name)s was %(old_value)s changed to %(new_value)s''' %
            {'bug_id': bug.get_id_display(),
                'field_name': history_entry.field_name,
                'old_value': history_entry.old_value,
                'new_value': history_entry.new_value,})
    else:
        """ bug changed somehow """
        message = _('''Bug #%(bug_id)s is changed''' %
            {'bug_id': bug.get_id_display(),})
    
    send_alerts(bug, recipients, message)

post_save.connect(bug_notify_change, BugHistory)


def bug_notify_bugnote(*args, **kwargs):
    """
    @author: lig
    """
    bugnote = kwargs.pop('instance')
    bug = bugnote.bug
    
    recipients = User.objects.filter(bugmonitor__bug=bug)
    
    message = _('''User %(user)s has added bugnote to the bug #%(bug_id)s:
%(bugnote_text)s''' %
        {'user': bugnote.reporter, 'bug_id': bug.get_id_display(),
            'bugnote_text': bugnote.text,})
    
    send_alerts(bug, recipients, message)

post_save.connect(bug_notify_bugnote, Bugnote)


def bug_assign_to_category_handler(*args, **kwargs):
    """
    @author: lig
    """
    bug = kwargs.pop('instance')
    created = kwargs.pop('created')
    
    if created and bug.category.handler:
        if not bug.handler:
            bug.handler = bug.category.handler
        else:
            bug.add_monitor(bug.category.handler)

post_save.connect(bug_assign_to_category_handler, Bug)


class BugHistoryHandler(object):
    
    def __init__(self, user):
        self._bug_cache={}
        self._user = user
        post_init.connect(self.bug_post_init_handler, Bug)
        post_save.connect(self.bug_post_save_handler, Bug)
    
    def bug_post_init_handler(self, sender, instance, **kwargs):
        if not instance.pk in self._bug_cache:
            """
            key for instance must be created to not trigger this mechanism on
            another object initialization follows
            """
            self._bug_cache[instance.pk] = None
            try:
                self._bug_cache[instance.pk] = Bug.objects.get(pk=instance.pk)
            except Bug.DoesNotExist:
                del self._bug_cache[instance.pk]
    
    def bug_post_save_handler(self, sender, instance, created, **kwargs):
        """
        type = models.PositiveIntegerField(_('bug history entry type'),
            choices=(
                (0,_('bug created'),),
                (1,_('field changed'),),
                (2,_('relationship added'),),
                (3,_('relationship changed'),),
                (4,_('relationship removed'),),
            ))
        """
        if created:
            bugHistory = BugHistory(bug=instance, type=0, user=self._user)
            bugHistory.save()
            del bugHistory
        else:
            """
            @todo: handle TextFieldS changes
            @todo: handle relationship changes
            """
            for log_field in ['project_id', 'reporter_id', 'handler_id',
                'duplicate_id', 'priority', 'severity', 'reproducibility',
                'status', 'resolution', 'projection', 'category_id',
                'scope_id', 'summary', 'sponsorship_total', 'sticky',]:
                get_log_field_display = 'get_%s_display' % log_field
                attribute_name = get_log_field_display if \
                    get_log_field_display in dir(instance) else log_field
                old_value = self._bug_cache[instance.pk].__getattribute__(
                    attribute_name)
                new_value = instance.__getattribute__(attribute_name)
                if callable(new_value):
                    old_value, new_value = old_value(), new_value()
                if new_value != old_value:
                    bugHistory = BugHistory(bug=instance, type=1,
                        field_name=log_field, old_value=old_value,
                        new_value=new_value, user=self._user)
                    bugHistory.save()
                    del bugHistory
        self._bug_cache[instance.pk] = instance
    
    def __del__(self):
        post_init.disconnect(self.bug_post_init_handler, Bug)
        post_save.disconnect(self.bug_post_save_handler, Bug)
