# coding=utf-8
# 作者: 拓跋龙
# 功能: 获取系统信息

import pynvml
import wmi
import platform

WMI = wmi.WMI()

def get_gpu_info():
    gpu_names = []
    pynvml.nvmlInit()
    for i in range(pynvml.nvmlDeviceGetCount()):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        gpu_names.append(pynvml.nvmlDeviceGetName(handle))
    return gpu_names

def get_cpu_info():
    cpu = WMI.WIN32_Processor()[0]
    return {'CPU型号': cpu.Name, '核心数': cpu.NumberOfCores}

def get_windows_info():
    win_info = platform.uname()
    print(win_info.system)
    return {'计算机名称': win_info.node,
            '系统版本': f'{win_info.system} {win_info.release}',
            '系统内核版本': win_info.version}

def get_disk_info():
    disks_info = []
    disks = WMI.Win32_DiskDrive()
    for disk in disks:
        if '虚拟' not in disk.Caption:
            manufacturer = disk.Name
            serialNumber = disk.SerialNumber
            size = int(disk.Size) // 1024 // 1024 // 1024
            disks_info.append({'硬盘名称': manufacturer, '序列号': serialNumber, '硬盘大小': f'{size}G'})
    return disks_info

if __name__ == '__main__':
    get_disk_info()