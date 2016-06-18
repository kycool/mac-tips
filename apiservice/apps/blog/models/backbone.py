# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from django.utils.encoding import python_2_unicode_compatible
from django.db import models

from utils import uuid4_hex


@python_2_unicode_compatible
class BaseBackbone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4_hex, editable=False)

    def __str__(self):
        return self.id

    class Meta:
        abstract = True
