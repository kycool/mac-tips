# -*- coding: utf-8 -*-

# from rest_framework import serializers
from apiservice.thirdcommon.serializers import BaseModelSerializer

from vbblog.models import Category


class CategorySerializer(BaseModelSerializer):
    """docstring for CategorySerializer"""

    class Meta:
        model = Category
        fields = '__all__'
