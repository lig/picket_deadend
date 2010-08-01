# Django settings for wapzap project.

from dist import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    #('Firstname Lastname', 'admin@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, 'local.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SECRET_KEY = ''

#CACHE_BACKEND = 'locmem://'

SERVE_STATIC = False

#FORCE_SCRIPT_NAME = ''
