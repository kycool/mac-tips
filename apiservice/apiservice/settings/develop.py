from .base import *

AUTH_PASSWORD_VALIDATORS = []

INSTALLED_APPS += [
    'rest_framework_swagger',
    'django_extensions',
    'django_nose',
]

SHELL_PLUS_PRINT_SQL = True

# rewrite root urlconf
ROOT_URLCONF = 'apiservice.urls_dev'
