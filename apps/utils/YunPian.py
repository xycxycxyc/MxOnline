#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  :2020/7/12 21:10
# @Author: xuyongchuan
# @File  : YunPian.py

import requests
import json


def send_single_sms(api_key, code, mobile):
    # 发送单条短信
    url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    text = '【许永川网站测试】您的验证码是:{}'.format(code)
    # 返回的是一个httpresponse对象，因此通过json转换为json对象返回
    res = requests.post(url, data={
        'apikey': api_key,
        'mobile': mobile,
        'text': text,
    })
    re_json = json.loads(res.text)
    return re_json


if __name__ == '__main__':
    res = send_single_sms('9dbdd48d97fdd6f90efd63023220d4e5', '12334', '15767205227')
    import json
    res_json = json.loads(res.text)
    code = res_json['code']
    msg = res_json['msg']
    if code == 0:
        print('发送成功')
    else:
        print('发送失败:{}'.format(msg))
    print(res.text)
