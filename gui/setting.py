# coding=utf-8
# 作者: 拓跋龙
# 功能: 设置界面

from PySide6.QtWidgets import QWidget, QGridLayout

class SettingPage(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QGridLayout()

        self.setObjectName('setting_page')
        self.setLayout(self._layout)