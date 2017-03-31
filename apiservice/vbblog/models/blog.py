# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models

from apiservice.thirdcommon.models import BaseBackBone


class Category(BaseBackBone):
    """category"""
    name = models.CharField('名称', max_length=30)
    created = models.DateTimeField('生成时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = '分类列表'


class Article(BaseBackBone):
    """article"""

    STATUS = (
        (0, 'draft'),
        (1, 'published'),
        (2, 'deleted'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_article')
    category = models.ForeignKey(Category, related_name='category_article', null=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    content = models.TextField()
    allow_comment = models.BooleanField('允许评论', default=True)
    status = models.IntegerField('状态', choices=STATUS, blank=True, default=0)
    updated = models.DateTimeField('更新时间', auto_now=True)
    created = models.DateTimeField('生成时间', auto_now_add=True)
    read = models.PositiveIntegerField('阅览量', blank=False, default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章列表'


class Tag(BaseBackBone):
    name = models.CharField('名称', max_length=50)
    article = models.ManyToManyField(Article, through='ArticleTagShip', through_fields=('tag', 'article'), related_name='article_tag')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = '标签列表'


class ArticleTagShip(BaseBackBone):
    article = models.ForeignKey(Article, related_name='article_ship')
    tag = models.ForeignKey(Tag, related_name='tag_ship')

    def __str__(self):
        return 'ArticleTagShip'

    class Meta:
        verbose_name = '文章标签映射'
        verbose_name_plural = '文章标签映射'
