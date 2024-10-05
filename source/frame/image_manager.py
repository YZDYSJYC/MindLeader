# coding=utf-8
# 作者: 拓跋龙
# 功能: 图片主题管理

import darkdetect
import weakref
from qfluentwidgets import Theme
from qfluentwidgets.common.style_sheet import CustomStyleSheetWatcher, DirtyStyleSheetWatcher
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject

class ImageManager(QObject):
    """ Style sheet manager """

    def __init__(self):
        self.widgets = weakref.WeakKeyDictionary()

    def register(self, widget: QWidget, callback=None):
        """ register widget to manager

        Parameters
        ----------

        widget: QWidget
            the widget to set style sheet

        callback: bool
            whether to reset the qss source
        """

        if widget not in self.widgets:
            widget.destroyed.connect(self.deregister)
            widget.installEventFilter(CustomStyleSheetWatcher(widget))
            widget.installEventFilter(DirtyStyleSheetWatcher(widget))
            self.widgets[widget] = callback

    def deregister(self, widget: QWidget):
        """ deregister widget from manager """
        if widget not in self.widgets:
            return

        self.widgets.pop(widget)

image_manager = ImageManager()

def register_image(widget, callback=None):
    image_manager.register(widget, callback)

def image_theme_update(theme=Theme.AUTO):
    theme = Theme(darkdetect.theme()) if theme == Theme.AUTO else theme
    for callback in image_manager.widgets.values():
        if callback:
            callback(theme.value.lower())