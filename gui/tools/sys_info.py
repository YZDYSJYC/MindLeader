# coding=utf-8
# 作者: 拓跋龙
# 功能: 系统信息展示界面

from qfluentwidgets import PushButton, TextEdit
from PySide6.QtWidgets import QWidget, QGridLayout

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
        pass