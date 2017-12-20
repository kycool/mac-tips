# -*- coding: utf-8 -*-

from django.db import DatabaseError, transaction
from django.db.models.query import QuerySet
from django.db.models import Prefetch

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route

from apiservice.exception.exceptions import BusinessException
from apiservice.thirdcommon.views import GetWithoutPermissionViewSet
from apiservice.thirdcommon.permission import IsVbAdminUser, wrap_permission

from vbblog.models import Article
from .serializers import ArticleSerializer, CreateValidateForm, UpdateValidateForm


class ArticleViewSet(GetWithoutPermissionViewSet):
    """Vue blog article view set"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    create_validate_form = CreateValidateForm

    def get_queryset(self):
        queryset = super(ArticleViewSet, self).get_queryset()

        if isinstance(queryset, QuerySet):
            queryset = queryset.select_related('user', 'category').prefetch_related(Prefetch('article_tag', to_attr='tags'))
        return queryset

    def perform_destroy(self, instance):
        """
        delete specify article

        article many to many tag，the data which in ArticleTagShip should delete
        """
        try:
            with transaction.atomic():
                # delete article
                instance.delete()
                # delete article tag ship
                instance.article_ship.all().delete()
        except DatabaseError:
            raise BusinessException(error_code='41001')

    @wrap_permission(IsVbAdminUser)
    def create(self, request, *args, **kwargs):
        # valiate data
        serializer_validate = self.create_validate_form(data=request.data,
                                                        context={'request': request})
        serializer_validate.is_valid(raise_exception=True)
        instance = self.perform_create(serializer_validate)

        # get create data
        serializer = self.get_serializer(instance=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @wrap_permission(IsVbAdminUser)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_validate = UpdateValidateForm(instance=instance,
                                                 data=request.data,
                                                 partial=partial,
                                                 context={'request': request})
        serializer_validate.is_valid(raise_exception=True)
        instance = self.perform_update(serializer_validate)

        serializer = self.get_serializer(instance=instance)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @detail_route()
    def t1(self, request, *args, **kwargs):
        return Response({'t1': 't1'})
