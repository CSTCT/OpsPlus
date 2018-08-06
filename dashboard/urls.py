#-*- coding: utf-8 -*-

from django.conf.urls import url,include
from django.contrib import admin
from dashboard import views

urlpatterns = [
    url(r'^$', views.index),
]
