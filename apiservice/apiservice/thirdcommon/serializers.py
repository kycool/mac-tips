# -*- coding: utf-8 -*-

import calendar
from collections import OrderedDict

from django.db import models

from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject


class BaseModelSerializer(serializers.ModelSerializer):
    """
    rewrite serializers ModelSerializer to_representation
    """

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.

        代码片段 1：

        elif isinstance(attribute, models.Manager):
            data = attribute.all()
            ret[field.field_name] = field.to_representation(data)

        A: 例如获取文章所拥有的标签， 使用方法不使用 Prefetch

        queryset = queryset.select_related('user', 'category').prefetch_related('article_tag')

        这里属性 article_tag 其实是 <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager at 0x10fa2df28>

        isinstance(u1.article_tag, models.Manager) is True

        如果不重写 serializer 的 to_representation 的方法，那么需要在业务逻辑中，

        赋值单篇文章所拥有的标签
        instance.tags = instance.article_tag.all()

        或者

        for item in queryset:
            # 迭代赋值单篇文章所拥有的标签
            item.tags = item.article_tag.all()

        这样不符合 DRY 原则，特别是多处是这样的场景的情况

        B: 例如获取文章所拥有的标签， 使用方法不使用 Prefetch

        queryset = queryset.select_related('user', 'category').prefetch_related(Prefetch('article_tag', to_attr='tags'))

        这里属性 tags 其实是 [<Tag: tag1>, <Tag: world>, <Tag: tag3>]

        注意分析使用 Prefetch('article_tag', to_attr='tags') 和 不使用的区别

        --------------------------------------------------------------------
        代码片段 2：

        elif hasattr(attribute, 'isoformat'):
            ret[field.field_name] = calendar.timegm(attribute.utctimetuple())

        这里是把 datetime 对象字符串转换为时间戳

        如果不转，显示的格式为："created": "2017-03-24T07:55:53.480951Z"
        转换已后，显示的格式为："created": 1490342153
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            elif isinstance(attribute, models.Manager):
                data = attribute.all()
                ret[field.field_name] = field.to_representation(data)
            elif hasattr(attribute, 'isoformat'):
                ret[field.field_name] = calendar.timegm(attribute.utctimetuple())
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret
