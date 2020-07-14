#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  :2020/7/14 17:30
# @Author: xuyongchuan
# @File  : redis_test.py

import redis

r = redis.Redis(host='localhost', port=6379, db=0, charset='utf8', decode_responses=True)

r.set('mobile', '123')
print(r.get('mobile')) # 这里输出是byte类型的数据，加上charset=uttf8和
r.expire('mobile', 1)
import time
time.sleep(1)
print(r.get('mobile'))