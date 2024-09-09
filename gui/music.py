# coding=utf-8
# 作者: 拓跋龙
# 功能: 音乐界面

from PySide6.QtWidgets import QWidget, QVBoxLayout

class MusicPage(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout(self)
        self.setObjectName('music_page')

    def add_top_widgets(self):
        pass

    def add_mid_widgets(self):
        pass

    def add_bottom_widgets(self):
        pass