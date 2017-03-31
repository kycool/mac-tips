from django.contrib import admin

from .models import (
    Article, Category,
    SystemMeta, Tag, ArticleTagShip,
)


@admin.register(SystemMeta)
class SystemMetaAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'allow_comment', 'updated', 'created')
    list_display_links = ('user', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(ArticleTagShip)
class ArticleTagShipAdmin(admin.ModelAdmin):
    pass
