# coding=utf-8
# 作者: 拓跋龙
# 功能: 日志功能

import os
import logging
import traceback
from datetime import datetime, timedelta

from source.util.common_util import tar_file

MAX_LOG_SIZE = 20 * 1024 * 1024 # 20M

class Log(logging.Logger):

    _instance = None

    def __init__(self) -> None:
        super().__init__('mind_leader')
        self.setLevel(logging.INFO) # 设置日志级别

        # 创建一个handler，用于写入日志文件
        self.log_dir = os.path.join(os.getcwd(), 'log')
        self.cur_log_path = os.path.join(self.log_dir, 'mind_leader.log')
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        self.fh = logging.FileHandler(self.cur_log_path, encoding='utf-8')
        self.fh.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(formatter)

        # 给logger添加handler
        self.addHandler(self.fh)

        self.workspace_init()

    # Log对象单实例
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def workspace_init(self):
        # 获取当前时间
        now = datetime.now()
 
        # 获取年月日时分秒
        year = now.strftime('%Y')  # 年份
        month = now.strftime('%m')  # 月份
        day = now.strftime('%d')  # 日期
        hour = now.strftime('%H')  # 小时
        minute = now.strftime('%M')  # 分钟
        second = now.strftime('%S')  # 秒

        log_tar = os.path.join(self.log_dir, f'mind_leader_{year}{month}{day}{hour}{minute}{second}.tar.gz')
        if os.path.getsize(self.cur_log_path) > MAX_LOG_SIZE:
            tar_file(self.cur_log_path, log_tar)
            # 日志压缩后清理原日志文件
            with open(self.cur_log_path, 'w') as f:
                f.write('')
        self.clean_up_logs()
 
    def clean_up_logs(self, max_days=90):
        """删除指定目录下超过max_days的日志文件"""
        now = datetime.now()
        for log_file in os.listdir(self.log_dir):
            log_path = os.path.join(self.log_dir, log_file)
            if not log_file.endswith('.tar.gz'):
                continue
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(log_path))
            if now - file_mod_time > timedelta(days=max_days):
                os.remove(log_path)
                self.error(f"Log file {log_file} has been deleted.")

logger = Log()

def log_debug(text: str):
    logger.debug(text)

def log_info(text: str):
    logger.info(text)

def log_error(text: str):
    logger.error(text)

def set_log_level(level: str | int):
    try:
        logger.setLevel(level)
        return True
    except Exception:
        log_error(traceback.format_exc())
        return False