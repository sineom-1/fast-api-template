#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author sineom
@Date 2024/5/8-16:23
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""

from functools import wraps
from typing import TypeVar, Optional, Callable, Any

import httpx
from httpx import Response
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


def handle_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            raise
        except httpx.RequestError as e:
            print(f"Network error occurred: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    return wrapper


def _parse_data(response: Response, return_type: Optional[T] = None):
    response.raise_for_status()
    json_data = response.json()
    if return_type is not None:
        if hasattr(return_type, '__call__'):
            return return_type(**json_data)
        else:
            raise ValueError("return_type must be a Pydantic model or a callable")
    else:
        return json_data


class HttpxSchema:

    @handle_errors
    def make_request(self, url: str, method: str, return_type: Optional[T] = None, **kwargs):
        """
        构建同步的请求方式

        参数:
        - url: 请求的 url
        - method: 请求的方法
        - return_type: 返回的数据类型
        - **kwargs: 其他参数
        """
        with httpx.Client(event_hooks=kwargs["event_hooks"]) as client:
            # 是否是post请求
            if method.lower() == "post":
                response = client.request(method, url,
                                          data=kwargs["data"],
                                          json=kwargs["json"],
                                          files=kwargs["files"],
                                          headers=kwargs["headers"],
                                          params=kwargs["params"],
                                          timeout=kwargs["timeout"])
            else:
                response = client.request(method, url,
                                          headers=kwargs["headers"],
                                          params=kwargs["params"],
                                          timeout=kwargs["timeout"])
            return _parse_data(response, return_type)

    @handle_errors
    async def make_request_async(self, url: str, method: str, return_type: Optional[T] = None, **kwargs):
        """
        构建异步的请求方式

        参数:
        - url: 请求的 url
        - method: 请求的方法
        - return_type: 返回的数据类型
        - **kwargs: 其他参数
        """
        with httpx.AsyncClient(event_hooks=kwargs["event_hooks"]) as client:
            # 是否是post请求
            if method.lower() == "post":
                response = client.request(method, url, data=kwargs["data"],
                                          files=kwargs["files"],
                                          headers=kwargs["headers"],
                                          params=kwargs["params"],
                                          timeout=kwargs["timeout"])
            else:
                response = client.request(method, url,
                                          headers=kwargs["headers"],
                                          params=kwargs["params"],
                                          timeout=kwargs["timeout"])
            return _parse_data(response, return_type)

    # post的异步请求
    @classmethod
    async def post_async_data(cls, url: str,
                              data: Optional[Any] = None,
                              params: Optional[Any] = None,
                              files: Optional[dict] = None,
                              return_type: Optional[T] = None,
                              headers: Optional[dict] = None,
                              timeout: float = 60.0,
                              event_hooks: Optional[dict] = None) -> Any:
        """
        post的异步请求

        参数:
        - url: 请求的 url
        - data: 请求的数据
        - files: 上传文件
        - return_type: 返回的数据类型
        - headers: 请求头
        - timeout: 超时时间
        - event_hooks: 事件钩子 如 {'request': [log_request], 'response': [log_response]}  https://www.python-httpx.org/advanced/event-hooks/
        """
        result = await cls.make_request_async(cls, url, 'post', return_type, data=data, files=files, headers=headers,
                                              timeout=timeout,
                                              params=params,
                                              event_hooks=event_hooks)
        return result

    # get的异步请求
    @classmethod
    async def get_async_data(cls, url: str,
                             params: Optional[Any] = None,
                             return_type: Optional[T] = None,
                             headers: Optional[dict] = None, timeout: float = 60.0,
                             event_hooks: Optional[dict] = None) -> Any:
        """
        get的异步请求

        参数:
        - url: 请求的 url
        - params: 请求的参数
        - return_type: 返回的数据类型
        - headers: 请求头
        - timeout: 超时时间
        - event_hooks: 事件钩子 如 {'request': [log_request], 'response': [log_response]}  https://www.python-httpx.org/advanced/event-hooks/
        """
        result = await cls.make_request_async(cls, url, 'get', return_type, params=params, headers=headers,
                                              timeout=timeout,
                                              event_hooks=event_hooks)
        return result

    # get的同步请求
    @classmethod
    def get_data(cls,
                 url: str,
                 params: Optional[Any] = None,
                 return_type: Optional[T] = None,
                 headers: Optional[dict] = None,
                 timeout: float = 60.0,
                 event_hooks: Optional[dict] = None
                 ) -> Any:
        """
        get的同步请求

        参数:
        - url: 请求的 url
        - params: 请求的参数
        - return_type: 返回的数据类型
        - headers: 请求头
        - timeout: 超时时间
        - event_hooks: 事件钩子 如 {'request': [log_request], 'response': [log_response]}  https://www.python-httpx.org/advanced/event-hooks/
        """

        result = cls.make_request(cls, url, 'get', return_type, params=params, headers=headers, timeout=timeout,
                                  event_hooks=event_hooks)
        return result

    # post的同步请求
    @classmethod
    def post_data(cls, url: str,
                  data: Optional[Any] = None,
                  json: Optional[Any] = None,
                  params: Optional[Any] = None,
                  files: Optional[dict] = None,
                  return_type: Optional[T] = None,
                  headers: Optional[dict] = None, timeout: float = 60.0,
                  event_hooks: Optional[dict] = None) -> Any:
        """
        post的同步请求

        参数:
        - url: 请求的 url
        - data: 请求的数据
        - files: 上传文件
        - return_type: 返回的数据类型
        - headers: 请求头
        - timeout: 超时时间
        - event_hooks: 事件钩子 如 {'request': [log_request], 'response': [log_response]}  https://www.python-httpx.org/advanced/event-hooks/
        """
        result = cls.make_request(cls,
                                  url,
                                  'post',
                                  return_type,
                                  data=data,
                                  json=json,
                                  files=files,
                                  headers=headers,
                                  params=params,
                                  timeout=timeout,
                                  event_hooks=event_hooks)
        return result
