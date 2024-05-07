import json

import websocket

from app.platforms.wx.message import WXMessage
from app.platforms.wx.model.save_msg import SaveMsg
from app.platforms.wx.msg_type import WXMessageType
from app.scheduler.rm_wx_msg_file import run_scheduler
from app.utils import logger
from app.utils.chat_history_util import ChatHistoryUtil


def on_message(_, message):
    logger.debug(message)
    data = json.loads(message, strict=False)
    data = WXMessage(**data)
    if data.CurrentPacket.Data.AddMsg.MsgType == WXMessageType.Text:
        if data.CurrentPacket.Data.AddMsg.FromUserName == "39253891795@chatroom":
            save_msg = SaveMsg(
                **{k: v for k, v in data.CurrentPacket.Data.AddMsg.dict().items() if k in SaveMsg.__fields__})
            ChatHistoryUtil.save_msg(save_msg)


def on_error(_, error):
    print(error)


def on_close(_, close_status_code, close_msg):
    print("### closed ###")


def on_open(_):
    print("### open ###")
    run_scheduler()


def connect_wx_bot(url):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
