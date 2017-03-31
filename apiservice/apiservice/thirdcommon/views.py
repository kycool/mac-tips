# -*- coding: utf-8 -*-

import copy
from django.http.response import HttpResponseBase

from rest_framework.response import Response
from rest_framework import viewsets


class CommonViewMixin(object):
    """
    common view mixin which redefine finalize_response function

    not 4xx return result:

    --------------------------------success----------------------------

    return not list

    {
        'error_code': '0',
        'error_message': 'success',
        'result': dict
    }

    return list:

    {
        "count": 3,
        "next": "http://127.0.0.1:8000/api/article/?page=2&size=2",
        "previous": url,
        "error_code": "0",
        "error_message": "success",
        "result": []
    }

    -------------------------------business-error------------------------

    {'error_code': 'xxxx', 'error_message': 'xxxx'}
    or
    {'error_code': 'xxxx', 'error_message': 'xxxx', 'error_data': 'xxxx'}

    """
    success_data = {
        'error_code': '0',
        'error_message': 'success',
    }

    def _build_business_error(self, request, response, *args, **kwargs):
        """rebuild business error data"""
        return response

    def _build_http_error(self, request, response, *args, **kwargs):
        """rebuild http error data"""
        if isinstance(response.data, dict) and 'detail' in response.data:
            response.data = response.data['detail']
        response.data = {
            'error_message': response.data
        }
        return response

    def _build_common(self, request, response, *args, **kwargs):
        """rebuild response data"""
        # validate whether is list by page and size
        if '_list' in response.data:
            response.data.pop('_list')
            response.data.update(self.success_data)
            return response

        data = copy.deepcopy(self.success_data)
        data.update({'result': response.data})
        response.data = data
        return response

    def _patch_response(self, request, response, *args, **kwargs):
        """patch response"""
        if response.status_code >= 400:
            return self._build_http_error(request, response, *args, **kwargs)

        # if error_code in response data which means business error
        if isinstance(response.data, dict) and 'error_code' in response.data:
            return self._build_business_error(request, response, *args, **kwargs)

        # patch success return data which include list and common
        if isinstance(response.data, (dict, list)) and 'error_code' not in response.data:
            return self._build_common(request, response, *args, **kwargs)
        return response

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Returns the final response object.
        """
        # Make the error obvious if a proper response is not returned
        assert isinstance(response, HttpResponseBase), (
            'Expected a `Response`, `HttpResponse` or `HttpStreamingResponse` '
            'to be returned from the view, but received a `%s`'
            % type(response)
        )

        if isinstance(response, Response):
            if not getattr(request, 'accepted_renderer', None):
                neg = self.perform_content_negotiation(request, force=True)
                request.accepted_renderer, request.accepted_media_type = neg

            response.accepted_renderer = request.accepted_renderer
            response.accepted_media_type = request.accepted_media_type
            response.renderer_context = self.get_renderer_context()

        for key, value in self.headers.items():
            response[key] = value

        return self._patch_response(request, response, *args, **kwargs)


class CommonViewSet(CommonViewMixin, viewsets.ModelViewSet):
    """Common ViewSet"""
    pass
