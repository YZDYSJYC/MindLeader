# coding=utf-8
# 作者: 拓跋龙
# 功能: 设置界面

from qfluentwidgets import ExpandLayout, SettingCardGroup, FluentIcon, ConfigItem, QConfig, setTheme, BoolValidator, ScrollArea, \
    HyperlinkCard, PrimaryPushSettingCard, OptionsConfigItem, OptionsValidator
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

from gui.custom_widgets import OptionsSettingCard, SwitchSettingCard, common_signal, StyleSheet
from source.util.common_util import isWin11
from source.util.db import set_config, get_config
from source.util.default_config import README_URL, ISSUE_URL, VERSION, AUTHOR
from source.frame.image_manager import image_theme_update
from source.frame.power_on_startup import register_power_on, delete_power_on

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

        self.add_system_group()
        self.add_presonal_group()
        self.add_update_group()
        self.add_about_group()

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)
        self.setObjectName('setting_page')
        StyleSheet.VIEW_INTERFACE.apply(self, get_config('System', 'Theme'))

    def add_system_group(self):
        self.sys_group = SettingCardGroup('系统', self.scroll_widget)
        self.log_card = OptionsSettingCard(
            OptionsConfigItem('Log', 'LogLevel', 'ERROR', OptionsValidator(['DEBUG', 'INFO', 'ERROR', 'CRITICAL'])),
            FluentIcon.BRUSH,
            '日志级别',
            '设置应用日志级别, 高于或等于此级别点日志才会打印',
            texts=['DEBUG', 'INFO', 'ERROR', 'CRITICAL'],
            parent=self.sys_group
        )
        self.sys_group.addSettingCard(self.log_card)

        self.expand_ayout.addWidget(self.sys_group)

    def add_presonal_group(self):
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

    def add_update_group(self):
        self.update_group = SettingCardGroup('软件更新', self.scroll_widget)
        self.update_start_card = SwitchSettingCard(
            FluentIcon.UPDATE,
            '在应用程序启动时检查更新',
            '新版本功能更全面更稳定（建议启动此选项）',
            configItem= ConfigItem("System", "CheckUpdateAtStartUp", True, BoolValidator()),
            parent=self.update_group
        )

        self.update_start_card.checkedChanged.connect(lambda is_enabled: set_config('System', is_enabled, 'IsUpdateOnStart'))
        self.update_start_card.setValue(get_config('System', 'IsUpdateOnStart'))
        self.update_group.addSettingCard(self.update_start_card)

        self.startup_card = SwitchSettingCard(
            FluentIcon.POWER_BUTTON,
            '设置应用程序在开机时自动启动',
            '开机即可享受到大量功能（建议启动此选项）',
            configItem= ConfigItem("System", "PowerOnStartUp", True, BoolValidator()),
            parent=self.update_group
        )

        self.startup_card.checkedChanged.connect(lambda is_enabled: self.set_enable_power_on_startup(is_enabled))
        self.startup_card.setValue(get_config('System', 'PowerOnStartUp'))
        self.update_group.addSettingCard(self.startup_card)

        self.expand_ayout.addWidget(self.update_group)

    def add_about_group(self):
        self.about_group = SettingCardGroup('关于', self.scroll_widget)
        self.help_card = HyperlinkCard(
            README_URL,
            '打开帮助页面',
            FluentIcon.HELP,
            '帮助',
            '发现新功能并了解有关思维导航的使用技巧',
            self.about_group
        )
        self.feedback_card = PrimaryPushSettingCard(
            '提供反馈',
            FluentIcon.FEEDBACK,
            '提供反馈',
            '通过提供反馈帮助改进思维导航',
            self.about_group
        )
        self.feedback_card.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(ISSUE_URL)))

        self.about_card = PrimaryPushSettingCard(
            '检查更新',
            FluentIcon.INFO,
            '关于',
            f'© Copyright 2024, {AUTHOR}, 版本 {VERSION}\n 特别鸣谢PySide6-Fluent-Widgets提供界面框架支持',
            self.about_group
        )
        self.about_group.addSettingCard(self.help_card)
        self.about_group.addSettingCard(self.feedback_card)
        self.about_group.addSettingCard(self.about_card)

        self.expand_ayout.addWidget(self.about_group)

    def set_theme(self, theme):
        setTheme(theme)
        image_theme_update(theme)
        set_config('System', theme, 'Theme')

    def set_enable_power_on_startup(self, is_enabled):
        set_config('System', is_enabled, 'PowerOnStartUp')
        if is_enabled:
            register_power_on()
        else:
            delete_power_on()