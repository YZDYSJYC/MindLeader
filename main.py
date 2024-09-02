# coding=utf-8
# 作者: 拓跋龙
# 功能: 程序住入口

import sys
import traceback

from PySide6.QtWidgets import QApplication

from source.frame.log import log_error
from gui.main_window import MainWindow

def main():
    try:
        log_error('程序启动')
        app = QApplication()
        # 修改在win11高版本阴影异常
        if sys.platform == 'win32' and sys.getwindowsversion().build >= 22000:
            app.setStyle('fusion')
        application = MainWindow()
        application.show()
        sys.exit(app.exec())
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()