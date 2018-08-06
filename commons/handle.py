#-*- coding: utf-8 -*-
'''
    Author: Geekwolf
    Blog: http://www.simlinux.com
'''
from commons.saltapi import SaltClient
import datetime,time
from dateutil.relativedelta import relativedelta


def uuid_rm(str):
	return ('').join(str.split('-'))

def salt_api_status(request):
	
    salt_host = request.POST.get('host')
    salt_username = request.POST.get('username')
    salt_password = request.POST.get('password')
    salt= SaltClient(salt_host,salt_username,salt_password)
    status = 1 if salt.get_token() else 0
    return status

def ip_range(start_ip,end_ip):



    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ips = []
   
    ips.append(start_ip)
    while temp != end:
       start[3] += 1
       for i in (3, 2, 1):
          if temp[i] == 256:
             temp[i] = 0
             temp[i-1] += 1
       ips.append(".".join(map(str, temp)))    
      
    return ips

def ip_lists(ip_input):

    ip_lists = []

    for i in ip_input:
        if i.find('-') != -1:
            start_ip = i.split('-')[0]
            end_ip = i.split('-')[1]
            ip_lists = ip_lists + ip_range(start_ip, end_ip)
        else:
            ip_lists.append(i)
    return ip_lists

def list_to_in(objectids):

    return  ','.join(map(str, objectids))

def get_month_day():
    
    return datetime.date.today() - relativedelta(months=+1)

def timestamp_to_time(timestamp):

    timestamp = int(timestamp)
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    return dt

def time_delta(timestamp):

    nowstamp = int(time.time())
    oldtime = int(timestamp)

    timestamp = nowstamp - oldtime
    td = str(timestamp // 86400) + '天' +str(timestamp % 86400// 3600) + '时' + str(timestamp % 3600 // 60) + '分'
    
    return td