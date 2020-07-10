#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  :2020/7/10 19:17
# @Author: xuyongchuan
# @File  : adminx.py

import xadmin

from apps.courses.models import Course, Lesson, Video, CourseResource


# 设置xadmin的全局信息，在任意一个app的adminx.py中都可以
class GlobalSettings(object):
    site_title = '慕学后台管理系统'
    site_footer = '慕学在线网'
    # menu_style = 'accordion'  # 设置models表的下拉菜单


# 设置xadmin的主题功能
class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']  # 在列表页显示哪些字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']  # 用来搜索的字段
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']  # 用来过滤的字段
    list_editable = ['degree', 'desc']  # 设置字段可编辑


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    # 过滤的时候course是一个外键，我们希望在course的name字段上过滤，就可以采用course__name的形式（双下划线)
    list_filter = ['course__name', 'name', 'add_time']


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

# 注册xadmin的全局设置
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
