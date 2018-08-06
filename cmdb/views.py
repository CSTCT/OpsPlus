#-*- coding: utf-8 -*-
'''
	Author: Geekwolf
	Blog: http://www.simlinux.com
'''
from django.shortcuts import render,render_to_response,reverse
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from commons.paginator import paginator
import json,logging
from cmdb.models import IDC, ServerAsset, NetworkInterface
from cmdb.forms import IDCForm, ServerAssetForm
from commons.handle import uuid_rm,ip_lists
from django import forms
from django.shortcuts import get_object_or_404,redirect
from cmdb.asset_info import update_assets_info

def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

def idc_list(request):

    data = {}
    idc = IDC.objects.all().order_by('-update_time')
    data = paginator(request, idc)
    request.breadcrumbs((('首页', '/'),('机房管理',reverse('cmdb_idc'))))

    return render(request, 'cmdb/idc/idc.html', {'request': request, 'data': data})

def idc_add(request):

    error = ""
    if request.method == "POST":
        new_name = request.POST.get('name')
        name = IDC.objects.filter(name=new_name)
        form = IDCForm(request.POST)
        if name:
            error = u'该机房记录已存在，请更换名称!'
        else:
            if form.is_valid():
                tmp = form.save(commit=False)
                tmp.save()
                return HttpResponseRedirect(reverse('cmdb_idc'))
    else:
        form = IDCForm()
    request.breadcrumbs((('首页', '/'),('机房管理',reverse('cmdb_idc')),('添加机房',reverse('cmdb_idc_add'))))

    return render(request, 'cmdb/idc/idc_add.html', {'request': request, 'form': form, 'error': error})

def idc_edit(request):

    error = ""
    uuid = uuid_rm(request.GET.get("uuid"))
    if uuid:
        try:
            idc = IDC.objects.select_related().get(uuid=uuid)
            form = IDCForm(instance=idc)
        except:
            error = "不存在"
            form = ""
    if request.method == "POST":
        idc = IDC.objects.select_related().get(uuid=uuid)
        form = IDCForm(request.POST,instance=idc)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.save()
            return HttpResponseRedirect(reverse('cmdb_idc'))
    request.breadcrumbs((('首页', '/'),('机房管理',reverse('cmdb_idc')),('编辑机房',reverse('cmdb_idc_edit'))))

    return render(request, 'cmdb/idc/idc_edit.html', {'request': request, 'form': form, 'uuid': uuid,'error': error})

def idc_del(request):

    uuid = request.GET.get('uuid')
    if uuid:
        IDC.objects.filter(uuid=uuid).delete()
    return HttpResponseRedirect(reverse('cmdb_idc'))


def server_list(request):

    data = {}
    # server = ServerAsset.objects.all().order_by('-update_time')
    server = ServerAsset.objects.raw('SELECT s.uuid,s.hostname,s.status,s.productname,s.cpu_model,s.memory,s.disk,s.os,s.virtual,s.kernel,s.ops_id,s.dev_id,s.minion_status,GROUP_CONCAT(n.address)as ips  from cmdb_serverasset s LEFT JOIN cmdb_networkinterface n on s.uuid = n.server_id GROUP BY s.uuid;')
    data = paginator(request, list(server))
    data['fields'] = ServerAsset._meta.get_fields()
    
    request.breadcrumbs((('首页', '/'),('主机管理',reverse('cmdb_server'))))

    return render(request, 'cmdb/assets/server.html', {'request': request, 'data': data})



def server_add(request):

    error = ""
    if request.method == "POST":
        
        ip_input = request.POST.get('ip').split('\n')
        ips = ip_lists(ip_input)
        uuids = []
        for i in ips:
            data = request.POST.copy()
            data['ip'] = i
            form = ServerAssetForm(data)
            if form.is_valid():
                tmp = form.save(commit=False)
                tmp.save()
                uuids.append(tmp.uuid)
        update_assets_info(request,uuids=uuids,type="server_add")
        return HttpResponseRedirect(reverse('cmdb_server'))
    else:
        form = ServerAssetForm()
    request.breadcrumbs((('首页', '/'),('主机管理',reverse('cmdb_server')),('添加主机',reverse('cmdb_server_add'))))
    return render(request, 'cmdb/assets/server_add.html', {'request': request, 'form': form, 'error': error})


def server_edit(request,uuid):

    error = ""
    server = get_object_or_404(ServerAsset,uuid = uuid)
    form = ServerAssetForm(instance=server)
    if request.method == "POST":
        server = ServerAsset.objects.select_related().get(uuid=uuid)
        form = ServerAssetForm(request.POST,instance=server)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.save()
            return HttpResponseRedirect(reverse('cmdb_server'))
    request.breadcrumbs((('首页', '/'),('主机管理',reverse('cmdb_server')),))
    return render(request, 'cmdb/assets/server_edit.html', {'request': request, 'form': form, 'uuid': uuid,'error': error})



def server_del(request):

    uuid = request.GET.get('uuid')
    uuids = []

    if uuid: 
        uuids = [uuid]
    if request.POST.get('type') == 'bulk_delete':
        print(request.POST.get('type'))
        uuids = [ uuid_rm(i) for i in json.loads(request.POST.get('servers'))]

    NetworkInterface.objects.filter(server__in = uuids).delete()
    ServerAsset.objects.filter(uuid__in = uuids).delete()

    return HttpResponseRedirect(reverse('cmdb_server'))


def server_detail(request,uuid):

    data = {}
    serverasset = get_object_or_404(ServerAsset,uuid = uuid)
    network = NetworkInterface.objects.filter(server=uuid)
    if serverasset:
        data['serverasset'] = serverasset
        # data['serverasset'].disk = eval(serverasset.disk)
        data['request'] = request
        data['network'] = network

    request.breadcrumbs((('首页', '/'),('主机管理',reverse('cmdb_server')),))
    return render_to_response('cmdb/assets/server_detail.html', data)

