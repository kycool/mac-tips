# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models

from apiservice.thirdcommon.models import BaseBackBone, BaseMeta


class SystemMeta(BaseMeta):
    """system meta"""

    def __str__(self):
        return '{0}:{1}'.format(self.key, self.value)

    class Meta:
        verbose_name = '系统元数据'
        verbose_name_plural = '系统元数据'