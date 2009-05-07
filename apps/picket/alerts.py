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

from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from settings import *

def send_alerts(bug, recipients, message=None):
    
    if EMAIL_SEND_ALERTS:
        
        site = Site.objects.get_current()
        for recipient in recipients:
            if recipient.email:
                recipient.email_user(
                    subject='[%s #%s] %s' % (site.name, bug.id, bug.summary),
                    message=render_to_string('picket/alert.eml',
                        {'bug': bug, 'message': message}))
