"""
@Author sineom
@Date 2024/4/30-14:17
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SaveMsg(BaseModel):
    FromUserName: str
    """消息来自哪里，私聊可以取ActionNickName，群聊需要先获取群资料，然后赋值群昵称"""
    ToUserName: str
    """消息发送到哪里"""
    Content: str
    """消息内容"""
    ActionUserName: Optional[str] = None
    """消息操作人名"""
    ActionNickName: Optional[str] = None
    """当前发言的用户昵称"""

    CreateTime: int = int(datetime.now().timestamp())
    """消息时间"""
