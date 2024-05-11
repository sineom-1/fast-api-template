#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author sineom
@Date 2024/4/29-10:58
@Email h.sineom@gmail.com
@description  日志文件
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
import sys

from loguru import logger

logfile_dir = "./logs/{time:YYYY-MM-DD}.log"

# 配置第二个日志处理器，输出到文件，并进行分割和压缩
logger.add(logfile_dir,
           rotation="1 day",
           compression="zip",
           level="INFO",
           enqueue=True,
           backtrace=True,
           serialize=True,
           format="{time:YYYY-MM-DD at HH:mm:ss} - {level} - {message}")

# 配置第三个日志处理器，输出到文件，但不记录INFO及以上级别的日志
logger.add(
    "./logs/{time:YYYY-MM-DD}_error.log",
    level="ERROR",
    format="{time:YYYY-MM-DD at HH:mm:ss} - {level} - {message}",
    serialize=True  # 序列化日志消息，使其更加紧凑
)
