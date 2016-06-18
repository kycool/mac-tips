# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from django import forms
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class MembersChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'password', 'is_active', )

    def clean_password(self):
        return self.initial['password']


class UserAdmin(admin.ModelAdmin):
    # form = MembersChangeForm
    list_display = ('id', 'username', 'nick_name',)


admin.site.register(User, UserAdmin)
