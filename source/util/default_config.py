# coding=utf-8
# 作者: 拓跋龙
# 功能: 默认配置

from qfluentwidgets import Theme
import logging

# 需保证配置配置最多只有两层结构
conf = {
    'System': {
        'Theme': Theme.AUTO,
        'MicaEnabled': True,
        'IsUpdateOnStart': True,
        'LogLevel': logging.ERROR,
    }
}

README_URL = 'https://github.com/YZDYSJYC/MindLeader/blob/main/README.md'
ISSUE_URL = 'https://github.com/YZDYSJYC/MindLeader/issues'
VERSION = '1.0.0'
AUTHOR = '拓跋龙'