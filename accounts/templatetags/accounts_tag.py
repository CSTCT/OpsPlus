# -*- coding: utf-8 -*-
# @Author: Geekwolf
# @Date:   2018-07-20 16:51:11
# @Last Modified by:   Geekwolf
# @Last Modified time: 2018-07-20 16:51:22

from django import template

register = template.Library()


@register.filter()
def usetostr(value):

    data = []
    for v in value:
        data.append("%s(%s)" % (v.username, v.fullname))

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


@register.filter
def get_at_index(list, index):
    return list[index]


@register.filter
def report_item_count(value):
    count = 0
    for k, v in value.items():
        count += len(v)
    print(count)
    return count
