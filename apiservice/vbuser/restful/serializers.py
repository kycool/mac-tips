# -*- coding: utf-8 -*-

from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """docstring for CategorySerializer"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', )
