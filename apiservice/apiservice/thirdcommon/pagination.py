# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """vue blog result list common pageination"""
    max_page_size = 50
    page_query_param = 'page'
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'result': data,
            '_list': True,
        })
