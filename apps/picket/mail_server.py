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

import email
import re
from smtpd import SMTPServer

from django.contrib.auth.models import User

from models import Category, Bug, Bugnote
from signals import BugHistoryHandler

""" typical subject is: '(re|fw): [site.name #bug.id] bug.summary' """
subject_regex = re.compile(r'\[.* #(?P<bug_id>\d+)\] .*$')

OK = None


class PicketServer(SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        """
        peer is a tuple containing (ipaddr, port) of the client that made the
        socket connection to our smtp port.

        mailfrom is the raw address the client claims the message is coming
        from.

        rcpttos is a list of raw addresses the client wishes to deliver the
        message to.

        data is a string containing the entire full text of the message,
        headers (if supplied) and all.  It has been `de-transparencied'
        according to RFC 821, Section 4.5.2.  In other words, a line
        containing a `.' followed by other text has had the leading dot
        removed.

        This function should return None, for a normal `250 Ok' response;
        otherwise it returns the desired response string in RFC 821 format.

        Picket mail processing algorithm:
          1. Find category via rcpttos or drop message
          2. Try to find user for mailfrom or create new one
          2. Try to find bug to post reply or assume new bug
            In case of reply (even bug moved to other category) create bugnote
              with text from message body
            In case of new bug create new bug with summary from mail subject
              and text from message body
          3. Create bugfiles from attachments
        """

        """
            HACK aka crutch
            Reopen database connection in current thread.
            We close it, and django open it again in current thread.
        """
        from django.db import connection
        connection.close()

        """ find all categories mail sent to """
        categories = Category.objects.filter(mail_addr__in=rcpttos)

        """ do anything if there is any categories only """
        if categories.count() > 0:

            """ find or create user for mailfrom """
            try:
                user = User.objects.get(email=mailfrom)
            except User.DoesNotExist:
                username = mailfrom.split('@', 1)[0] + \
                    str(User.objects.all().order_by('-id')[0].id + 1)
                user = User.objects.create_user(username, mailfrom)
            
            """ connect history handler """
            bugHistoryHandler = BugHistoryHandler(user)
            
            """ make message object """
            message = email.message_from_string(data)

            """ try to find bug """
            subject_parsed = subject_regex.search(message['subject']) \
                if 'subject' in message else ''
            if subject_parsed:
                bug_id = subject_parsed.group('bug_id')
                if bug_id:
                    try:
                        bug = Bug.objects.get(id=bug_id)
                    except:
                        """ if bug not found will create new one """
                        pass
                    else:
                        """ we have reply here """
                        try:
                            Bugnote.from_message(bug, user, message).save()
                        except Exception, e:
                            result = '451 %s' % e
                        else:
                            result = OK
            
            """ bug wasn't found thus we creating new one """
            try:
                Bug.from_message(categories[0], user, message).save()
            except Exception, e:
                result = '451 %s' % e
            else:
                result = OK
        
        else:
            """ go away silently if there is nothing to do """
            result = OK
        
        if 'bugHistoryHandler' in locals():
            del bugHistoryHandler
        
        return result
