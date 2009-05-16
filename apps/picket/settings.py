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

from django.utils.translation import ugettext as _

__all__ = ['PROJECT_STATUS_CHOICES', 'PROJECT_STATUS_CHOICES_DEFAULT',
    'PRIORITY_CHOICES', 'PRIORITY_CHOICES_DEFAULT', 'PRIORITY_ICONS',
    'SEVERITY_CHOICES', 'SEVERITY_CHOICES_DEFAULT', 'REPRODUCIBILITY_CHOICES',
    'REPRODUCIBILITY_CHOICES_DEFAULT', 'BUG_STATUS_CHOICES',
    'BUG_STATUS_CHOICES_DEFAULT', 'BUG_STATUS_COLORS',
    'BUG_RESOLVED_STATUS_THRESHOLD', 'RESOLUTION_CHOICES',
    'RESOLUTION_CHOICES_DEFAULT', 'BUG_REOPEN_STATUS',
    'BUGRELATIONSHIP_TYPE_CHOICES', 'BUGRELATIONSHIP_TYPE_DEFAULT',
    'BUGRELATIONSHIP_TYPE_REVERSE_MAP', 'PROJECTION_CHOICES',
    'PROJECTION_CHOICES_DEFAULT', 'ETA_CHOICES', 'ETA_CHOICES_DEFAULT',
    'ACCESS_LEVELS_CHOICES', 'ACCESS_LEVELS_CHOICES_DEFAULT',
    'COLUMNS_BUGS_VIEW', 'EMAIL_SEND_ALERTS', 'RIGHTS', 'INTEGRATION_ENABLED',
    'INTEGRATION_PROJECT_VIEW', 'USE_JAVASCRIPT', 'SHOW_PROJECT_MENU_BAR',
    'SHOW_VERSION', 'SHOW_LEGEND']

PROJECT_STATUS_CHOICES = (
    (10, _('development'),),
    (30, _('release'),),
    (50, _('stable'),),
    (70, _('obsolete'),),
)

PROJECT_STATUS_CHOICES_DEFAULT = 10


PRIORITY_CHOICES = (
    (10, _('none'),),
    (20, _('low'),),
    (30, _('normal'),),
    (40, _('high'),),
    (50, _('urgent'),),
    (60, _('immediate'),),
)

PRIORITY_CHOICES_DEFAULT = 30

PRIORITY_ICONS = {
                10: '/media/images/priority_low_3.gif',
                20: '/media/images/priority_low_2.gif',
                30: '/media/images/priority_low_1.gif',
                40: '/media/images/priority_1.gif',
                50: '/media/images/priority_2.gif',
                60: '/media/images/priority_3.gif',
}


SEVERITY_CHOICES = (
    (10, _('feature'),),
    (20, _('trivial'),),
    (30, _('text'),),
    (40, _('tweak'),),
    (50, _('minor'),),
    (60, _('major'),),
    (70, _('crash'),),
    (80, _('block'),),
)

SEVERITY_CHOICES_DEFAULT = 50


REPRODUCIBILITY_CHOICES = (
    (10, _('always'),),
    (30, _('sometimes'),),
    (50, _('random'),),
    (70, _('have not tried'),),
    (90, _('unable to duplicate'),),
    (100, _('N/A'),),
)

REPRODUCIBILITY_CHOICES_DEFAULT = 70


BUG_STATUS_CHOICES = (
    (10, _('new'),),
    (20, _('feedback'),),
    (30, _('acknowledged'),),
    (40, _('confirmed'),),
    (50, _('assigned'),),
    (80, _('resolved'),),
    (90, _('closed'),),
)

BUG_STATUS_CHOICES_DEFAULT = 10

BUG_STATUS_COLORS = {
    10: '#ffa0a0', # red
    20: '#ff50a8', # purple
    30: '#ffd850', # orange
    40: '#ffffb0', # yellow
    50: '#c8c8ff', # blue
    80: '#cceedd', # buish-green
    90: '#e8e8e8', # light gray
}


BUG_RESOLVED_STATUS_THRESHOLD = 80

RESOLUTION_CHOICES = (
    (10, _('open'),),
    (20, _('fixed'),),
    (30, _('reopened'),),
    (40, _('unable to duplicate'),),
    (50, _('not fixable'),),
    (60, _('duplicate'),),
    (70, _('not a bug'),),
    (80, _('suspended'),),
    (90, _('wont fix'),),
)

RESOLUTION_CHOICES_DEFAULT = 10


""" Status to assign to the bug when reopened. """
BUG_REOPEN_STATUS = 20; # 20: feedback


BUGRELATIONSHIP_TYPE_CHOICES = (
    (1,_('related to'),),
    (2,_('parent of'),),
    (3,_('child of'),),
    (0,_('duplicate of'),),
    (4,_('has duplicate'),),
)

BUGRELATIONSHIP_TYPE_DEFAULT = 3 # 3: child of

BUGRELATIONSHIP_TYPE_REVERSE_MAP = {
    1: 1,
    2: 3,
    3: 2,
    0: 4,
    4: 0,
}

PROJECTION_CHOICES = (
    (10, _('none'),),
    (30, _('tweak'),),
    (50, _('minor fix'),),
    (70, _('major rework'),),
    (90, _('redesign'),),
)

PROJECTION_CHOICES_DEFAULT = 10


ETA_CHOICES = (
    (10, _('none'),),
    (20, _('< 1 day'),),
    (30, _('2-3 days'),),
    (40, _('< 1 week'),),
    (50, _('< 1 month'),),
    (60, _('> 1 month'),),
)

ETA_CHOICES_DEFAULT = 10


""" @note: not used. scopes used instead yet. """
ACCESS_LEVELS_CHOICES = (
    (10, _('viewer'),),
    (25, _('reporter'),),
    (40, _('updater'),),
    (55, _('developer'),),
    (70, _('manager'),),
    (90, _('administrator'),),
)

ACCESS_LEVELS_CHOICES_DEFAULT = 10


COLUMNS_BUGS_VIEW = (
    ('priority', _('P'),),
    ('id', _('ID'),),
    ('sponsorship_total', _('$'),),
    ('num_bugnotes', _('#'),),
    ('category', _('Category'),),
    ('severity', _('Severity'),),
    ('status', _('Status'),),
    ('last_updated', _('Updated'),),
    ('summary', _('Summary'),),
)

""" behaviour settings """
EMAIL_SEND_ALERTS = True

""" access rights lists. every string is a list of the possible rights """
RIGHTS = (
    ('r', 'Read'),
    ('rw', 'Read/Write'),
    #('rwd', 'Read/Write/Delete'),
    #('w', 'Write only'),
)


"""
Is Picket integrated as app. Work as standalone project in other case.
This MUST be implemented in case of integration:
 * Template named 'base.html' must exist and contain 'content' block.
 * contrib.auth.models.User.get_absolute_url method MUST return valid url
 * View named 'users-add' MUST exist and allow somebody usually superuser to
     add users.
 * View named 'user-edit' MUST exist and accept 'user' parameter as
     contrib.auth.models.User.pk value.
 * View named 'user-password' MUST exist and accept 'user' parameter as
     contrib.auth.models.User.pk value.
 * INTEGRATION_PROJECT_VIEW MAY contain name of the view to show for project.
     This view MUST accept 'mantis_project' keyword argument as
     picket.models.Project.pk value.
"""
INTEGRATION_ENABLED = False
INTEGRATION_PROJECT_VIEW = False

""" settings inherited from Mantis """
USE_JAVASCRIPT = True
SHOW_PROJECT_MENU_BAR = True
SHOW_VERSION = True
SHOW_LEGEND = True
