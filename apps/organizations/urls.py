#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  :2020/7/16 17:34
# @Author: xuyongchuan
# @File  : urls.py

from django.urls import path
from django.conf.urls import url
from apps.organizations.views import OrgView, AddAskView, OrgHomeView, \
    OrgTeacherView, OrgCourseView, OrgDescView


urlpatterns = [
    url(r'list/$', OrgView.as_view(), name='list'),
    url(r'add_ask/$', AddAskView.as_view(), name='add_ask'),
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='home'),  # 这两种url的设置方式都能满足要求
    # path('<int:org_id>/', OrgHomeView.as_view(), name='home'),
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='home'),  # 这两种url的设置方式都能满足要求
    url(r'^(?P<org_id>\d+)/teacher$', OrgTeacherView.as_view(), name='teachers'),
    url(r'^(?P<org_id>\d+)/course$', OrgCourseView.as_view(), name='courses'),
    url(r'^(?P<org_id>\d+)/desc$', OrgDescView.as_view(), name='desc'),

]
