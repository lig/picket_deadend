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

from picketapp.models       import Project
from picketapp              import settings as config

def navi(req):
    
    projects = Project.objects.permited(req.user)
    
    if req.method == 'POST':
        cur_url = req.META['HTTP_REFERER']
    elif req.META.has_key('QUERY_STRING'):
        cur_url = '%s?%s' % (req.path, req.META['QUERY_STRING'])
    else:
        cur_url = '%s?%s'
    
    return {'picket_url': config.BASE_URL, 'site_name': config.SITE_NAME,
        'picket_projects': projects, 'cur_url': cur_url, 'config': config}
