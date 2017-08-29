# -*- coding: utf8 -*-
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static

from netease import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.IndexView.as_view(), name="home"),
    url(r'^detail/(?P<id>\w+)', views.GoodsDetailView.as_view(), name='detail_view'),
    url(r'^category/(?P<category_id>\w+)/(?P<sec_category_id>\w+)',
        views.CategoryListView.as_view(), name='category_view'),
    # 正式环境静态文件走nginx
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
