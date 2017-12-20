# -*- coding: utf-8 -*-

from rest_framework.authentication import SessionAuthentication
from rest_framework import exceptions


def wrap_authentication(*permissions):
    """custom authentication for special route"""
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            self.authentication_classes = permissions
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


class BasicLogin(SessionAuthentication):
    """docstring for HasLogin"""
    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """
        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)
        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            raise exceptions.AuthenticationFailed('No credentials provided')
        self.enforce_csrf(request)

        # CSRF passed with authenticated user
        return (user, None)
