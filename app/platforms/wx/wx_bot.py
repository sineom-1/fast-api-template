import json

import websocket

from app.platforms.wx.message import WXMessage
from app.platforms.wx.model.save_msg import SaveMsg
from app.platforms.wx.msg_type import WXMessageType
from app.utils import logger
from app.utils.chat_history_util import ChatHistoryUtil


def on_message(_, message):
    logger.debug(message)
    data = json.loads(message, strict=False)
    data = WXMessage(**data)
    if data.CurrentPacket.Data.AddMsg.MsgType == WXMessageType.Text:
        save_msg = SaveMsg(
            FromUserName=data.CurrentPacket.Data.AddMsg.FromUserName,
            ToUserName=data.CurrentPacket.Data.AddMsg.ToUserName,
            Content=data.CurrentPacket.Data.AddMsg.Content,
            ActionUserName=data.CurrentPacket.Data.AddMsg.ActionUserName,
            ActionNickName=data.CurrentPacket.Data.AddMsg.ActionNickName,
        )
        ChatHistoryUtil.save_msg(save_msg)


def on_error(_, error):
    print(error)


def on_close(_, close_status_code, close_msg):
    print("### closed ###")


def on_open(_):
    print("### open ###")


def connect_wx_bot(url):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
