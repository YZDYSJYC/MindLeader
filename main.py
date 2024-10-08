# coding=utf-8
# 作者: 拓跋龙
# 功能: 程序主入口

import sys
import traceback

from qfluentwidgets import FluentTranslator
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLocale

from source.util.log import log_error
from source.util.db import config_init
from source.util.common_util import isWin11
from gui.main_window import MainWindow

# 程序初始化操作
def sys_init():
    config_init()

def main():
    try:
        log_error('程序启动')
        sys_init()

        app = QApplication()
        # 修改在win11高版本阴影异常
        if isWin11():
            app.setStyle('fusion')

        # 设置中文界面
        locale = QLocale(QLocale.Language.Chinese, territory=QLocale.Country.China)
        fluentTranslator = FluentTranslator(locale)
        settingTranslator = QTranslator()
        settingTranslator.load(locale, "settings", ".", "resource/i18n")
        app.installTranslator(fluentTranslator)
        app.installTranslator(settingTranslator)

        application = MainWindow()
        application.show()
        sys.exit(app.exec())
    except SystemExit: # 系统退出会抛出异常, 无需关注
        pass
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()