#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  :2020/7/10 19:17
# @Author: xuyongchuan
# @File  : adminx.py

import xadmin

from apps.organizations.models import Teacher, CourseOrg, City


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_filter = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']


class CityAdmin(object):
    list_display = ['id', 'name', 'desc']  # 在列表页显示哪些字段
    search_fields = ['name', 'desc']  # 用来搜索的字段
    list_filter = ['name', 'desc', 'add_time']  # 用来过滤的字段
    list_editable = ['name', 'desc']  # 设置字段可编辑


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)
