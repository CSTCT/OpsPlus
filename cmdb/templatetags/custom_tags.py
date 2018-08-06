# -*- encoding:utf-8 -*-
from django import template 
from netaddr import IPAddress
from django.template import Context, Template
from django.shortcuts import render
import json

register = template.Library()

@register.filter()  
def strsubst(value):
	return value.replace('\n',', ')


@register.filter()  
def strtodict(value,arg):

	data = eval(value) if value  else ""
	if data and arg != "all":
		return data[arg]
	else: 
		return data

@register.filter()
def ipio(value):

	private = []
	public = []

	if value:
		data = value.split(',')
		for i in data:
			if IPAddress(i).is_private():
				private.append(i)
			else:
				public.append(i)
	if public:
		public = (',').join(public)
	if private:
		private = (',').join(private)

	template = Template("<h5><label class='label label-primary'>内</label>&nbsp;{% if private %}{{private}}{% else %}{% endif %}</h5><h5><label class='label label-default'>外</label>&nbsp;{% if public %}{{public}}{% else %}{% endif %}</h5>")
	context = Context({"public":public,"private":str(private)})
	return template.render(context)

@register.filter()  
def usetostr(value):

	data = []
	for v in value:
		data.append("%s(%s)"%(v.username,v.fullname))

	if data:
		data = (',').join(data)
	return data
	
@register.filter()  
def gsetostr(value):

	data = []
	for v in value:
		data.append(v.name)

	if data:
		data = (',').join(data)
	return data

