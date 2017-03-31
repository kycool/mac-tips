from django.contrib import admin

from .models import UserMeta


@admin.register(UserMeta)
class UserMetaAdmin(admin.ModelAdmin):
    pass
