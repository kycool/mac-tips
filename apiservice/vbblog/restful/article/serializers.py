# -*- coding: utf-8 -*-

from django.db import DatabaseError, transaction

from rest_framework import serializers

from apiservice.exception.exceptions import BusinessException
from apiservice.thirdcommon.serializers import BaseModelSerializer

from vbblog.models import Article, Category, Tag, ArticleTagShip

from ..tag import serializers as tag
from ..category import serializers as category
from vbuser.restful import serializers as user


class ArticleSerializer(BaseModelSerializer):
    """article data serializer"""
    tags = tag.TagSimpleSerializer(many=True)
    category = category.CategorySerializer()
    user = user.UserSerializer()

    class Meta:
        model = Article
        fields = '__all__'


class CreateValidateForm(serializers.Serializer):
    """create article validate form"""
    title = serializers.CharField(min_length=2, max_length=20)
    description = serializers.CharField(max_length=100)
    content = serializers.CharField(min_length=1)
    category = serializers.UUIDField(format='hex')
    allow_comment = serializers.BooleanField(required=False)
    status = serializers.ChoiceField(choices=[0, 1, 2])
    tags = serializers.ListField(child=serializers.UUIDField(format='hex'), required=False)

    def validate(self, attrs):
        category_queryset = Category.objects.filter(pk=attrs.get('category').hex)
        if not category_queryset.exists():
            raise BusinessException(error_code='40001')

        tags = attrs.get('tags')
        if tags:
            tags = [item.hex for item in tags]
            tag_queryset = Tag.objects.filter(id__in=tags)

            if tag_queryset.count() != len(tags):
                raise BusinessException(error_code='40201')
            attrs['tags'] = tag_queryset

        attrs['category'] = category_queryset.first()
        attrs['user'] = self.context.get('request').user
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                tags = validated_data.pop('tags', [])
                instance = Article.objects.create(**validated_data)
                if tags:
                    article_tag_ships = [ArticleTagShip(article=instance, tag=item) for item in tags]
                    ArticleTagShip.objects.bulk_create(article_tag_ships)
                instance.tags = instance.article_tag.all()
                return instance
        except DatabaseError:
            raise BusinessException(error_code='41001')


class UpdateValidateForm(serializers.Serializer):
    """create article validate form"""
    title = serializers.CharField(min_length=2, max_length=20)
    description = serializers.CharField(max_length=100)
    content = serializers.CharField(min_length=1)
    category = serializers.UUIDField(format='hex')
    allow_comment = serializers.BooleanField(required=False)
    status = serializers.ChoiceField(choices=[0, 1, 2])
    tags = serializers.ListField(child=serializers.UUIDField(format='hex'), required=False)

    def validate(self, attrs):
        category_queryset = Category.objects.filter(pk=attrs.get('category').hex)
        if not category_queryset.exists():
            raise BusinessException(error_code='40001')

        tags = attrs.get('tags')
        if tags:
            tags = [item.hex for item in tags]
            tag_queryset = Tag.objects.filter(id__in=tags)

            if tag_queryset.count() != len(tags):
                raise BusinessException(error_code='40201')
            attrs['tags'] = tag_queryset

        attrs['category'] = category_queryset.first()
        attrs['user'] = self.context.get('request').user
        return attrs

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                tags = validated_data.pop('tags', [])

                for key, value in validated_data.items():
                    setattr(instance, key, value)
                instance.save()
                instance.article_ship.all().delete()
                if tags:
                    article_tag_ships = [ArticleTagShip(article=instance, tag=item) for item in tags]
                    ArticleTagShip.objects.bulk_create(article_tag_ships)
                instance.tags = instance.article_tag.all()
                return instance
        except DatabaseError:
            raise BusinessException(error_code='41001')
