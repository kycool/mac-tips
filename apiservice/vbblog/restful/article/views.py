# -*- coding: utf-8 -*-

from django.db import DatabaseError, transaction

from django.db.models.query import QuerySet
from django.db.models import Prefetch

from rest_framework.response import Response
from rest_framework import status

from apiservice.exception.exceptions import BusinessException
from apiservice.thirdcommon.views import CommonViewSet
from vbblog.models import Article

from .serializers import ArticleSerializer, CreateValidateForm


class ArticleViewSet(CommonViewSet):
    """Vue blog article view set"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    create_validate_form = CreateValidateForm

    def get_queryset(self):
        queryset = super(ArticleViewSet, self).get_queryset()

        if isinstance(queryset, QuerySet):
            queryset = queryset.select_related('user', 'category').prefetch_related(Prefetch('article_tag', to_attr='tags'))
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        """
        delete special article

        Note: article many to many tag，the data which in ArticleTagShip should
        delete
        """
        try:
            with transaction.atomic():
                instance.delete()
                instance.article_ship.all().delete()
        except DatabaseError:
            raise BusinessException(error_code='41001')

    def create(self, request, *args, **kwargs):
        # valiate data
        serializer_validate = self.create_validate_form(data=request.data, context={'request': request})
        serializer_validate.is_valid(raise_exception=True)
        instance = self.perform_create()

        # get create data
        serializer = self.get_serializer(instance=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
