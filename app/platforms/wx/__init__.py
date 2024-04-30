"""
@Author sineom
@Date 2024/4/29-11:01
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
from app.config import globalAppSettings
from app.platforms.wx.wx_bot import connect_wx_bot


def wx_init():
    connect_wx_bot(globalAppSettings.socket_url)
