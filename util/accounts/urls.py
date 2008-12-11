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
from django.http                import HttpResponseRedirect

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login', {}, 'login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {}, 'logout'),
    (r'^registration/$', 'util.accounts.views.registration', {}, 'signup'),
    (r'^validation/$', 'util.accounts.views.validation', {}, 'validate'),
    (r'^registration/password/$', 'util.accounts.views.make_password', {},
        'make-password'),
    (r'^profile/$',
        lambda req: HttpResponseRedirect(req.user.get_absolute_url())),
)
