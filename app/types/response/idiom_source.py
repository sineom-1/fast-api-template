#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author sineom
@Date 2024/5/7-15:12
@Email h.sineom@gmail.com
@description  成语出处
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
from typing import List

from pydantic import BaseModel


class IdiomSource(BaseModel):
    chengyu: str
    """成语"""
    pinyin: str
    """拼音"""
    diangu: str
    """典故"""
    chuchu: str
    """出处"""
    fanli: str
    """范例"""
    pysx: str
    """拼音缩写"""


class IdiomPage(BaseModel):
    curpage: int
    allnum: int
    list: List[IdiomSource]
