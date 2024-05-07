import json
import re
from asyncio import Timeout

import httpx
import asyncio
import time

# def test_dify(query):
#     data = {
#         "inputs": {},
#         "query": query,
#         "response_mode": "streaming",
#         "conversation_id": "",
#         "user": "abc-123",
#         "files": []
#     }
#     headers = {
#         "Authorization": "Bearer app-KOgillOBGFBnF6Xn6eHNkitR",
#         "Content-Type": "application/json"
#     }
#     request = requests.post("https://api.dify.ai/v1/chat-messages",
#                             json=data,
#                             headers=headers, stream=True)
#     print(request.status_code)
#     for chunk in request.iter_content(chunk_size=1024):
#         if chunk:
#             # 处理每个数据块
#             print(chunk)


msg = """
horsley(16:37): 上门取车貌似其实是代驾
辅助-摸鱼王(16:37): 还有一次跟朋友出去，车都开始胎压报警了，他说没问题，误报来的
糕乐糕乐糕(16:37): 瞧瞧 这就是有钱人的待遇 上门取车
"""


async def test_dify_aoi(query: str):
    data = {
        "inputs": {},
        "query": query,
        "response_mode": "streaming",
        "conversation_id": "",
        "user": "abc-123",
        "files": []
    }
    headers = {
        "Authorization": "Bearer app-ZQgsXzGUzFP1MPKWyjf1qsb2",
        "Content-Type": "application/json"
    }
    with httpx.stream("POST", "https://api.dify.ai/v1/chat-messages", data=json.dumps(data),
                      headers=headers, timeout=60) as response:
        answer = ""
        for chunk in response.iter_lines():
            print(chunk)
            if not chunk:
                print("Empty chunk")
                continue

            # 将chunk中的json数据提取出来
            pattern = r"({.*})"

            match = re.search(pattern, chunk, re.DOTALL)
            if match:
                extracted_data = match.group(1)
                print(extracted_data)
                json_data = json.loads(extracted_data)
                answer += json_data.get("answer") or ""
        print(answer)


asyncio.run(test_dify_aoi(msg))
