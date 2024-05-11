#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author sineom
@Date 2024/5/8-15:52
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
import asyncio
from random import random
from typing import Optional

import httpx
from loguru import logger

from app.config import globalAppSettings, globalRedis
from app.constant.redis_key import skill_reply
from app.utils.httpx_schem import HttpxSchema

wx_url = globalAppSettings.wx_url


# 发送文本消息
async def send_txt(txt: str, to_user_name: str, at_users: Optional[str] = None) -> bool:
    """
    发送文本消息
    """
    try:
        # 检查技能是否处理CD期间
        if not globalRedis.trigger_skill(skill_reply):
            return False
        HttpxSchema.post_data(f"{wx_url}/v1/LuaApiCaller?funcname=SendMsg&timeout=10&wxid=wxid_sib20p52764722",
                              json={"ToUserName": to_user_name, "Content": txt, "MsgType": 1,
                                    "AtUsers": at_users or ""})
        return True
    except httpx.HTTPStatusError as e:
        logger.error(f"发送文本消息失败: {e}")
        return False


async def send_img(img: str, to_user_name: str) -> bool:
    """
    发送图片
    :param img:
    :param to_user_name:
    """
    try:
        # 检查技能是否处理CD期间
        if not globalRedis.trigger_skill(skill_reply):
            return False
        HttpxSchema.post_data(
            f"{wx_url}/v1/LuaApiCaller?funcname=SendImage&timeout=10&wxid=wxid_sib20p52764722",
            json={"ToUserName": to_user_name, "ImageUrl": img})
        return True
    except httpx.HTTPStatusError as e:
        e.with_traceback()
        logger.error(f"发送文本消息失败: {e}")
        return False
