# coding=utf-8
# 作者: 拓跋龙
# 功能: 设置界面

from qfluentwidgets import ExpandLayout, SettingCardGroup, FluentIcon, ConfigItem, QConfig, setTheme, BoolValidator, ScrollArea
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt

from gui.custom_widgets import OptionsSettingCard, SwitchSettingCard, common_signal, StyleSheet
from source.util.common_util import isWin11
from source.util.db import set_config, get_config

class SettingPage(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setting_label = QLabel('设置', self)
        self.setting_label.move(60, 63)
        self.setting_label.setObjectName('settingLabel')

        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName('scrollWidget')
        self.expand_ayout = ExpandLayout(self.scroll_widget)
        self.expand_ayout.setSpacing(28)
        self.expand_ayout.setContentsMargins(60, 10, 60, 0)

        self.personal_group = SettingCardGroup('个性化', self.scroll_widget)
        self.mica_card = SwitchSettingCard(
            FluentIcon.TRANSPARENT,
            '云母效果',
            '窗口和表面显示半透明',
            ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator()),
            self.personal_group
        )
        self.mica_card.checkedChanged.connect(common_signal.mica_enable_changed)
        self.mica_card.setValue(get_config('System', 'MicaEnabled'))

        self.theme_card = OptionsSettingCard(
            QConfig.themeMode,
            FluentIcon.BRUSH,
            '应用主题',
            '调整你的应用外观',
            texts=['浅色', '深色', '跟随系统设置'],
            parent=self.personal_group
        )
        self.theme_card.optionChanged.connect(lambda theme: self.set_theme(theme))
        self.theme_card.setValue(get_config('System', 'Theme'))

        self.personal_group.addSettingCard(self.mica_card)
        self.personal_group.addSettingCard(self.theme_card)

        self.expand_ayout.addWidget(self.personal_group)
        self.setObjectName('setting_page')
        self.setLayout(self.expand_ayout)

        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)
        StyleSheet.VIEW_INTERFACE.apply(self, get_config('System', 'Theme'))

    def set_theme(self, theme):
        setTheme(theme)
        set_config('System', theme, 'Theme')