# coding=utf-8
# 作者: 拓跋龙
# 功能: 数据库操作接口

import os
import shelve
import traceback

from source.util.default_config import conf

g_workspace = os.getcwd()
CONFIG_FILE = os.path.join(g_workspace, 'config/db/config') # nosql数据库
config_data = {} # 配置数据

def config_init():
    global config_data
    config_not_exists = False
    if not os.path.exists(f'{CONFIG_FILE}.dat'):
        config_not_exists = True
    with shelve.open(CONFIG_FILE) as data:
        if config_not_exists: # 首次启动或配置DB不存在, 则加载系统默认配置
            for k, v in conf.items():
                data[k] = v
            config_data = conf
        else:
            for key in data: # 若已存在, 则从数据库中读取数据
                config_data[key] = data[key]

def set_config(key1: str, value, key2=''):
    try:
        configs = config_data.get(key1)
        if configs is None:
            print(f'不存在的配置集: {key1}')
            return

        if key2: # 配置为dict类型
            if configs.get(key2) is None:
                print(f'不存在的配置: {key2}')
                return

            configs[key2] = value
            with shelve.open(CONFIG_FILE) as data:
                data[key1] = configs
        else: # 配置为str类型
            config_data[key1] = value
            with shelve.open(CONFIG_FILE) as data:
                data[key1] = value
    except Exception:
        traceback.print_exc()

def get_config(key1: str, key2=''):
    configs = config_data.get(key1)
    if configs is None:
        print(f'不存在的配置集: {key1}')
        raise Exception(f'不存在的配置集: {key1}')

    if key2: # 配置为dict类型
        config = configs.get(key2)
        if config is None:
            print(f'不存在的配置: {key2}')
            raise Exception(f'不存在的配置: {key2}')
        return config
    else: # 配置为str类型
        return configs