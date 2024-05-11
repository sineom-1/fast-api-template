"""
@Author sineom
@Date 2024/4/30-14:12
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.platforms.wx.enum.msg_event import MsgEvent
from app.platforms.wx.enum.msg_type import WXMessageType


class MsgInfo(BaseModel):
    MsgId: int = Field(default=None, type=int)
    FromUserName: str = Field(default=None, type=str)
    """来源"""
    ToUserName: str = Field(default=None, type=str)
    """当前用户"""
    MsgType: WXMessageType = Field(default=None, type=WXMessageType)
    """消息类型"""
    Content: str = Field(default=None, type=str)
    """消息内容"""
    Status: int = Field(default=None, type=int)
    """消息状态"""
    ImgStatus: int = Field(default=None, type=int)
    """消息图片状态"""
    ImgBuf: Any = Field(default=None, type=Any)
    """图片二进制"""
    CreateTime: int = Field(default=None, type=int)
    """创建时间"""
    MsgSource: str = Field(default=None, type=str)
    """消息来源"""
    PushContent: str = Field(default=None, type=str)
    """推送内容"""
    NewMsgId: int = Field(default=None, type=int)
    """新消息ID"""
    NewMsgIdExt: str = Field(default=None, type=str)
    """新消息ID扩展"""
    ActionUserName: str = Field(default=None, type=str)
    """消息发送者"""
    ActionNickName: str = Field(default=None, type=str)
    """消息发送者昵称"""
    Template: str = Field(default=None, type=str)
    """消息模板"""


class PacketInfo(BaseModel):
    AddMsg: MsgInfo = Field(default=None, type=MsgInfo)
    """消息"""
    EventName: MsgEvent = Field(default=None, type=MsgEvent)
    """事件"""


class Packet(BaseModel):
    WebConnId: str = Field(default=None, type=str)
    Data: PacketInfo = Field(default=None, type=PacketInfo)


class WXMessage(BaseModel):
    CurrentPacket: Packet = Field(default=None, type=Packet)
    """当前数据包信息"""
    CurrentWxid: str = Field(default=None, type=str)
    """当前用户di"""
