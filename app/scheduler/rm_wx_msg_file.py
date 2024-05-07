"""
@Author sineom
@Date 2024/5/7-10:33
@Email h.sineom@gmail.com
@description  每天凌晨清楚前一天的微信消息文件
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""
import datetime
import os
import shutil
import time

import schedule
from loguru import logger

from app.config import globalAppSettings


def rm_wx_msg_folder():
    logger.info("执行定时任务：删除前一天的微信消息文件")
    # 获取前一天的日期
    previous_day = datetime.datetime.now() - datetime.timedelta(days=1)
    folder_name = previous_day.strftime("%Y/%m/%d")
    folder_path = os.path.join(globalAppSettings.wx_msg_path, folder_name)
    # 判定文件是否存在
    if os.path.exists(folder_path):
        # 删除文件夹以及文件
        shutil.rmtree(folder_path, ignore_errors=True)
        logger.info(f"删除文件夹：{folder_path}")

    else:
        logger.info(f"文件夹不存在：{folder_path}")


# 设置定时任务，每天凌晨12点执行一次
schedule.every().day.at("00:00").do(rm_wx_msg_folder)


def run_scheduler():
    # 立即执行一次
    rm_wx_msg_folder()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run_scheduler()
