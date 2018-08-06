# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from cmdb import views,api,asset_info

urlpatterns = [
    url(r'^idc$', views.idc_list,name='cmdb_idc'),
    url(r'^idc/add$', views.idc_add,name='cmdb_idc_add'),
    url(r'^idc/edit$', views.idc_edit,name='cmdb_idc_edit'),
    url(r'^idc/del$', views.idc_del,name='cmdb_idc_del'),

    #IDC Search
    url(r'^idc/search$', api.idc_search,name='idc_search'),
    #Server Search
    url(r'^asset/search$', api.asset_search,name='asset_search'),

    #Server Assets
    url(r'^server$', views.server_list, name='cmdb_server'),
    url(r'^server/add$', views.server_add, name='cmdb_server_add'),
    url(r'^server/detail/(?P<uuid>[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?)$', views.server_detail, name='cmdb_server_detail'),
    url(r'^server/edit/(?P<uuid>[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?)$', views.server_edit, name='cmdb_server_edit'),
    url(r'^server/del$', views.server_del, name='cmdb_server_del'),

    #更新主机
    url(r'^update$', asset_info.update_assets_info, name='cmdb_server_update'),
    url(r'^export$', asset_info.export_assets_info, name='cmdb_server_export'),
]