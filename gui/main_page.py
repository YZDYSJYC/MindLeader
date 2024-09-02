# coding=utf-8
# 作者: 拓跋龙
# 功能: 主页

import qfluentwidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout()

        label = qfluentwidgets.TitleLabel()
        label.setText('欢迎使用思维导航!')
        self._layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        theme_switching = qfluentwidgets.ToolButton(qfluentwidgets.FluentIcon.CONSTRACT, self)
        theme_switching.installEventFilter(qfluentwidgets.ToolTipFilter(theme_switching))
        theme_switching.setToolTip('切换主题')
        theme_switching.clicked.connect(lambda: qfluentwidgets.toggleTheme(True))

        self._layout.addWidget(theme_switching)
        self.setObjectName('main_page')
        self.setLayout(self._layout)