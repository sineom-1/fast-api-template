#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast-api-template 
@File    ：log.py
@Author  ：Mr.LiuQHui
@Date    ：2023/11/20 22:21 
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

# 创建Logger对象
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置日志记录级别为DEBUG

# 定义日志目录和日志文件名
logfile_dir = "./logs"
logfile_name = "app.log"

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

# 创建日志文件的路径
logfile_path = os.path.join(logfile_dir, logfile_name)

# 创建一个TimedRotatingFileHandler，每天午夜轮换日志
file_handler = TimedRotatingFileHandler(logfile_path, when="midnight", interval=1, backupCount=5)
file_handler.setLevel(logging.DEBUG)  # 设置文件中写入的日志等级
file_handler.suffix = "%Y-%m-%d.log"  # 设置分割后日志文件的后缀
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 创建StreamHandler对象，将日志输出到控制台
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  # 设置控制台显示的日志等级

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

# 将处理器添加到Logger对象中（注册）
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
