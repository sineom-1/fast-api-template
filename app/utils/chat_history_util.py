"""
@Author sineom
@Date 2024/4/30-13:55
@Email h.sineom@gmail.com
@description  聊天记录的工具类
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
import os
import time

from app.config import globalAppSettings
from app.platforms.wx.model.save_msg import SaveMsg


class ChatHistoryUtil(object):

    # 根据今日的日期生成writeFile的路径 yyyy/MM/dd/接收人id.txt, 如果文件不存在则创建
    @staticmethod
    def get_chat_history_file_path(to_user: str) -> str:
        import datetime
        now = datetime.datetime.now()
        # 保存的文件夹路径
        dir_path = os.path.join(globalAppSettings.wx_msg_path, now.strftime("%Y/%m/%d"))
        file_path = os.path.join(dir_path, f"{to_user}.txt")
        # 如果文件夹不存在则创建
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        return file_path

    # 保存聊天记录到文件
    @staticmethod
    def save_msg(chat_msg: SaveMsg):
        file_path = ChatHistoryUtil.get_chat_history_file_path(chat_msg.FromUserName)
        # 将时间格式化为 HH:mm
        chat_time = time.localtime(chat_msg.CreateTime)
        time_str = time.strftime("%H:%M", chat_time)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"{chat_msg.ActionNickName}({time_str}): {chat_msg.Content}\n")
