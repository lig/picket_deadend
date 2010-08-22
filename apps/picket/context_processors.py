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

from mongoengine.queryset import DoesNotExist

from . import COPYING
from .documents import UserInfo, Project


def picket(request):
    
    if request.user.is_authenticated():
        try:
            user_info = UserInfo.objects.get(id=request.user.id)
        except DoesNotExist:
            user_info = UserInfo()
            user_info.save()
        current_project = user_info.current_project
    else:
        session_project_id = request.session.get('current_project')
        current_project = (Project.objects.get(id=session_project_id) if
            session_project_id else None) 
    
    return {'copying': COPYING, 'current_project': current_project}
