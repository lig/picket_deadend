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

from django.contrib.auth.models import Group
from django.db.models.signals import post_syncdb

from ..settings import SMTP_USERS_GROUP


def email_user_group_create(app, **kwargs):
    
    if app.__name__ == 'apps.picket.models':
        group, created = Group.objects.get_or_create(name=SMTP_USERS_GROUP)
        
        if created:
            print('Group "%s" for "email" Picket users created.' % group.name)

post_syncdb.connect(email_user_group_create)
