# -*- coding: utf-8 -*-

from rest_framework import routers

from .tag import views as tag_views
from .article import views as article_views

router = routers.SimpleRouter()
router.register(r'tag', tag_views.TagViewSet)
router.register(r'article', article_views.ArticleViewSet)
urlpatterns = router.urls
