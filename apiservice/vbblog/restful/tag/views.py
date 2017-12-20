# -*- coding: utf-8 -*-

from apiservice.thirdcommon.views import GetWithoutPermissionViewSet
from vbblog.models import Tag

from .serializers import TagSerializer


class TagViewSet(GetWithoutPermissionViewSet):
    """Vue blog tag view set"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
