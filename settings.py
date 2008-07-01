"""
Copyright 2008 Serge Matveenko

This file is part of Picket.

Picket is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Picket.  If not, see <http://www.gnu.org/licenses/>.
"""

# Django settings for picket project.

import _settings as s

DEBUG = s.DEBUG
TEMPLATE_DEBUG = s.TEMPLATE_DEBUG

ADMINS = s.ADMINS

MANAGERS = s.MANAGERS

DATABASE_ENGINE = s.DATABASE_ENGINE           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = s.DATABASE_NAME             # Or path to database file if using sqlite3.
DATABASE_USER = s.DATABASE_USER             # Not used with sqlite3.
DATABASE_PASSWORD = s.DATABASE_PASSWORD         # Not used with sqlite3.
DATABASE_HOST = s.DATABASE_HOST             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = s.DATABASE_PORT             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = s.TIME_ZONE

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = s.LANGUAGE_CODE

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = s.MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = s.MEDIA_URL

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = s.ADMIN_MEDIA_PREFIX

# Make this unique, and don't share it with anybody.
SECRET_KEY = s.SECRET_KEY

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = s.TEMPLATE_DIRS

INSTALLED_APPS = (
    #picket
    'accounts',
    'picketapp',
    'users',
    #development
    'django_evolution',
    #django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    #picket
    'picketapp.context_processors.navi',
    #django
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
)

AUTH_PROFILE_MODULE = s.AUTH_PROFILE_MODULE
