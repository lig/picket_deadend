# Django settings for wapzap project.

import mongoengine

from dist import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    #('Firstname Lastname', 'admin@example.com'),
)

MANAGERS = ADMINS

mongoengine.connect('picket')

SECRET_KEY = ''

#CACHE_BACKEND = 'locmem://'

SERVE_STATIC = False

#FORCE_SCRIPT_NAME = ''
