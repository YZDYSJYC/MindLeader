# coding=utf-8
# 作者: 拓跋龙
# 功能: 自定义组件

from typing import Sequence
from enum import Enum

import darkdetect
import qfluentwidgets
from qfluentwidgets import Theme
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QFrame
from PySide6.QtCore import Qt

# 自定义style
class StyleSheet(qfluentwidgets.StyleSheetBase, Enum):

    VIEW_INTERFACE = "view_interface"

    def path(self, theme=Theme.AUTO):
        theme = Theme(darkdetect.theme()) if theme == Theme.AUTO else theme
        return f"./gui/qss/{theme.value.lower()}/{self.value}.qss"

class ListFrame(QFrame):
    def __init__(self, max_width=300):
        super().__init__()
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.setObjectName('frame')

        navitree_frame = QFrame()
        navitree_layout = QGridLayout()

        self.tool_search_edit = qfluentwidgets.LineEdit()
        self.tool_search_edit.setClearButtonEnabled(True)
        navitree_layout.addWidget(self.tool_search_edit, 0, 0, 2, 1)

        self.too_searh_btn = qfluentwidgets.PushButton('搜索')
        navitree_layout.addWidget(self.too_searh_btn, 0, 2, 1, 1)

        navitree_frame.setLayout(navitree_layout)
        self._layout.addWidget(navitree_frame, alignment=Qt.AlignmentFlag.AlignTop)

        self.list_widget = qfluentwidgets.ListWidget(self)
        self._layout.addWidget(self.list_widget)

        StyleSheet.VIEW_INTERFACE.apply(self)

        self.setMaximumWidth(max_width)

    def add_items(self, texts: Sequence[str]):
        self.list_widget.addItems(texts)

    def add_item(self, text):
        self.list_widget.addItem(text)