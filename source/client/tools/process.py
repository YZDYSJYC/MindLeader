# coding=utf-8
# 作者: 拓跋龙
# 功能: 进程管理功能

'''
提供了一些用于处理进程的工具类，包括通过窗体标题获取PID、终止进程等功能。
所有的功能为Windows系统专用，不支持Unix系统
'''

import ctypes
import ctypes.wintypes as wintypes
import fnmatch
import os
import re
import signal
import subprocess
import sys
from typing import Literal

import psutil

from source.util.log import log_error, log_info

"""
一个用于处理系统进程的工具类，专为Windows系统设计。

该类提供了基于窗体标题获取进程ID（PID）和通过PID终止进程的方法。

方法：
    get_pid_by_full_window_title(title: str) -> int:
        通过完整的窗体标题获取进程的PID。

    get_pid_by_regex_window_title(title: str) -> int:
        通过正则表达式匹配窗体标题获取进程的PID。

    get_pid_by_fnmatch_window_title(title: str) -> int:
        通过通配符匹配窗体标题获取进程的PID。

    get_pid_by_partial_window_title(title: str) -> int:
        通过部分窗体标题获取进程的PID。

    kill_process(pid: int) -> bool:
        尝试通过PID终止进程，使用多种方法。

示例：
    ```python
    from utils.process_utils import Progress

    # 通过完整的窗体标题获取PID
    pid = Progress.get_pid_by_full_window_title("WeChat")
    print(pid)

    # 通过正则表达式匹配窗体标题获取PID
    pid = Progress.get_pid_by_regex_window_title(".*WeChat.*")
    print(pid)

    # 通过通配符匹配窗体标题获取PID
    pid = Progress.get_pid_by_fnmatch_window_title("*WeChat*")
    print(pid)

    # 通过部分窗体标题获取PID
    pid = Progress.get_pid_by_partial_window_title("WeChat")
    print(pid)

    # 终止指定的进程
    Progress.kill_process(pid)
    ```
"""

@staticmethod
def get_pid_by_full_window_title(title: str) -> int:
    """通过完整的窗体标题获取对应程序的PID

    Args:
        title (str): 窗体标题的名称。

    Returns:
        int: 对应的进程PID，如果未找到返回-1。
    """
    # 定义所需的Windows API函数
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    # FindWindow函数，用于查找窗体句柄
    FindWindow = user32.FindWindowW
    FindWindow.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
    FindWindow.restype = wintypes.HWND

    # GetWindowThreadProcessId函数，用于获取进程ID
    GetWindowThreadProcessId = user32.GetWindowThreadProcessId
    GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    GetWindowThreadProcessId.restype = wintypes.DWORD

    try:
        # 查找窗体句柄
        hwnd = FindWindow(None, title)
        if not hwnd:
            print(f"未找到标题为 '{title}' 的窗体。")
            return -1

        # 获取进程ID
        pid = wintypes.DWORD()
        GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        return pid.value

    except Exception as e:
        print(f"发生错误: {e}")
        return -1

def get_pid_by_regex_window_title(title: str) -> int:
    """通过正则表达式匹配窗体标题获取对应程序的PID

    Args:
        title (str): 窗体标题的正则表达式。

    Returns:
        int: 对应的进程PID，如果未找到返回-1。
    """
    return _get_pid(title, "regex")

def get_pid_by_fnmatch_window_title(title: str) -> int:
    """通过通配符匹配窗体标题获取对应程序的PID

    Args:
        title (str): 窗体标题的通配符。

    Returns:
        int: 对应的进程PID，如果未找到返回-1。
    """
    return _get_pid(title, "fnmatch")

def get_pid_by_partial_window_title(title: str) -> int:
    """通过部分的窗体标题获取对应程序的PID

    Args:
        title (str): 窗体标题的部分名称。

    Returns:
        int: 对应的进程PID，如果未找到返回-1。
    """
    return _get_pid(title, "partial")

def kill_process(pid: int) -> bool:
    """通过PID终止指定的进程

    尝试终止指定的进程，通过以下步骤：
    1. 发送SIGTERM信号优雅停止。
    2. 发送SIGKILL信号强制停止。
    3. 如果依旧无法停止，则请求管理员权限并使用os.kill。
    4. 如果依旧无法停止，则使用taskkill命令。

    Args:
        pid (int): 要终止的进程ID。

    Returns:
        bool: 如果进程成功终止，返回True；否则返回False。
    """
    try:
        process = psutil.Process(pid)

        # Step 1: 尝试发送SIGTERM信号优雅停止
        process.terminate()
        try:
            process.wait(timeout=5)
        except psutil.TimeoutExpired:
            pass

        if not process.is_running():
            log_info(f"进程 {pid} 已优雅停止。")
            return True

        # Step 2: 发送SIGKILL信号强制停止
        process.kill()
        try:
            process.wait(timeout=5)
        except psutil.TimeoutExpired:
            pass

        if not process.is_running():
            log_info(f"进程 {pid} 已强制停止。")
            return True

    except (psutil.NoSuchProcess, psutil.ZombieProcess):
        # 如果进程不存在或是僵尸进程，返回True
        log_error(f"进程 {pid} 不存在或是僵尸进程。")
        return True
    except psutil.AccessDenied:
        # 如果权限不足，尝试提升权限
        try:
            ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, f"{__file__} {pid}", None, 1
                    )
            return True
        except Exception as e:
            log_error(f"管理员权限请求失败: {e}")

    # Step 3: 提升权限后再尝试使用os.kill
    try:
        os.kill(pid, signal.SIGKILL)
        log_info(f"进程 {pid} 已使用os.kill成功终止。")
        return True
    except (PermissionError, ProcessLookupError) as e:
        log_error(f"使用os.kill终止失败: {e}")

    # Step 4: 最后一步，尝试在Windows上使用taskkill强制终止进程
    if os.name == 'nt':
        try:
            subprocess.check_call(['taskkill', '/F', '/PID', str(pid)])
            log_info(f"进程 {pid} 已使用taskkill成功终止。")
            return True
        except subprocess.CalledProcessError as e:
            log_error(f"使用taskkill终止失败: {e}")

    # 如果所有尝试都失败，返回False
    log_error(f"无法终止进程 {pid}。")
    return False

def _get_pid(search_title: str, current_mode: Literal["regex", "fnmatch", "partial"]) -> int:
    """通过正则表达式匹配窗体标题获取对应程序的PID"""
    # 定义所需的Windows API函数
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    GetWindowThreadProcessId = user32.GetWindowThreadProcessId
    GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    GetWindowThreadProcessId.restype = wintypes.DWORD

    windows = get_processes()

    for title, pid in windows:
        if current_mode == "regex":
            if re.search(search_title, title):
                return pid
        elif current_mode == "fnmatch":
            if fnmatch.fnmatch(title, search_title):
                return pid
        elif current_mode == "partial":
            if search_title.lower() in title.lower():
                return pid
    return -1

def get_processes():
    # 定义所需的Windows API函数
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    
    # 定义用于枚举窗口的回调函数类型
    EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    # 定义所需的Windows API函数
    EnumWindows = user32.EnumWindows
    EnumWindows.argtypes = [EnumWindowsProc, wintypes.LPARAM]
    EnumWindows.restype = wintypes.BOOL

    GetWindowTextLength = user32.GetWindowTextLengthW
    GetWindowTextLength.argtypes = [wintypes.HWND]
    GetWindowTextLength.restype = ctypes.c_int

    GetWindowText = user32.GetWindowTextW
    GetWindowText.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    GetWindowText.restype = ctypes.c_int
    processes = []

    GetWindowThreadProcessId = user32.GetWindowThreadProcessId
    GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    GetWindowThreadProcessId.restype = wintypes.DWORD

    def foreach_window(hwnd, _):
        length = GetWindowTextLength(hwnd)
        if length > 0:
            buffer = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buffer, length + 1)
            pid = wintypes.DWORD()
            GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            processes.append([buffer.value, pid.value])
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)

    return processes

if __name__ == '__main__':
    # 通过完整的窗体标题获取PID
    pid = get_pid_by_full_window_title('思维导航')
    print(pid)

    # 通过正则表达式匹配窗体标题获取PID
    # pid = get_pid_by_regex_window_title(".*WeChat.*")
    # print(pid)

    # # 通过通配符匹配窗体标题获取PID
    # pid = Progress.get_pid_by_fnmatch_window_title("*WeChat*")
    # print(pid)

    # # 通过部分窗体标题获取PID
    # pid = Progress.get_pid_by_partial_window_title("WeChat")
    # print(pid)

    # # 终止指定的进程
    # Progress.kill_process(pid)
