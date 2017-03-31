# -*- coding: utf-8 -*-

from django.db import models
from apiservice.utils.uuid import UUIDTools

class BaseBackBone(models.Model):
    """base backbone"""
    id = models.CharField(primary_key=True, default=UUIDTools.uuid1_hex, editable=False, max_length=32)

    class Meta:
        abstract = True


class BaseMeta(BaseBackBone):
    """base meta"""
    key = models.CharField('配置键', max_length=20)
    value = models.CharField('配置值', max_length=50)

    class Meta:
        abstract = True
