# coding=utf-8
# 作者: 拓跋龙
# 功能: 程序主界面

import ctypes
from typing import override

import qfluentwidgets
from PySide6.QtWidgets import QApplication, QWidget, QSystemTrayIcon
from PySide6.QtGui import Qt, QIcon

from gui.custom_widgets import common_signal
from gui.main_page import MainPage
from gui.music import MusicPage
from gui.games.main_page import GamePage
from gui.tools.main_page import ToolPage
from gui.setting import SettingPage
from source.util.db import get_config, set_config

class MainWindow(qfluentwidgets.FluentWindow):
    def __init__(self):
        super().__init__()

        # 设置无边框和透明背景
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.navigationInterface.setExpandWidth(250)
        self.navigationInterface.setCollapsible(True)

        theme = get_config('System', 'Theme')
        qfluentwidgets.setTheme(theme)

        self.setWindowTitle('思维导航')
        ico = QIcon('config/title.ico')
        self.setWindowIcon(ico)
        # 设置任务栏图标
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

        self.setMicaEffectEnabled(get_config('System', 'MicaEnabled'))
        self.add_sub_page()

        # 居中显示, 默认显示在屏幕1
        desktop = QApplication.screens()[0].availableGeometry()
        self.resize(1000, 800)
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

        self.connect_signal_slot()

    def add_sub_page(self):
        self.addSubInterface(MainPage(), qfluentwidgets.FluentIcon.HOME, '主页')
        self.addSubInterface(MusicPage(), qfluentwidgets.FluentIcon.MUSIC, '音乐')
        self.addSubInterface(GamePage(), qfluentwidgets.FluentIcon.GAME, '游戏')
        self.addSubInterface(ToolPage(), qfluentwidgets.FluentIcon.DEVELOPER_TOOLS, '实用工具')
        self.addSubInterface(SettingPage(), qfluentwidgets.FluentIcon.SETTING, '设置', qfluentwidgets.NavigationItemPosition.BOTTOM)

    def connect_signal_slot(self):
        common_signal.mica_enable_changed.connect(lambda is_enabled: self.enable_changed(is_enabled))

    @override
    def switchTo(self, interface: QWidget):
        self.stackedWidget.setCurrentWidget(interface, popOut=False)
        # 点击对应功能时再初始化数据, 提升启动性能
        if hasattr(interface, 'comp_init'):
            mothed = getattr(interface, 'comp_init')
            mothed()

    def enable_changed(self, is_enabled: bool):
        self.setMicaEffectEnabled(is_enabled)
        set_config('System', is_enabled, 'MicaEnabled')