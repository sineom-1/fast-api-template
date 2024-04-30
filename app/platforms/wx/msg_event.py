"""
@Author sineom
@Date 2024/4/30-15:53
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
from enum import Enum


class MsgEvent(Enum):
    ON_EVENT_MSG_NEW = "ON_EVENT_MSG_NEW"
    """新消息"""
    ON_EVENT_PAT_MSG = "ON_EVENT_PAT_MSG"
    """拍一拍消息"""
