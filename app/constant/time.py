#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast-api-template
@File    ：time.py
@Author  ：Mr.LiuQHui
@Date    ：2023/12/14 5:23 PM
"""
import pytz

ChinaTimeZone = pytz.timezone("Asia/Shanghai")

# 1分钟-毫秒
ONE_MINUTE_MS = 60 * 1000

# 1分钟-秒
ONE_MINUTE = 60

# 5分钟-秒
FIVE_MINUTES = 5 * ONE_MINUTE

# 5分钟-毫秒
FIVE_MINUTES_MS = 5 * ONE_MINUTE_MS
