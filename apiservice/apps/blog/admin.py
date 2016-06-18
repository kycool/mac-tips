# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib import admin

from .models import Post, Category, UserMeta, GlobalMeta, Tag


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'allow_comment', 'modified', 'created')
    list_display_links = ('author', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(UserMeta)
class UserMetaAdmin(admin.ModelAdmin):
    pass


@admin.register(GlobalMeta)
class GlobalMetaAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
