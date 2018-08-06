# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from saltapi import views
urlpatterns = [
    url(r'^$', views.salt_info,name='salt_info'),
    url(r'^add$', views.salt_add,name='salt_add'),
    url(r'^edit$', views.salt_edit,name='salt_edit'),
    url(r'^del$', views.salt_del, name='salt_del'),
    url(r'^update/keys',views.update_all_minion_keys, name='update_all_minion_keys'),
    url(r'^get/keys', views.get_minion_keys, name='get_minion_keys'),
    url(r'^minion/status', views.minion_status, name='minion_status')
]