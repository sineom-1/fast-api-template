#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast-api-template
@File    ：main.py
@Author  ：Mr.LiuQHui
@Date    ：2023/11/13 17:44 
"""
import uvicorn
from fastapi import FastAPI
from app.router import index_router, admin_router, open_router

# 实例化
app = FastAPI(redoc_url=None)
# 加载路由
app.include_router(index_router.router)
app.include_router(admin_router.router)
app.include_router(open_router.router)

#
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
