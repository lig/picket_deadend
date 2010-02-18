"""
Copyright 2008-2009 Serge Matveenko, Alexey Smirnov

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

from signals import BugHistoryHandler


class PicketSignalsMiddleware(object):
    
    def process_request(self, request):
        self.handler = BugHistoryHandler(request.user)
        return None
    
    def process_response(self, request, response):
        del self.handler
        return response
