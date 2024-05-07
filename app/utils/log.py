#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author sineom
@Date 2024/4/29-10:58
@Email h.sineom@gmail.com
@description  日志文件
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""

from loguru import logger

logfile_dir = "./logs/{time}.log"

# 配置 loguru
logger.add(logfile_dir,
           rotation="1 day",
           compression="zip",
           level="INFO",
           enqueue=True,
           backtrace=True,
           format="{time:YYYY-MM-DD at HH:mm:ss} - {level} - {message}")
