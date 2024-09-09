# coding=utf-8
# 作者: 拓跋龙
# 功能: 获取系统信息

import pynvml
import wmi
import platform
import subprocess
import socket
import re

_wmi = None

def wmi_init():
    global _wmi
    _wmi = wmi.WMI()

def get_gpu_info():
    gpu_names = {}
    try:
        pynvml.nvmlInit()
    except Exception:
        return '您的电脑没有英伟达显卡!'
    for i in range(pynvml.nvmlDeviceGetCount()):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        gpu_names[f'显卡{i + 1}型号'] = pynvml.nvmlDeviceGetName(handle)
    return gpu_names

def get_cpu_info():
    cpu = _wmi.WIN32_Processor()[0]
    return {'CPU型号': cpu.Name, '核心数': cpu.NumberOfCores}

def get_windows_info():
    win_info = platform.uname()
    host_ip = socket.gethostbyname(win_info.node)
    return {'计算机名称': win_info.node,
            '计算机IP': host_ip,
            '系统版本': f'{win_info.system} {win_info.release}',
            '系统内核版本': win_info.version}

def get_disk_info():
    disks_info = []
    disks = _wmi.Win32_DiskDrive()
    for disk in disks:
        if '虚拟' not in disk.Caption:
            manufacturer = disk.Name
            serialNumber = disk.SerialNumber
            size = int(disk.Size) // 1024 // 1024 // 1024
            disks_info.append({'硬盘名称': manufacturer, '序列号': serialNumber, '硬盘大小': f'{size}G'})
    return disks_info

def get_vpn_info():
    output = subprocess.check_output('ipconfig', shell=True).decode('gbk')
    vpn_name = ''
    vpn_names = []
    ip_addrs = []
    for line in output.split('\n'):
        if 'PPP' in line:
            vpn_name = line.split(':')[0].replace('PPP 适配器 ', '')
            vpn_names.append(vpn_name)
        if vpn_name and 'IPv4 地址' in line:
            ip_addr = line.split(':')[-1].strip()
            ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            ip_addr = re.findall(ip_pattern, ip_addr)[0]
            ip_addrs.append(ip_addr)

    vpn_info = {}
    for vpn_name, ip_addr in zip(vpn_names, ip_addrs):
        vpn_info[vpn_name] = ip_addr
    return vpn_info

if __name__ == '__main__':
    wmi_init()
    print(get_cpu_info())
    print(get_gpu_info())
    print(get_disk_info())
    print(get_windows_info())
    print(get_vpn_info())
