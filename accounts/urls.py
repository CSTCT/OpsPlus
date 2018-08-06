# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from accounts import views,api,permissions
urlpatterns = [
	#Login & Logout
    url(r'^login/$', views.login,name='accounts_login'),
    url(r'^logout/$', views.logout,name='accounts_logout'),
    #User Managment
    url(r'^user$', views.accounts_user,name='accounts_user'),
    url(r'^user/add$', views.accounts_add,name='accounts_add'),
    url(r'^user/edit$', views.accounts_edit,name='accounts_edit'),
    url(r'^user/del$', views.accounts_del,name='accounts_del'),

    #Group Managment
    url(r'group$', views.accounts_group, name='accounts_group'),
    url(r'group/update$', views.accounts_group_update, name='accounts_group_update'),
    url(r'group/del$', views.accounts_group_del, name='accounts_group_del'),

    #Idc Search
    url(r'^user/search$', api.user_search,name="user_search"),
    url(r'permission$', permissions.permission, name='accounts_permission'),

]