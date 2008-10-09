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

import os

from django.conf                import settings
from django.conf.urls.defaults  import *
from django.contrib             import admin
from django.core.urlresolvers   import reverse
from django.http                import HttpResponseRedirect
from django.template            import RequestContext

from picketapp.settings import BASE_URL

## django admin
admin.autodiscover()

urlpatterns = patterns('',
    
    ## main page:
    (r'^$', lambda req: HttpResponseRedirect(reverse('picket-index')), {}, 'index'),
    
    ## picket itself
    (r'^picket/', include('picketapp.urls')),

    ## picket util
    (r'^accounts/', include('accounts.urls')),
    (r'^users/', include('users.urls')),

    ## django admin
    (r'^admin/(.*)', admin.site.root),
    
    ## testing
    (r'^i/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PATH_TO_PICKET, 'i'),}),
    (r'^m/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PATH_TO_PICKET, 'm'),}),
)
