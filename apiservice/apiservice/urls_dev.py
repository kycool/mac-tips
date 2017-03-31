# -*- coding: utf-8 -*-

from django.conf.urls import url, include

# django debug toolbar
import debug_toolbar

# django rest framework swagger api
from rest_framework_swagger.views import get_swagger_view

from .urls import urlpatterns


schema_view = get_swagger_view(title='VBlog API')

urlpatterns += [
    url(r'^docs/', schema_view),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
