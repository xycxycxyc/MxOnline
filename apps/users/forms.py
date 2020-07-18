#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  :2020/7/12 0:05
# @Author: xuyongchuan
# @File  : forms.py
# 登录时的表单验证
from django import forms
from captcha.fields import CaptchaField
import redis
from MxOnline.settings import  REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile


class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True, )

    def clean_mobile(self):
        mobile = self.data.get('mobile')
        # 验证手机号码是否已注册
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError('该手机号已注册')
        return mobile
    # 选择一个字段进行验证，一般用于返回出错的字段信息
    # clean_《字段名》函数是先于clean函数执行的，，因此，在clean_字段名函数中，clean_data不存在，因此要使用data取原始数据

    def clean_code(self):
        mobile = self.data.get('mobile')
        code = self.data.get('code')

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError('验证码不正确')
        return code


class LoginForm(forms.Form):
    # 其中username和password要与前端html中表单的input的name保持一致
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    # 选择一个字段进行验证，一般用于返回出错的字段信息
    # clean_《字段名》函数是先于clean函数执行的，，因此，在clean_字段名函数中，clean_data不存在，因此要使用data取原始数据
    def clean_code(self):
        mobile = self.data.get('mobile')
        code = self.data.get('code')

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data


    # def clean(self):  # 这个方法验证所有字段是否都正确，否则is_valid方法返回False
    #     mobile = self.cleaned_data['mobile']
    #     code = self.cleaned_data['code']
    #
    #     r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
    #     redis_code = r.get(str(mobile))
    #     if code != redis_code:
    #         raise forms.ValidationError('验证码不正确')
    #     return self.cleaned_data
