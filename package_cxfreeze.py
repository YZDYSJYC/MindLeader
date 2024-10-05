#!/usr/bin/env python
# coding=utf-8
# auther: j30001764
# descripition: Python打包功能

import os
import sys
import shutil
import traceback
from source.util.default_config import VERSION
from cx_Freeze import setup, Executable

# cx_Freeze打包固定需要 build 参数, 代码侧直接添加, 无需调用方传入
sys.argv.append('build')

g_work_space = os.getcwd()

def cp_dir():
    dirs = ['config/', 'gui/qss/', 'README.md']
    dst_path = os.path.join(g_work_space, 'build', 'exe.win-amd64-3.12')
    for dir in dirs:
        if os.path.isdir(dir):
            shutil.copytree(dir, os.path.join(dst_path, dir), ignore_dangling_symlinks=True, dirs_exist_ok=True)
        else:
            shutil.copy(dir, dst_path)
    # 打包时删除数据库文件
    shutil.rmtree(os.path.join(dst_path, 'config/db'))
    os.mkdir(os.path.join(dst_path, 'config/db'))
    print('配置文件拷贝完成!')


# target
main_target = Executable(script='main.py', base='Win32GUI', icon='config/title.ico', target_name='MindLeader')
# upgrade_target = Executable(script='gui/upgrade.py', base='Win32GUI', icon='config/title.ico', target_name='upgrade')

# setup
setup(
    name = 'MindLeader',
    version = VERSION,
    description = 'MindLeader',
    auther = '拓跋龙',
    options = {'build_exe': {
        'includes': ['dbm.dumb'], # 需要额外打包的库
        'excludes': [], # 不需要打包的库
    }},
    executables = [main_target]
)

try:
    cp_dir()
except Exception:
    traceback.print_exc()
