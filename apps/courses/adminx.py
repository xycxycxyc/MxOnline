#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  :2020/7/10 19:17
# @Author: xuyongchuan
# @File  : adminx.py

import xadmin

from apps.courses.models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']  # 在列表页显示哪些字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']  # 用来搜索的字段
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']  # 用来过滤的字段
    list_editable = ['degree', 'desc']  # 设置字段可编辑


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
