#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author sineom
@Date 2024/5/13-17:29
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
import json
import re
from typing import Optional

import httpx
from loguru import logger

from app.adapter.base_adapter import BaseAdapter
from app.config import globalAppSettings


class DifyAdapter(BaseAdapter):
    def __init__(self, session_id: str = "unknown"):
        super().__init__(session_id)
        self.session_id = session_id
        self.supported_models = {"kk": globalAppSettings.dify_kk_key, "tg": globalAppSettings.dify_tg_key}
        self.current_model = "tg"
        self.acs_client = httpx.AsyncClient()
        self.client = httpx.AsyncClient()
        self.__setup_headers(self.client)

    def __setup_headers(self, client):
        client.headers['Authorization'] = self.supported_models.get(self.current_model)
        client.headers['Content-Type'] = "application/json"

    async def ask(self, msg: str) -> str:
        """向 AI 发送消息"""
        logger.info("Asking Dify: %s" % msg)
        try:
            logger.debug("token is %s" % self.client.headers.get("Authorization"))
            async with self.client.stream("POST", globalAppSettings.dify_url,
                                          json=self.__generate_payload(msg), timeout=120) as response:
                answer = ""
                async for chunk in response.aiter_text():
                    if not chunk.strip():
                        continue
                    json_data = self.extract_json_data(chunk)
                    if json_data:
                        answer += json_data.get("answer", "")
                logger.debug("Final answer: %s" % answer)
                return answer
        except httpx.RequestError as e:
            e.with_traceback()
            logger.error("HTTP request error: %s", e)
        except Exception as e:
            e.with_traceback()
            logger.error("An unexpected error occurred: %s", e)

    def extract_json_data(self, chunk: str) -> Optional[dict]:
        """尝试从chunk中提取JSON数据"""
        pattern = r"({.*})"
        match = re.search(pattern, chunk, re.DOTALL)
        if match:
            try:
                extracted_data = match.group(1)
                return json.loads(extracted_data)
            except json.JSONDecodeError as e:
                logger.error("JSON decode error: %s", e)
        return None

    def __generate_payload(self, msg: str) -> dict:
        return {
            "inputs": {},
            "query": msg,
            "response_mode": "streaming",
            "conversation_id": self.session_id,
            "user": self.session_id,
            "files": []
        }

    def switch_model(self, model_name):
        if model_name in self.supported_models:
            self.current_model = model_name
            self.__setup_headers(self.client)
