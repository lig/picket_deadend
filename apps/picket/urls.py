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

from django.conf.urls.defaults  import *

"""
@todo: project view with project summary not administration

@todo: make urls includable with any picket app path
"""
urlpatterns = patterns('apps.picket.views',
    
    ## index
    (r'^$', 'index', {},
        'picket-index',),
    
    ## reports
    (r'^filebug/$', 'filebug', {},
        'picket-filebug',),
    (r'^clonebug/(?P<clone_id>\d+)/$', 'filebug', {'clone': True,},
        'picket-filebug-clone',),
    
    ## project
    (r'^project(?P<project_id>\d+)/$', 'project', {},
        'picket-project',),
    
    ## bugs lists
    (r'^bugs/$', 'bugs', {},
        'picket-bugs',),
    (r'^bugs/sort/(?P<sort_field>\w+)/(?P<sort_dir>(ASC|DESC))/$', 'bugs', {},
        'picket-bugs-ordered',),
    (r'^bugs/c(?P<category_id>\d+)/$', 'bugs', {},
        'picket-category',),
    
    ## bug view
    (r'^bug/(?P<bug_id>\d+)/$', 'bug', {},
        'picket-bug',),
    
    ## bug update
    (r'^bug/(?P<bug_id>\d+)/update/$', 'update', {},
        'picket-bug-update',),
    
    ## bug fields updates
    (r'^bug/(?P<bug_id>\d+)/update_handler/$', 'update_field',
        {'form_class': 'AssignForm',},
        'picket-bug-update-handler',),
    (r'^bug/(?P<bug_id>\d+)/update_status/$', 'update_field',
        {'form_class': 'StatusForm',},
        'picket-bug-update-status',),
    (r'^bug/(?P<bug_id>\d+)/move/$', 'update_field',
        {'form_class': 'BugMoveForm',},
        'picket-bug-move',),
    
    ## various bug operations
    (r'^bug/(?P<bug_id>\d+)/monitor/$', 'update_monitor', {'mute': False,},
        'picket-bug-monitor',),
    (r'^bug/(?P<bug_id>\d+)/mute/$', 'update_monitor', {'mute': True,},
        'picket-bug-mute',),
    (r'^bug/(?P<bug_id>\d+)/delete/$', 'delete', {},
        'picket-bug-delete',),
    (r'^bug/(?P<bug_id>\d+)/annotate/$', 'annotate', {},
        'picket-annotate',),
    
    ## relationships operations
    (r'^bug/(?P<bug_id>\d+)/add_rel/$', 'add_relationship', {},
        'picket-bug-relationship-add'),
    (r'^relationship/(?P<bug_relationship_id>\d+)/delete/$',
        'delete_relationship', {},
        'picket-bug-relationship-delete'),
    
    ## file upload
    (r'^bug/(?P<bug_id>\d+)/upload/$', 'bug_file_upload', {},
        'picket-bugfile-upload'),
    
    ## active project selections
    (r'^choose_project/next/(?P<view_name>[\w-]+)/$', 'choose_project', {},
        'picket-choose-project-gonext'),
    (r'^choose_project/$', 'choose_project', {},
        'picket-choose-project'),
    (r'^set_project/next/(?P<view_name>[\w-]+)/$', 'set_project', {},
        'picket-set-project-gonext'),
    (r'^set_project/$', 'set_project', {},
        'picket-set-project'),
    
    ## jump to bug by id
    (r'^jump/$', 'jump_to_bug', {},
        'picket-jump-to-bug'),
    
    ## special views
    (r'^my/$', 'my', {},
        'picket-my-view',),
    (r'^changelog/$', 'changelog', {},
        'picket-changelog'),
    (r'^roadmap/$', 'roadmap', {},
        'picket-roadmap'),
    
    ## picket administration
    (r'^admin/', include('apps.picket.admin.urls')),
)
