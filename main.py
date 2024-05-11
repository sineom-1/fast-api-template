#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast-api-template
@File    ：main.py
@Author  ：Mr.LiuQHui
@Date    ：2023/11/13 17:44 
"""
from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from app import bootstrap
from app.config import globalAppSettings
from app import platforms
from app.platforms.wx.wx_bot import socket_server
from app.scheduler import InitScheduler

# 实例化
server = FastAPI(redoc_url=None, docs_url="/apidoc", title=globalAppSettings.app_name)

scheduler = AsyncIOScheduler()

# 配置和启动调度器
scheduler.configure(
    max_instances=3
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("项目启动")
    scheduler.start()
    InitScheduler()
    yield
    print("项目关闭")
    scheduler.shutdown()
    if socket_server:
        socket_server.close()


if __name__ == "__main__":
    print("打印项目配置:", globalAppSettings)
    # 初始化项目
    bootstrap.Init(server)
    platforms.Init()
    # 使用 python main.py 启动服务
    uvicorn.run(server, host=globalAppSettings.app_host, port=globalAppSettings.app_port)
