"""
Copyright 2008 Serge Matveenko, Alexey Smirnov

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

from django.db.models.signals import post_init, post_save

from apps.picket.models import Bug, BugHistory

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

class PicketSignalsMiddleware(object):
    
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
        if created:
            bugHistory = BugHistory(bug=instance, type=0, user=self._req.user)
            bugHistory.save()
            del bugHistory
        else:
            """
            @todo: handle TextFieldS changes
            @todo: handle relationship changes
            """
            print self._bug_cache[instance.pk].priority
            print instance.priority
            for log_field in ['project_id', 'reporter_id', 'handler_id',
                'duplicate_id', 'priority', 'severity', 'reproducibility',
                'status', 'resolution', 'projection', 'category_id',
                'scope_id', 'summary', 'sponsorship_total', 'sticky',]:
                old_value = self._bug_cache[instance.pk].__getattribute__(
                    log_field)
                new_value = instance.__getattribute__(log_field)
                if new_value != old_value:
                    bugHistory = BugHistory(bug=instance, type=1,
                        field_name=log_field, old_value=old_value,
                        new_value=new_value, user=self._req.user)
                    bugHistory.save()
                    del bugHistory
        self._bug_cache[instance.pk] = instance
    
    def process_request(self, request):
        self._bug_cache={}
        self._req = request
        post_init.connect(self.bug_post_init_handler, Bug)
        post_save.connect(self.bug_post_save_handler, Bug)
        return None

