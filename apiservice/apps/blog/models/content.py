# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings

from .backbone import BaseBackbone


@python_2_unicode_compatible
class Category(BaseBackbone):
    name = models.CharField('名称', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = '分类列表'


@python_2_unicode_compatible
class Post(BaseBackbone):
    """post"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.ForeignKey(Category, null=True)
    draft = models.BooleanField('草稿', default=False)
    allow_comment = models.BooleanField('允许评论', default=True)
    modified = models.DateTimeField('更新时间', auto_now=True)
    created = models.DateTimeField('生成时间', auto_now_add=True)
    read = models.PositiveIntegerField('阅览量', blank=False, default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章列表'


@python_2_unicode_compatible
class Tag(BaseBackbone):
    name = models.CharField('名称', max_length=50)
    articles = models.ManyToManyField(Post, through='PostTagShip')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = '标签列表'


@python_2_unicode_compatible
class PostTagShip(BaseBackbone):
    post = models.ForeignKey(Post)
    tag = models.ForeignKey(Tag)

    def __str__(self):
        return 'PostTagShip'
