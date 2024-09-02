# coding=utf-8
# 作者: 拓跋龙
# 功能: 游戏主界面

from PySide6.QtWidgets import QWidget, QGridLayout

class GamePage(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QGridLayout()

        self.setObjectName('game_page')
        self.setLayout(self._layout)