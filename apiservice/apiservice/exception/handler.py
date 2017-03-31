# -*- coding: utf-8 -*-

from django.http import HttpResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.compat import set_rollback
from rest_framework.views import exception_handler

from .exceptions import BusinessException


def error_response(code, message, data=None, http_response=False):
    response_data = {'error_code': code, 'error_message': message}

    if data is not None:
        response_data['error_data'] = data

    if http_response:
        return HttpResponse(JSONRenderer().render(response_data),
                            content_type='application/json')
    return Response(response_data)


def business_exception_handler(exc, context):
    if isinstance(exc, BusinessException):
        set_rollback()
        if getattr(exc, 'error_data', ''):
            response = error_response(exc.error_code,
                                      exc.error_message,
                                      exc.error_data)
        else:
            response = error_response(exc.error_code, exc.error_message)
    else:
        response = exception_handler(exc, context)
    return response
