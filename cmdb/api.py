#-*- coding: utf-8 -*-
'''
	Author: Geekwolf
	Blog: http://www.simlinux.com
'''
from django.shortcuts import render,render_to_response,reverse
from django.http import HttpResponse,HttpResponseRedirect
from commons.paginator import paginator
from cmdb.models import IDC,ServerAsset
from django.db.models import Q

def idc_search(request):

    data = {}
    search = request.GET.get("search")
    idc = IDC.objects.filter(Q(isp__name__icontains=search) | Q(name__icontains=search) | Q(contact__icontains=search) | Q(network__icontains=search))
    data = paginator(request, idc)
    return render_to_response('cmdb/idc/idc_table.html',data)


def asset_search(request):

    data = {}
    search = request.GET.get("search")
    serverasset = ServerAsset.objects.filter(Q(ip__icontains=search) | Q(hostname__icontains=search) | Q(idc__name__icontains=search) | Q(ops__fullname__icontains=search) | Q(dev__fullname__icontains=search) | Q(salt__name__icontains=search))
    data = paginator(request, serverasset)
    return render_to_response('cmdb/assets/server_table.html',data)