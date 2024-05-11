import asyncio
import json

import websocket
from loguru import logger

from app.config import globalRedis, globalAppSettings, wx_commands, admin_ids
from app.constant.redis_key import idiom_user, open_reply_group, reply_mode, open_summary_group
from app.platforms.wx.model.message import WXMessage, MsgInfo
from app.platforms.wx.model.save_msg import SaveMsg
from app.platforms.wx.enum.msg_type import WXMessageType
from app.platforms.wx.wx_chat import send_txt
from app.scheduler.guess_idiom import GuessIdiom
from app.utils.chat_history_util import ChatHistoryUtil

socket_server = None


def on_message(_, message):
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(parse_msg(message))
    finally:
        loop.close()


async def parse_msg(message):
    data = json.loads(message, strict=False)
    data = WXMessage(**data)
    msg_info = data.CurrentPacket.Data.AddMsg
    if not msg_info.FromUserName.endswith("@chatroom"):
        # 私聊暂不处理
        return

    if is_command(msg_info):
        await dispatch_command(msg_info)
    else:
        # 是否开启了回复
        if not globalRedis.get(open_reply_group % msg_info.FromUserName):
            # 当前群未开启回复
            return
        # 回复


# 开始保存聊天记录
async def save_msg(msg_info: MsgInfo):
    if msg_info.MsgType == WXMessageType.Text:
        # 文本消息
        if globalRedis.get(open_summary_group % msg_info.FromUserName):
            save_msg = SaveMsg(
                **{k: v for k, v in msg_info.dict().items() if k in SaveMsg.__fields__})
            ChatHistoryUtil.save_msg(save_msg)


async def dispatch_command(msg_info: MsgInfo):
    if msg_info.MsgType == WXMessageType.Text:
        # 指令的分发
        if msg_info.Content == globalAppSettings.skill_idiom:
            # 看图猜成语
            await check_idiom(msg_info)
            if msg_info.PushContent.endswith("@了你"):
                if msg_info.Content.endswith("看图猜成语"):
                    await GuessIdiom.guess_idiom(to_user_name=msg_info.FromUserName)
        elif msg_info.Content == globalAppSettings.skill_open:
            # 开启指令
            # 1. 将群id添加到redis中
            admin_ids.append(msg_info.FromUserName)
            globalRedis.set(open_reply_group % msg_info.FromUserName, msg_info.FromUserName)
        elif msg_info.Content == globalAppSettings.skill_close:
            # 关闭指令
            admin_ids.remove(msg_info.FromUserName)
            globalRedis.delete(open_reply_group % msg_info.FromUserName)
        elif msg_info.Content == globalAppSettings.skill_kk:
            # 开启夸夸模式
            # 设置当前群的模式为夸夸模式
            globalRedis.set(reply_mode % msg_info.FromUserName, globalAppSettings.skill_kk)
        elif msg_info.Content == globalAppSettings.skill_tg:
            # 开启抬杠模式
            globalRedis.set(reply_mode % msg_info.FromUserName, globalAppSettings.skill_tg)
        elif msg_info.Content == globalAppSettings.skill_zj:
            # 开始总结
            pass
        elif msg_info.Content == globalAppSettings.skill_open_zj:
            # 开启总结
            globalRedis.set(open_summary_group % msg_info.FromUserName, globalAppSettings.skill_tg)
        elif msg_info.Content == globalAppSettings.skill_close_zj:
            # 关闭总结
            globalRedis.delete(open_summary_group % msg_info.FromUserName)


# 判定当前是否是指令
def is_command(msg_info: MsgInfo):
    """判定集合中是否有指令，并且是否是管理员发布的"""
    return msg_info.Content in wx_commands and msg_info.ActionUserName in admin_ids


async def check_idiom(msg_info):
    try:
        key = idiom_user % msg_info.FromUserName
        # 是否开启了看图猜成语
        if globalRedis.get(key) and globalRedis.get(msg_info.Content):
            token = await globalRedis.acquire_lock(msg_info.Content + msg_info.FromUserName)
            if not token:
                return
            globalRedis.delete(idiom_user % msg_info.FromUserName)
            globalRedis.delete(msg_info.Content)
            globalRedis.release_lock(token.lock_key, token.token)
            result = await GuessIdiom.get_idiom_source(msg_info.Content)
            if result:
                reply_info = f"恭喜@{msg_info.ActionNickName}，答对了！\n【答案】{msg_info.Content}\n【发音】{result.pinyin}\n【解释】{result.diangu}\n【出处】{result.chuchu}\n【范例】{result.fanli}"
                await send_txt(to_user_name=msg_info.FromUserName, txt=reply_info, at_users=msg_info.ActionUserName)
    except Exception as e:
        logger.error(e)


def on_error(_, error):
    logger.error(error)


def on_close(_, close_status_code, close_msg):
    logger.info("### closed ###")


def on_open(_):
    logger.info("### open ###")


def connect_wx_bot(url):
    global socket_server
    websocket.enableTrace(True)
    socket_server = websocket.WebSocketApp(url,
                                           on_message=on_message,
                                           on_error=on_error,
                                           on_close=on_close)
    socket_server.on_open = on_open
    socket_server.run_forever()
