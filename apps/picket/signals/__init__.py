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

"""
@todo: bug reminders and notifications mechanism
"""

from django.db.models.signals import post_save, post_delete

from middleware import PicketSignalsMiddleware
from ..models import BugRelationship
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


post_save.connect(bugrelationship_reverse_update, BugRelationship)
post_delete.connect(bugrelationship_reverse_remove, BugRelationship)
