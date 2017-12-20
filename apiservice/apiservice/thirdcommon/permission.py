# -*- coding: utf-8 -*-

from functools import update_wrapper

from rest_framework.permissions import IsAdminUser


class IsVbAdminUser(IsAdminUser):
    """
    Allows access only to admin users.
    """
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return self.has_permission(request, view)


def wrap_permission(*permissions, validate_permission=True):
    """custom permissions for special route"""
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            self.permission_classes = permissions
            if validate_permission:
                self.check_permissions(request)
            return func(self, request, *args, **kwargs)
        return update_wrapper(wrapper, func)
    return decorator
