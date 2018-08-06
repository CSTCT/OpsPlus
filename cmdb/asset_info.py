#-*- coding: utf-8 -*-
'''
    Author: Geekwolf
    Blog: http://www.simlinux.com
'''
from django.shortcuts import render,render_to_response,reverse
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from commons.paginator import paginator
import json,logging
from cmdb.models import ServerAsset, NetworkInterface
from cmdb.forms import ServerAssetForm
from django.db.models import Q
from commons.handle import uuid_rm
from django.shortcuts import get_object_or_404,redirect
from commons.saltapi import SaltClient
from saltapi.models import Salt
import threadpool,time,re,tablib,collections
from io import BytesIO
from cmdb.templatetags.custom_tags import strtodict
import sys
print(sys.getfilesystemencoding())

logger = logging.getLogger('info')


def GetInfo(r, arg):
    try:
        arg = r[arg]
    except:
        arg = ''
    return arg


def GetInfoDict(r, arg):
    try:
        result = ''
        for k in r[arg]:
            result = result + k + ': ' + str(r[arg][k]) + '\n'
    except:
        result = ''
    return result
def GetDiskSize(r):
    if r > 1000:
        r = r/1000
        s = str('%.2f'%r) + 'G'
        if r > 1000:
            r = r/1000.0
            s = ('%.2f'%r) + 'T'
    else:
        s = str('%.2f'%r) + 'M'
    return s


def MultiTheads(server_lists):

    global asset_info
    asset_info = []
    start_time = time.time()
    pool = threadpool.ThreadPool(10) 
    requests = threadpool.makeRequests(GetServerInfo, server_lists) 
    [pool.putRequest(req) for req in requests] 
    pool.wait() 
    print('%d second'% (time.time()-start_time))

    return asset_info 


def GetServerInfo(server):
    '''
    Salt API获取主机信息并进行格式化输出
    '''
    global asset_info
    info = {}

    sapi = SaltClient(server[1], server[2], server[3])
    ret = sapi.remote_server_info(server[0], 'grains.items')
    info['hostname']=GetInfo(ret,'fqdn')
    info['sn']=GetInfo(ret,'serialnumber')

    info['ip']=server[0]
    info['os']=GetInfo(ret,'lsb_distrib_description')
    info['os']= info['os'] if info['os'] else GetInfo(ret,'lsb_distrib_codename') 
    info['manufacturer']=GetInfo(ret,'manufacturer')
    info['cpu_model']=GetInfo(ret,'cpu_model')
    info['productname']=GetInfo(ret,'productname')
    info['cpu_nums']=GetInfo(ret,'num_cpus')
    info['kernel'] = GetInfo(ret,'kernel') + GetInfo(ret,'kernelrelease')
    info['zmqversion'] = GetInfo(ret,'zmqversion')
    info['shell'] = GetInfo(ret,'shell')
    info['saltversion'] = GetInfo(ret,'saltversion')
    info['locale'] = GetInfoDict(ret, 'locale_info')
    info['selinux'] = GetInfoDict(ret, 'selinux')

    if 'virtual_subtype' in ret:
        virtual = GetInfo(ret,'virtual') + '-' + GetInfo(ret,'virtual_subtype')
    else:
        virtual=GetInfo(ret,'virtual')
    info['virtual'] = virtual

    try:
        hwaddr = ret['hwaddr_interfaces']
        ipaddr = ret['ip4_interfaces']

        hwaddr.pop('lo')
        ipaddr.pop('lo')

        info['network'] = []

        for i in ipaddr:
            ip = ''
            for j in ipaddr[i]:
                info['network'].append({"name": i, "address": j, "mac": hwaddr[i]})
    except:
        info['network'] = 'Nan'


    mem=GetInfo(ret,'mem_total')
    if mem > 1000:
        mem = int(mem)/1000.0
        memory = ('%.1f'%mem) + 'G'
    else:
        memory = str(mem) + 'M'
    info['memory'] = memory

    ret = sapi.remote_server_info(server[0], 'disk.usage')


    info['disk'] = {}
    total = 0

    for i in ret:
        r = int(ret[i]['1K-blocks'])/1000
        total = total + r
        key = ret[i]['filesystem']
        info['disk'][key] = [i,GetDiskSize(r)]
    info['disk']['total'] = GetDiskSize(total)
    _tmp = sorted(info['disk'].items(), key=lambda item:item[0])

    info['disk'] = {}
    for k,v in _tmp:
        info['disk'][k] = v

    asset_info.append(info)



def update_assets_info(request,**kw):

    '''
    通过Salt更新主机配置
    '''
    if kw:
        type = kw['type']
        uuids = kw['uuids']
    else:    
        type = request.POST.get('type')

    if type == "bulk_update":
        uuids = [ uuid_rm(i) for i in json.loads(request.POST.get('servers'))]
        ServerAssets = ServerAsset.objects.select_related().filter(uuid__in = uuids)
    elif type == "server_add":
        ServerAssets = ServerAsset.objects.select_related().filter(uuid__in = uuids)
    else:
        ServerAssets = ServerAsset.objects.select_related().filter(~Q(salt__isnull = True))

    # ServerAssets = ServerAsset.objects.select_related().filter(~Q(salt__isnull = True),Q(status__in = [0,1,4,5]),Q(salt__status = 1 ))
    
    if ServerAssets:
        server_lists = []
        output_ips = []
        [server_lists.append([i.ip,i.salt.host,i.salt.username,i.salt.password]) for i in ServerAssets]
        ret = MultiTheads(server_lists)
        for i in ret:
            try:
                server_asset = get_object_or_404(ServerAsset, ip=i['ip'])                
                for j in i:
                    if i[j] != 'Nan':
                        setattr(server_asset, j, i[j])
            except:
                server_asset = ServerAsset()
                for j in i:
                    setattr(server_asset, j, i[j])

            setattr(server_asset,'minion_status',1)
            server_asset.save()

            interface_name = []
            for j in i['network']:
                obj, created = NetworkInterface.objects.update_or_create(name = j['name'], address = j['address'], mac = j['mac'], server = server_asset,)
                interface_name.append(j['name'])
            # 批量更新
            # NetworkInterface.objects.bulk_create(nlist)
            NetworkInterface.objects.filter(~Q(name__in = interface_name),Q(server=server_asset)).delete()
            output_ips.append(i['ip'])
        
        input_ips = [ i[0] for i in server_lists]
        remain_ips = list(set(input_ips).difference(set(output_ips)))
        ServerAsset.objects.filter(Q(ip__in = remain_ips)).update(minion_status = 2)
    else:
            logger.warning('ServerAssets为空!')
    return redirect('cmdb_server')


def export_assets_info(request):

 
    _filename = u"服务器资产信息"  
    filename = _filename.encode('utf-8').decode('unicode-escape')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename + '.xls'
    
    # uuids = [ uuid_rm(i) for i in json.loads(request.POST.get('servers'))]
    ServerAssets = ServerAsset.objects.select_related().all()
    NetworkInterfaces = NetworkInterface.objects.select_related().all()

    headers = ('主机名','内网地址','外网地址','操作系统','所属机房','运营状态','运维负责人','开发负责人','产品型号','硬件配置','序列号','Salt版本')
    data = []
    network = []

    network = collections.defaultdict(lambda: collections.defaultdict(list))

    r = '192\.168(\.([2][0-4]\d|[2][5][0-5]|[01]?\d?\d)){2}|^(\D)*10(\.([2][0-4]\d|[2][5][0-5]|[01]?\d?\d)){3}|172\.([1][6-9]|[2]\d|3[01])(\.([2][0-4]\d|[2][5][0-5]|[01]?\d?\d)){2}'

    for i in NetworkInterfaces:
        if re.findall(r, i.address):
            network[i.server.uuid]['in'].append(i.address)
        else:
            network[i.server.uuid]['out'].append(i.address)

    for s in ServerAssets:

        in_ip = (',').join(network[s.uuid]['in'])
        out_ip = (',').join(network[s.uuid]['out'])
        hardware = "%s/%s核/内存%s/磁盘%s"%(s.cpu_model,s.cpu_nums,s.memory,strtodict(s.disk,'total'))
        data.append((s.hostname,in_ip,out_ip,s.os,s.idc.name,s.get_status_display(),str(s.ops),str(s.dev),s.productname,hardware,s.sn,s.saltversion))

    data = tablib.Dataset(*data, headers=headers, title=_filename)
    data.fields_width = (100, 199, 100)
    output=BytesIO()  

    output.write(data.xls)
    response.write(output.getvalue())

    return  response  


