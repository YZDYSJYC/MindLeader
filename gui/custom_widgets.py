# coding=utf-8
# 作者: 拓跋龙
# 功能: 自定义组件

from typing import Sequence
from enum import Enum
import traceback

import darkdetect
import fuzzywuzzy
import fuzzywuzzy.process
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

        self.tool_list = []

        navitree_frame = QFrame()
        navitree_layout = QGridLayout()

        self.tool_search_edit = qfluentwidgets.LineEdit()
        self.tool_search_edit.setClearButtonEnabled(True)
        # 清空输入框的同时, 列表展示所有项
        self.tool_search_edit.clearButton.clicked.connect(lambda: self.show_all_item())
        navitree_layout.addWidget(self.tool_search_edit, 0, 0, 2, 1)

        self.tool_search_btn = qfluentwidgets.PushButton('搜索')
        self.tool_search_btn.clicked.connect(lambda: self.search_item(self.tool_search_edit.text()))
        navitree_layout.addWidget(self.tool_search_btn, 0, 2, 1, 1)

        navitree_frame.setLayout(navitree_layout)
        self._layout.addWidget(navitree_frame, alignment=Qt.AlignmentFlag.AlignTop)

        self.list_widget = qfluentwidgets.ListWidget(self)
        self._layout.addWidget(self.list_widget)

        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self)

        self.setMaximumWidth(max_width)

    def add_items(self, texts: Sequence[str]):
        self.list_widget.addItems(texts)
        self.tool_list.extend(texts)

    def add_item(self, text):
        self.list_widget.addItem(text)
        self.tool_list.append(text)

    def show_all_item(self):
        self.list_widget.clear()
        self.list_widget.addItems(self.tool_list)

    def search_item(self, s: str):
        if not s:
            return
        try:
            results = fuzzywuzzy.process.extract(s, self.tool_list, limit=10)
            search_result = []
            for result in results:
                if result[1] > 0:
                    search_result.append(result[0])

            self.list_widget.clear()
            self.list_widget.addItems(search_result)
        except Exception:
            traceback.print_exc()