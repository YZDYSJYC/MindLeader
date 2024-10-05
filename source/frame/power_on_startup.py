import os
import sys

# 获取当前用户的系统路径
user_startup_path = os.environ['APPDATA']
# 获取可执行文件路径
exe_path = sys.executable
exe_dir = os.path.dirname(exe_path)
batpath = os.path.join(user_startup_path, 'Microsoft/Windows/Start Menu/Programs/Startup/MindLeader.bat')

# 创建任务计划项
def register_power_on():
    if os.path.exists(batpath):
        return

    disk_letter = exe_dir.split(':')[0]
    with open(batpath, 'w', encoding='utf-8') as f:
        f.write(f'cd /{disk_letter} {exe_dir} \n')
        f.write(f'start /B {exe_path}')

# 删除任务计划项
def delete_power_on():
    if os.path.exists(batpath):
        os.remove(batpath)
