# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models

from apiservice.thirdcommon.models import BaseBackBone, BaseMeta


class UserMeta(BaseMeta):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return '{0}:{1}:{2}'.format(self.user.name, self.key, self.value)

    class Meta:
        verbose_name = '用户元数据'
        verbose_name_plural = '用户元数据'
