# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

# from django.core import validators
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser


@python_2_unicode_compatible
class User(AbstractUser):
    nick_name = models.CharField('昵称', max_length=50, blank=True, default='')

    def __str__(self):
        return "{0}".format(self.username)
