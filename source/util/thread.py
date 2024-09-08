# coding=utf-8
# 作者: 拓跋龙
# 功能: 多线程功能

from typing import Any

from PySide6.QtCore import Signal, QThread

class Asynchronous(QThread):

    finish = Signal(Any)

    def __init__(self, callback, args: list=None, parent=None) -> None:
        super().__init__(parent)
        self.callback = callback
        self.args = args

    def run(self):
        if self.args:
            ret = self.callback(self.args)
        else:
            ret = self.callback()

        self.finish.emit(ret)