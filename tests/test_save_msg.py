"""
@Author sineom
@Date 2024/4/30-14:14
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""

import json
import re
from random import random


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


#  random() * 3.0 循环10次
# for _ in range(10):
#     print(random() * 3.0)

# 原始字符串
s = "@啊哟喔K说话"

# 使用正则表达式进行匹配
# 这个正则表达式会匹配以@开头，后面跟着任意数量的字符（包括空格），然后是我们要查找的字符串'bbbb'
match = re.search(r"@.*\s(\S+)", s)

# 如果匹配成功，获取匹配的字符串
result = match.group(1) if match else None

print(result)  # 输出应该是 'bbbb'
