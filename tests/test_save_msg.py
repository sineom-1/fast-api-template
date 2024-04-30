"""
@Author sineom
@Date 2024/4/30-14:14
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""

import json

from app.platforms.wx.message import WXMessage
from app.platforms.wx.model.save_msg import SaveMsg

msg = """{
    "CurrentPacket": {
        "WebConnId": "",
        "Data": {
            "AddMsg": {
                "MsgId": 1232300195,
                "FromUserName": "hf-2-68",
                "ToUserName": "wxid_sib20p52764722",
                "MsgType": 1,
                "Content": "21",
                "Status": 3,
                "ImgStatus": 1,
                "ImgBuf": null,
                "CreateTime": 1714458562,
                "MsgSource": "\u003cmsgsource\u003e\n\t\u003calnode\u003e\n\t\t\u003cfr\u003e1\u003c/fr\u003e\n\t\u003c/alnode\u003e\n\t\u003cpua\u003e1\u003c/pua\u003e\n\t\u003csignature\u003eV1_0y1EvSP3|v1_0y1EvSP3\u003c/signature\u003e\n\t\u003ctmp_node\u003e\n\t\t\u003cpublisher-id\u003e\u003c/publisher-id\u003e\n\t\u003c/tmp_node\u003e\n\u003c/msgsource\u003e\n",
                "PushContent": "🌝 : 21",
                "NewMsgId": 4128129486240340728,
                "NewMsgIdExt": "4128129486240340728",
                "ActionUserName": "",
                "ActionNickName": "🌝"
            },
            "EventName": "ON_EVENT_MSG_NEW"
        }
    },
    "CurrentWxid": "wxid_sib20p52764722"
}"""


def save_msg(msg):
    data = json.loads(msg, strict=False)
    data = WXMessage(**data)
    #  保存聊天记录

    save_msg = SaveMsg(
        FromUserName=data.CurrentPacket.Data.AddMsg.FromUserName,
        ToUserName=data.CurrentPacket.Data.AddMsg.ToUserName,
        Content=data.CurrentPacket.Data.AddMsg.Content,
        ActionUserName=data.CurrentPacket.Data.AddMsg.ActionUserName,
        ActionNickName=data.CurrentPacket.Data.AddMsg.ActionNickName, )
    file_path = "./test.txt"
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{save_msg.ActionNickName}({save_msg.time}): {save_msg.Content}\n")


save_msg(msg)
