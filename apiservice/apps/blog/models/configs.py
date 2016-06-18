# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings

from .backbone import BaseBackbone


@python_2_unicode_compatible
class BaseMeta(BaseBackbone):
    key = models.CharField('配置键', max_length=20)
    value = models.CharField('配置值', max_length=100)

    def __str__(self):
        return '{0}-{1}'.format(self.key, self.value)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class UserMeta(BaseMeta):
    """docstring for UserMeta"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return '{0}-{1}'.format(self.key, self.value)

    class Meta:
        verbose_name = '用户元数据'
        verbose_name_plural = '用户元数据'


@python_2_unicode_compatible
class GlobalMeta(BaseMeta):

    def __str__(self):
        return '{0}-{1}'.format(self.key, self.value)

    class Meta:
        verbose_name = '系统元数据'
        verbose_name_plural = '系统元数据'
