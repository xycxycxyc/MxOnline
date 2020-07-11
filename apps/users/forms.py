#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  :2020/7/12 0:05
# @Author: xuyongchuan
# @File  : forms.py
# 登录时的表单验证
from django import forms


class LoginForm(forms.Form):
    # 其中username和password要与前端html中表单的input的name保持一致
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)