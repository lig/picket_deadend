"""
Copyright 2010 Serge Matveenko

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

from mongoengine import ValidationError

from documents import Project


class PicketMiddleware(object):
    
    def process_request(self, request):
        
        # set project
        if 'set_project' in request.GET:
            request.session['current_project'] = request.GET['set_project']
        
        # attach project object to request
        current_project_id = request.session.get('current_project')
        # current_project_id could be None for all projects
        current_project = (current_project_id and
            Project.objects.with_id(current_project_id))
        # current_project could be None after lookup
        request.project = current_project
