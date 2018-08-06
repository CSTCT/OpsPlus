#-*- coding: utf-8 -*-

from django.conf.urls import url,include
from django.contrib import admin
from cmdb import views as cmdb_views
from accounts import urls
from dashboard import urls
from dashboard import views as dashboard_views
import saltapi

urlpatterns = [
	url(r'^$', dashboard_views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^/dashboard/', include('dashboard.urls')),
    url(r'accounts/', include('accounts.urls')),
    url(r'cmdb/', include('cmdb.urls')),
    url(r'salt/', include('saltapi.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', admin.site.urls),
]



