"""
@Author sineom
@Date 2024/5/7-10:00
@Email h.sineom@gmail.com
@description  TODO
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""


def InitScheduler():
    from app.scheduler.rm_wx_msg_file import run_scheduler
    run_scheduler()
