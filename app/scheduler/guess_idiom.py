#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author sineom
@Date 2024/5/7-14:49
@Email h.sineom@gmail.com
@description  看图猜成语
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
import asyncio
import datetime
from random import random
from typing import Optional, Union, Tuple

import httpx
from loguru import logger

from app.config import globalRedis
from app.constant import FIVE_MINUTES, FIVE_MINUTES_MS
from app.constant.redis_key import idiom_user, skill_guess_idiom
from app.platforms.wx.wx_chat import send_img
from app.types.response.idiom_source import IdiomSource, IdiomPage


class GuessIdiom:
    @classmethod
    async def generate_idiom(cls, id: str) -> Union[Tuple[str, str], None]:
        """
        成语图片和答案
        :param id: 唯一标志符
        :return: 元组 (图片 URL, 答案) 或者 None
        """
        try:
            response = httpx.get(f"https://xiaoapi.cn/API/game_ktccy.php?msg=开始游戏&id={id}")
            if response.status_code == 200:
                result = response.json()
                if result["code"] == 200:
                    data = result["data"]
                    # 如果成功，返回一个包含图片 URL 和答案的元组
                    return data["pic"], data["answer"]
                else:
                    # 如果 API 返回错误码，返回错误信息
                    return result["msg"]
            else:
                # 如果 HTTP 状态码不是 200，返回适当的错误消息
                logger.error(f"成语生成 API HTTP 错误: 状态码 {response.status_code}")
        except httpx.RequestError as e:
            e.with_traceback()
            # 如果请求过程中出现异常，返回异常信息
            logger.error(f"成语生成 API 请求错误: {str(e)}")

    # 成语出处的说明

    @classmethod
    async def get_idiom_source(cls, idiom: str) -> Optional[IdiomSource]:
        """
        成语出处
        :param idiom: 成语
        :param to_user: 接收者
        :return: 成语出处
        """
        try:
            response = httpx.get(
                f"https://apis.tianapi.com/chengyu/index?key=0612b4c5690c8d7c2f5b2f99295aec8f&word={idiom}")
            response.raise_for_status()  # 检查HTTP请求是否成功，若不成功则抛出异常
            result = response.json()
            if result["code"] == 200:
                page_info = IdiomPage.parse_obj(result["result"])
                if page_info.allnum > 0:
                    result = IdiomSource.parse_obj(page_info.list[0])
                    result.fanli = result.fanli.replace("～", idiom)
                    return result
                else:
                    return None
            else:
                logger.error(f"成语出处 API 返回错误: {result['msg']}")
                return None  # 返回错误消息，若不存在则返回默认消息
        except httpx.RequestError as e:
            logger.error("成语出处 API 请求错误", str(e))  # 记录请求错误日志
            return None

    @classmethod
    async def guess_idiom(cls, to_user_name: str = "39253891795@chatroom"):
        """
        猜成语， 可配置对哪些对象支持
        """
        # 检查技能是否处理CD期间
        if not globalRedis.trigger_skill(skill_guess_idiom, ex=FIVE_MINUTES_MS):
            logger.debug("猜成语技能冷却中")
            return
        logger.debug("猜成语开启")
        _id = str(datetime.datetime.now().timestamp())
        img_url, answer = await cls.generate_idiom(_id)
        # 发送图片
        if await send_img(img_url, to_user_name):
            # 将答案存入redis中 key为id value为答案 5分钟过期
            # 哪个用户开启了
            globalRedis.set(idiom_user % to_user_name, to_user_name, expire=FIVE_MINUTES)
            # 答案存入redis中
            globalRedis.set(answer, to_user_name, expire=FIVE_MINUTES)
        logger.info(f"猜成语 {answer}")
