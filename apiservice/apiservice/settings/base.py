# -*- coding: utf-8 -*-

from .source import *

# Application extend define
VUEBLOG_SELF_APPS = [
    'vbdummy',
    'vbblog',
    'vbuser',
]

VUEBLOG_THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
]

INSTALLED_APPS += VUEBLOG_SELF_APPS + VUEBLOG_THIRD_PARTY_APPS


REST_FRAMEWORK = {
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER': 'apiservice.exception.handler.business_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'apiservice.thirdcommon.pagination.StandardPagination',
    'PAGE_SIZE': 10,
}

# cors origin access config
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8080',
    '127.0.0.1:8081'
)

CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'POST',
    'PUT',
)
