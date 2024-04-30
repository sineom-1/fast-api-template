import json
import re

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
        "Authorization": "Bearer app-KOgillOBGFBnF6Xn6eHNkitR",
        "Content-Type": "application/json"
    }
    with httpx.stream("POST", "https://api.dify.ai/v1/chat-messages", data=json.dumps(data),
                      headers=headers) as response:
        for chunk in response.iter_lines():
            pattern = r'data:\s*(\{.*?\})'
            print(chunk)
            match = re.search(pattern, chunk, re.DOTALL)
            if match:
                extracted_data = match.group(1)
                print(extracted_data)
            else:
                print("No match found")

asyncio.run(test_dify_aoi("你是谁？"))
