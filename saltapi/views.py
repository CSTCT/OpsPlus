from django.shortcuts import render,reverse,render_to_response,get_object_or_404,HttpResponse
from django.http import HttpResponseRedirect
from saltapi.models import Salt
from saltapi.forms import SaltForm
from commons.paginator import paginator
from commons.handle import uuid_rm,salt_api_status
from cmdb.asset_info import MultiTheads
from commons import saltapi
from saltapi.models import Minions
import collections

def salt_info(request):

    data = {}
    info = Salt.objects.all().order_by('-update_time')
    data = paginator(request, info)
    request.breadcrumbs((('首页', '/'),('Salt管理',reverse('salt_info'))))

    return render(request,'saltapi/salt.html',{'data':data})


def salt_add(request):

    error = ""

    if request.method == "POST":
        new_name = request.POST.get('name')
        name = Salt.objects.filter(name=new_name)
        form = SaltForm(request.POST)
        print(request.body)
        if name:
            error = u'该Salt已存在!'
        else:
            if form.is_valid():
                salt = form.save(commit=False)
                salt.status = salt_api_status(request)
                salt.save()
                return HttpResponseRedirect(reverse('salt_info'))
    else:
        form = SaltForm()

    request.breadcrumbs((('首页', '/'),('Salt管理',reverse('salt_info')),('添加Salt',reverse('salt_add'))))

    return render(request, 'saltapi/salt_add.html', {'request': request, 'form': form, 'error': error})

def salt_edit(request):

    error = ""
    uuid = uuid_rm(request.GET.get("uuid"))
    if uuid:
        try:
            salt = Salt.objects.select_related().get(uuid=uuid)
            form = SaltForm(instance=salt)
        except:
            error = u"不存在"
            form = ""
    if request.method == "POST":
        salt = Salt.objects.select_related().get(uuid=uuid)
        form = SaltForm(request.POST,instance=salt)
        if form.is_valid():
            salt = form.save(commit=False)
            salt.status = salt_api_status(request)
            salt.save()
            return HttpResponseRedirect(reverse('salt_info'))

    request.breadcrumbs((('首页', '/'),('Salt管理',reverse('salt_info')),('编辑Salt',reverse('salt_edit'))))
    return render(request, 'saltapi/salt_edit.html', {'request': request, 'form': form, 'uuid': uuid,'error': error})


def salt_del(request):

    uuid = request.GET.get('uuid')
    if uuid:
        Salt.objects.filter(uuid=uuid).delete()
    return HttpResponseRedirect(reverse('salt_info'))



def update_all_minion_keys(request,**kw):

    salt = Salt.objects.filter(status=1)
    for s in salt:
        sapi = saltapi.SaltClient(s.host,s.username, s.password)
        minions,minions_pre,minions_rej,minions_deny = sapi.list_all_keys()
        for i in minions:
             Minions.objects.update_or_create(minion=i, saltserver=s, status=0)

        for pre in minions_pre:
            Minions.objects.update_or_create(minion=pre, saltserver=s, status=1)


        for rej in minions_rej:
            Minions.objects.update_or_create(minion=rej, saltserver=s, status=2)

        for deny in minions_deny:
            Minions.objects.update_or_create(minion=deny, saltserver=s, status=3)


def get_minion_keys(request):

    saltserver = request.GET.get('saltserver')
    data = collections.defaultdict(lambda: collections.defaultdict(list))
    accept_lists = []
    minions = Minions.objects.filter(saltserver=saltserver).order_by('minion')
    for m in minions:
        if m.status == 0:
            accept_lists.append(m)
        if m.status == 1:
            data['unaccept']['lists'].append(m)
        if m.status == 2:
            data['reject']['lists'].append(m)
        if m.status == 3:
            data['denied']['lists'].append(m)

    data['accept']['count'] = len(accept_lists)
    data['unaccept']['count'] = len(data['unaccept']['lists'])
    data['reject']['count'] = len(data['reject']['lists'])
    data['denied']['count'] = len(data['accept']['lists'])
    data['accept']['lists'] = paginator(request, accept_lists, page_number = 10)
    request.breadcrumbs((('首页', '/'),('Salt管理',reverse('salt_info'))))
    return render(request, 'saltapi/salt_keys.html', {'request': request,'data': data, 'saltserver': saltserver})

def minion_status(request):

    if request.method == 'POST':
        minion_match = request.POST.get('minion')
        status = int(request.POST.get('status'))
        print(minion_match,status)
        minion = get_object_or_404(Minions, minion = minion_match)
        minion.status = status
        minion.save()
        sapi = saltapi.SaltClient(minion.saltserver.host,minion.saltserver.username, minion.saltserver.password)

        if status == 0:
            sapi.accept_key(minion_match)
        #默认saltmaster自动添加key,删除key后依然会自动添加
        elif status == 1:
            sapi.delete_key(minion_match)
        elif status == 2:
            sapi.reject_key(minion_match)

        return HttpResponse('ok')




