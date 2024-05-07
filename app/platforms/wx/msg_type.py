"""
@Author sineom
@Date 2024/4/29-11:05
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
from enum import Enum


class WXMessageType(Enum):
    Text = 1
    """文本消息"""
    Image = 3
    """图片消息"""
    Audio = 34
    """语音消息"""
    Emoji = 47
    """表情消息"""
    Location = 48
    """位置消息"""
    Video = 43
    """视频消息"""
    Init = 51
    """初始化消息"""
    SystemNotification = 9999
    """系统通知"""
    SystemMessage = 10000
    """系统消息"""
    RecallMessage = 10002
    """撤回消息"""
    Quote = 49
    """引用消息"""
    GroupInvitation = 2
    """群邀请"""


class ChatType(Enum):
    Group = 2
    """群聊"""
    Friend = 1
    """单聊"""
