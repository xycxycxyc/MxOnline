#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  :2020/7/17 14:53
# @Author: xuyongchuan
# @File  : forms.py

import re
from django import forms
from apps.opreations.models import UserAsk


class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(max_length=11, min_length=11, required=True)

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean(self):
        '''
        验证手机号码是否合法
        :return:
        '''
        mobile = self.cleaned_data['mobile']
        regex_mobile = r"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')

