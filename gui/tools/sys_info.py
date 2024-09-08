# coding=utf-8
# 作者: 拓跋龙
# 功能: 系统信息展示界面

import json

from qfluentwidgets import PushButton, TextEdit
from PySide6.QtWidgets import QWidget, QGridLayout, QApplication

from source.util.thread import Asynchronous
import source.client.tools.sys_info as sys_func

class SysInfo(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QGridLayout(self)
        self._layout.setSpacing(10)

        self.display_btn = PushButton('展示系统信息')
        self.display_btn.clicked.connect(lambda: self.display_sys_info())
        self._layout.addWidget(self.display_btn, 0, 0, 1, 1)

        self.oled_screen = TextEdit()
        self.oled_screen.setReadOnly(True)
        self._layout.addWidget(self.oled_screen, 1, 0, 5, 5)

    def display_sys_info(self):
        self.print_msg('正在查询中, 请稍后……')
        asyn = Asynchronous(self.query_sys_info)
        asyn.finish.connect(lambda msg: self.print_sys_info(msg))
        asyn.run()

    def query_sys_info(self):
        win_info = sys_func.get_windows_info()
        cpu_info = sys_func.get_cpu_info()
        gpu_info = sys_func.get_gpu_info()
        disk_info = sys_func.get_disk_info()
        msg = {'系统信息': win_info,
               'CPU信息': cpu_info,
               'GPU信息': gpu_info,
               '硬盘信息': disk_info}
        msg = json.dumps(msg, indent=4, ensure_ascii=False)
        return msg

    def print_sys_info(self, msg):
        self.print_msg(msg)

    def print_msg(self, text, flag='set'):
        if flag == 'set':
            self.oled_screen.setPlainText(text)
        else:
            self.oled_screen.insertPlainText(text)
        QApplication.processEvents() # 立即刷新界面