"""
Copyright 2008-2009 Serge Matveenko

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
from django.db.models.signals import post_save, post_delete, pre_save
from django.utils.translation import ugettext_lazy as _

from ..alerts import send_alerts
from middleware import PicketSignalsMiddleware
from ..models import BugRelationship, BugHistory, Bugnote, Bug
from ..settings import BUGRELATIONSHIP_TYPE_REVERSE_MAP


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


def bugmonitor_update_from_bugnote(*args, **kwargs):
    """
    @author: lig
    """
    bugnote = kwargs.pop('instance')
    bugnote.bug.add_monitor(bugnote.reporter)

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


post_save.connect(bugrelationship_reverse_update, BugRelationship)
post_delete.connect(bugrelationship_reverse_remove, BugRelationship)

post_save.connect(bugmonitor_update_from_bughistory, BugHistory)
post_save.connect(bugmonitor_update_from_bugnote, Bugnote)

post_save.connect(bug_notify_change, BugHistory)
post_save.connect(bug_notify_bugnote, Bugnote)

post_save.connect(bug_assign_to_category_handler, Bug)
