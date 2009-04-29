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

from django.contrib import admin

from models import (Bug, BugFile, BugHistory, BugMonitor, Bugnote,
                    BugRelationship, Category, Project, ProjectFile,
                    ProjectUserList, Scope, ScopeGroup)


class BugFileInline(admin.StackedInline):
    model = BugFile
    extra = 1

class BugHistoryInline(admin.TabularInline):
    model = BugHistory
    extra = 0

class BugMonitorInline(admin.TabularInline):
    model = BugMonitor
    extra = 1

class BugnoteInline(admin.StackedInline):
    model = Bugnote
    extra = 1

class BugRelationshipInline(admin.TabularInline):
    model = BugRelationship
    fk_name = 'source_bug'
    extra = 1

class BugAdmin(admin.ModelAdmin):
    inlines = [
        BugFileInline,
        BugRelationshipInline,
        BugMonitorInline,
        BugnoteInline,
        BugHistoryInline,
    ]
admin.site.register(Bug, BugAdmin)

admin.site.register(Category)

class ProjectFileInline(admin.StackedInline):
    model = ProjectFile
    extra = 1

class ProjectUserListInline(admin.TabularInline):
    model = ProjectUserList
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ProjectFileInline,
        ProjectUserListInline,
    ]
admin.site.register(Project, ProjectAdmin)

class ScopeGroupInline(admin.TabularInline):
    model = ScopeGroup
    extra = 1

class ScopeAdmin(admin.ModelAdmin):
    inlines = [
        ScopeGroupInline,
    ]
admin.site.register(Scope, ScopeAdmin)

