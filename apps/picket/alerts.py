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

from django.conf import settings
from django.template.loader import render_to_string

from documents import Group

email_users_group = Group.objects.get(name=settings.SMTP_USERS_GROUP)


def send_alerts(bug, recipients, message=None):
    
    if settings.EMAIL_SEND_ALERTS:
        
        from_email = bug.category.mail_addr or None
        alert_subject = '[%s #%s] %s' % (bug.project.name, bug.id,
            bug.summary)
        email_only_alert_message = render_to_string(
            'picket/alert_email_only.eml', {'bug': bug, 'message': message})
        alert_message = render_to_string(
            'picket/alert.eml', {'bug': bug, 'message': message})
        
        for recipient in recipients:
            
            if email_users_group in recipient.groups.all():
                """ Send special alert to email user """
                recipient.email_user(subject=alert_subject,
                    message=email_only_alert_message, from_email=from_email)
            
            elif recipient.email:
                """ Send alert to user only if it exists """
                recipient.email_user(subject=alert_subject,
                    message=alert_message, from_email=from_email)
