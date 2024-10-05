import os
import sys
import winreg as reg

# 获取Python可执行文件路径
python_exe = sys.executable
print(python_exe)

# 获取脚本路径
script_path = os.path.realpath(__file__)

# 创建任务计划项
def create_task():
    # 打开任务计划项注册表
    key = reg.OpenKey(reg.HKEY_CURRENT_USER,
                      r"Software/Microsoft/Windows/CurrentVersion/Run",
                      0, reg.KEY_SET_VALUE)

    # 设置任务计划项
    reg.SetValueEx(key, "My Python Program", 0, reg.REG_SZ,
                   '{} "{}"'.format(python_exe, script_path))

    # 关闭注册表
    reg.CloseKey(key)

# 删除任务计划项
def delete_task():
    try:
        # 打开任务计划项注册表
        key = reg.OpenKey(reg.HKEY_CURRENT_USER,
                          r"Software/Microsoft/Windows/CurrentVersion/Run",
                          0, reg.KEY_ALL_ACCESS)

        # 删除任务计划项
        reg.DeleteValue(key, "My Python Program")

        # 关闭注册表
        reg.CloseKey(key)
    except FileNotFoundError:
        pass

# 主函数
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        delete_task()
        print("Task removed")