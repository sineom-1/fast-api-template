#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast-api-template
@File    ：load_conf.py
@Author  ：Mr.LiuQHui
@Date    ：2024/3/22 12:22
"""
import argparse
import os
from functools import lru_cache

from dotenv import load_dotenv

from app import config
from app.constant.redis_key import admin, open_reply_group
from app.utils.redis_client import RedisClient

# 指令的集合
wx_commands = []

# 管理员id
admin_ids = []

# 已经开启回复的群
reply_group = None

# 已经开启总结的群
summary_group = []

# 已经开启看图猜成语的群
idiom_group = []


def getEnvFile() -> str:
    """ 获取加载的配置文件"""
    # 读取运行环境
    run_env = os.environ.get("APP_ENV", "")
    print("运行环境: ", run_env)
    # 默认加载.env
    env_file = ".env"
    # 运行环境不为空加载 .env 文件
    if run_env != "":
        # 当是其他环境时，如测试环境: 加载 .env 正式环境: 加载.env.prod
        env_file = f".env.{run_env}"
    return env_file


@lru_cache
def getAppConfig() -> config.AppConfigSettings:
    """ 获取项目配置 """
    # 解析命令行参数
    parseCliArgument()
    # 获取配置文件
    envFile = getEnvFile()
    print("获取配置文件: ", envFile)
    # 加载配置
    load_dotenv(envFile)
    # 实例化配置模型
    setting = config.AppConfigSettings()
    wx_commands.append(setting.skill_idiom)
    wx_commands.append(setting.skill_kk)
    wx_commands.append(setting.skill_tg)
    wx_commands.append(setting.skill_zj)
    wx_commands.append(setting.skill_open_zj)
    wx_commands.append(setting.skill_open)
    wx_commands.append(setting.skill_close)
    return setting


@lru_cache
def getRedisClient() -> RedisClient:
    """ 获取redis客户端 """
    setting = getAppConfig()
    redis = RedisClient(setting.redis_host, setting.redis_port, setting.redis_db, setting.redis_user_name,
                        setting.redis_password, setting.redis_pool_size)
    _admin_ids = redis.get(admin)
    admin_ids.extend(setting.admin_id)
    admin_ids.extend(_admin_ids)
    reply_group = redis.smembers(open_reply_group)
    return redis


def parseCliArgument():
    """ 解析命令行参数 """
    # print("解析命令行参数:", sys.argv[0])
    # if "uvicorn" in sys.argv[0]:
    #     # TODO 使用uvicorn启动,则解析--env-file文件
    #     print("使用uvicorn启动....")
    #     return
    # 使用 argparse 定义命令行参数
    parser = argparse.ArgumentParser(description="命令行参数")
    parser.add_argument("--env", type=str, default="", help="运行环境")
    # 解析命令行参数
    args = parser.parse_args()
    # 设置环境变量
    # uvicorn模式启动，读取的.env*里面的APP_ENV
    os.environ["APP_ENV"] = args.env


# 创建全局配置实例
globalAppSettings = getAppConfig()

# 创建redis实例
globalRedis = getRedisClient()
