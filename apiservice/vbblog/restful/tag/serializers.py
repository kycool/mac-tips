# -*- coding: utf-8 -*-

from rest_framework import serializers
from apiservice.thirdcommon.serializers import BaseModelSerializer

from vbblog.models import Tag


class TagSimpleSerializer(serializers.ModelSerializer):
    """tag onclude show id and name"""

    class Meta:
        model = Tag
        fields = ('id', 'name')


class TagSerializer(BaseModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
