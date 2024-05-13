import asyncio
import json
import re
from typing import Optional

import httpx

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


async def dify_api(query: str):
    data = {
        "inputs": {},
        "query": query,
        "response_mode": "streaming",
        "conversation_id": "",
        "user": "abc-123",
        "files": []
    }
    headers = {
        "Authorization": "Bearer app-KOgillOBGFBnF6Xn6eHNkitR",
        "Content-Type": "application/json"
    }
    try:
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", "https://api.dify.ai/v1/chat-messages",
                                     json=data, headers=headers, timeout=60) as response:
                answer = ""
                async for chunk in response.aiter_text():
                    print("Received chunk: %s", chunk)
                    if not chunk.strip():
                        print("Empty or whitespace chunk, skipping")
                        continue

                    json_data = await extract_json_data(chunk)
                    if json_data:
                        answer += json_data.get("answer", "")
                print("Final answer: %s" % answer)
                return answer
    except httpx.RequestError as e:
        print("HTTP request error: %s", e)
    except Exception as e:
        print("An unexpected error occurred: %s", e)


async def extract_json_data(chunk: str) -> Optional[dict]:
    """尝试从chunk中提取JSON数据"""
    pattern = r"({.*})"
    match = re.search(pattern, chunk, re.DOTALL)
    if match:
        try:
            extracted_data = match.group(1)
            return json.loads(extracted_data)
        except json.JSONDecodeError as e:
            print("JSON decode error: %s", e)
    return None


asyncio.run(dify_api("你是谁"))
