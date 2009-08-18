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

from django.db import models


class ScopeManager(models.Manager):

    def get_permited(self, user):

        if user.is_superuser:
            return self.all()
        else:
            q = models.Q(anonymous_access=True)

            if not user.is_anonymous():
                q |= models.Q(groups__user=user)

            return self.filter(q)


class ProjectManager(models.Manager):
    def get_permited(self, user):
        if user.is_superuser:
            return self.all()
        else:
            return self.filter(scope__in=Scope.objects.get_permited(user))


class BugManager(models.Manager):

    def permited(self, user, project=None, category=None):

        if user.is_superuser:
            bugs = self.select_related()
        else:
            bugs = self.select_related().filter(
                scope__in=Scope.objects.get_permited(user),
                project__in=Project.objects.get_permited(user))

        bugs = bugs.filter(project=project) if project is not None else bugs
        bugs = bugs.filter(category=category) if category is not None else bugs

        return bugs


class BugMonitorManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(mute=False)


class PicketUserManager(models.Manager):
    def have_permissions(self, permissions, scope):
        rights_q = reduce(lambda q1, q2: q1 | q2,
            map(lambda char: models.Q(
                    groups__scopegroup__rights__contains=char),
                permissions))
        return self.filter(rights_q, groups__scope=scope)
