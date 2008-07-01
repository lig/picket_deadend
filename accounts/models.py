"""
Copyright 2008 Serge Matveenko

This file is part of Picket.

Picket is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Picket.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Validator(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user being validating'))
    hash = models.CharField(_('validation hash'), max_length=128, editable=False)
    
    @staticmethod
    def get_hash(username, code):
        import hashlib
        return hashlib.sha224('%s:%s' % (username, code)).hexdigest()
    
    def save(self):
        self.code = User.objects.make_random_password(length=6,
            allowed_chars='1234567890')
        self.username = self.user.username
        unique = False
        while not unique:
            self.hash = Validator.get_hash(self.username, self.code)
            try:
                Validator.objects.get(hash=self.hash)
            except Validator.DoesNotExist:
                unique = True
        super(Validator, self).save()
