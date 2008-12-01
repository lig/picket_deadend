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

from django.db.models.signals   import pre_save, post_save

from picketapp.models import Bug, BugHistory

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
    
    def bug_pre_save_handler(self, sender, instance, **kwargs):
        old_instance = Bug.objects.get(pk=instance.pk)
        self._bug_cache[old_instance.pk] = old_instance 
    
    def bug_post_save_handler(self, sender, instance, created, **kwargs):
        if created:
            bugHistory = BugHistory(bug=instance, type=0, user=self._req.user)
            bugHistory.save()
            del bugHistory
        else:
            for log_field in ['project_id', 'reporter_id', 'handler_id',
                'duplicate_id', 'priority', 'severity', 'reproducibility',
                'status', 'resolution', 'projection', 'category_id',
                'view_state_id', 'summary', 'sponsorship_total', 'sticky',]:
                old_value = self._bug_cache[instance.pk].__getattribute__(
                    log_field)
                new_value = instance.__getattribute__(log_field)
                if new_value != old_value:
                    bugHistory = BugHistory(bug=instance, type=1,
                        field_name=log_field, old_value=old_value,
                        new_value=new_value, user=self._req.user)
                    bugHistory.save()
                    del bugHistory
            #TODO: handle TextFieldS changes
            #TODO: handle relationship changes
    
    def process_request(self, request):
        self._bug_cache={}
        self._req = request
        pre_save.connect(self.bug_pre_save_handler, Bug)
        post_save.connect(self.bug_post_save_handler, Bug)
        return None
