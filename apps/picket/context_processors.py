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
from apps.picket            import COPYING
from apps.picket.models     import Project
from apps.picket            import settings as config

def navi(req):
    
    projects = list(Project.objects.permited(req.user))
    
    if req.method == 'POST':
        cur_url = req.META['HTTP_REFERER']
    elif 'QUERY_STRING' in req.META:
        cur_url = '%s?%s' % (req.path, req.META['QUERY_STRING'])
    else:
        cur_url = req.path
    
    return {'picket_projects': projects, 'cur_url': cur_url, 'config': config,
        'COPYING': COPYING,}
