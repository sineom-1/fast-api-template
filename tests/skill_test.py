#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author sineom
@Date 2024/5/10-18:27
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
import time

import redis
import threading

# 连接到Redis服务器
r = redis.Redis(host='localhost', port=6379, db=0, username="", password="123456")

# 技能A的冷却时间（以秒为单位）
COOLDOWN_TIME = 10


def trigger_skill_a(skill_name: str) -> bool:
    """
    触发技能A的函数
    :param skill_name: 技能名称
    """
    # 技能A的冷却时间键
    skill_key = f'{skill_name}:cooldown'
    # 用户请求的键
    user_request_key = f'{skill_name}:request'

    # 使用Redis事务来保证原子性
    with r.pipeline() as pipe:
        # 检查技能是否处于冷却时间
        pipe.exists(skill_key)
        # 设置用户请求的键，如果技能不在冷却时间内
        pipe.set(user_request_key, 1, nx=True, ex=10000)
        # 执行事务
        results = pipe.execute()
        # 如果技能不在冷却时间内，并且用户请求的键设置成功
        return not results[0] and results[1]
        # if not results[0] and results[1]:
        #     print(f"User {user_id} triggered skill A successfully!")
        #     # 模拟技能处理时间
        #     time.sleep(1)
        #     # 技能处理完成后，删除用户请求的键
        #     r.delete(user_request_key)
        # else:
        #     print(f"User {user_id} failed to trigger skill A due to cooldown.")
