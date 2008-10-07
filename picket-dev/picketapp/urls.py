"""
Copyright 2008 Serge Matveenko

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

from django.conf.urls.defaults  import *

urlpatterns = patterns('picketapp.views',
    (r'^$', 'index', {}, 'picket-index',),
    (r'^filebug/$', 'filebug', {}, 'picket-filebug',),
    (r'^bugs/$', 'bugs', {}, 'picket-bugs',),
    (r'^p(?P<projectId>\d+)/$', 'bugs', {}, 'picket-project',),
    (r'^p(?P<projectId>\d+)/c(?P<categoryId>\d+)/$', 'bugs', {},
        'picket-category',),
    (r'^p(?P<projectId>\d+)/c(?P<categoryId>\d+)/b(?P<bugId>\d+)/$',
        'bug', {}, 'picket-bug',),
    (r'^p\d+/c\d+/b(?P<bugId>\d+)/annotate/$',
        'annotate', {}, 'picket-annotate',),
)
