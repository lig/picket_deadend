"""
Copyright 2008-2010 Serge Matveenko

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
from django.conf.urls.defaults import *
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.static import serve


urlpatterns = patterns('',    
    # main page:
    (r'^$', lambda req: HttpResponseRedirect(reverse('picket-index')), {},
        'index'),
    
    # picket itself
    (r'^picket/', include('apps.picket.urls')),
    
    # logout
    (r'^logout/$', logout, {'next_page': settings.LOGIN_URL}, 'auth-logout'),
)

# static
if settings.SERVE_STATIC:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    )
