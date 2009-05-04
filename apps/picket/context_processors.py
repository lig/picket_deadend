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

import settings as config
from . import COPYING
from models import Project


def picket(request):
    
    projects = list(Project.objects.get_permited(request.user))
    
    try:
        cur_project = Project.objects.get_permited(request.user).get(
            pk=request.session.get('project_id', 0))
    except Project.DoesNotExist:
        cur_project = None

    if request.method == 'POST':
        cur_url = request.META['HTTP_REFERER']
    elif 'QUERY_STRING' in request.META:
        cur_url = '%s?%s' % (request.path, request.META['QUERY_STRING'])
    else:
        cur_url = request.path

    legend = []
    for (k, v) in config.BUG_STATUS_CHOICES:
        legend.append((v, config.BUG_STATUS_COLORS[k]))
        
    return { 'picket_projects': projects, 'cur_project': cur_project,
        'cur_url': cur_url, 'config': config, 'COPYING': COPYING,
        'legend': legend }
