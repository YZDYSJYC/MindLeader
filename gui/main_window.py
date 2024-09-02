# coding=utf-8
# 作者: 拓跋龙
# 功能: 程序主界面

import qfluentwidgets
from PySide6.QtGui import Qt

from gui.main_page import MainPage
from gui.music import MusicPage
from gui.games.main_page import GamePage
from gui.tools.main_page import ToolPage
from gui.setting import SettingPage

class MainWindow(qfluentwidgets.FluentWindow):
    def __init__(self):
        super().__init__()

        # 设置无边框和透明背景
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.navigationInterface.setExpandWidth(250)
        self.navigationInterface.setCollapsible(True)

        qfluentwidgets.setTheme(qfluentwidgets.Theme.AUTO)

        self.setWindowTitle('思维导航')
        self.add_sub_page()

    def add_sub_page(self):
        self.addSubInterface(MainPage(), qfluentwidgets.FluentIcon.HOME, '主页')
        self.addSubInterface(MusicPage(), qfluentwidgets.FluentIcon.MUSIC, '音乐')
        self.addSubInterface(GamePage(), qfluentwidgets.FluentIcon.GAME, '游戏')
        self.addSubInterface(ToolPage(), qfluentwidgets.FluentIcon.DEVELOPER_TOOLS, '实用工具')
        self.addSubInterface(SettingPage(), qfluentwidgets.FluentIcon.SETTING, '设置', qfluentwidgets.NavigationItemPosition.BOTTOM)