# coding=utf-8
# 作者: 拓跋龙
# 功能: 多线程功能

from typing import Any

from PySide6.QtCore import Signal, QThread

class Asynchronous(QThread):

    finish_signal = Signal()

    def __init__(self, callback, stop_func, args: list=None) -> None:
        super(Asynchronous, self).__init__()
        self.callback = callback
        self.args = args
        self.ret = None
        self.finish_signal.connect(lambda: stop_func(self, self.ret)) # 线程销毁信号

    def run(self):
        if self.args:
            self.ret = self.callback(self.args)
        else:
            self.ret = self.callback()
        self.finish_signal.emit()
