"""
@Author sineom
@Date 2024/4/30-14:12
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel

from app.platforms.wx.msg_event import MsgEvent
from app.platforms.wx.msg_type import WXMessageType


class AddMsg(BaseModel):
    MsgId: int
    FromUserName: str
    ToUserName: str
    MsgType: WXMessageType
    Content: str
    Status: int
    ImgStatus: int
    ImgBuf: Any
    CreateTime: int
    MsgSource: str
    PushContent: str
    NewMsgId: int
    NewMsgIdExt: str
    ActionUserName: str
    ActionNickName: str
    Template: str


class Data(BaseModel):
    AddMsg: AddMsg
    EventName: MsgEvent


class CurrentPacket(BaseModel):
    WebConnId: str
    Data: Data


class WXMessage(BaseModel):
    CurrentPacket: CurrentPacket
    CurrentWxid: str
