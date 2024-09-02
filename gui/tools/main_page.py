# coding=utf-8
# 作者: 拓跋龙
# 功能: 工具主界面

import qfluentwidgets
from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QLabel, QApplication

from gui.custom_widgets import ListFrame, StyleSheet

class ToolPage(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QHBoxLayout()
        # type: Dict[str, QWidget]
        self.items = {}

        self.tool_list = ListFrame()
        self.tool_list.list_widget.currentTextChanged.connect(lambda text: self.tool_changed(text))
        self._layout.addWidget(self.tool_list)

        self.tool_stack = QStackedWidget()
        StyleSheet.VIEW_INTERFACE.apply(self.tool_stack)
        self._layout.addWidget(self.tool_stack)

        self.setObjectName('tool_page')
        self.setLayout(self._layout)

        self.add_sub_tool('测试1', qfluentwidgets.TitleLabel('测试1'))
        self.add_sub_tool('测试2', qfluentwidgets.TitleLabel('测试2'))

    def add_sub_tool(self, tool_name: str, tool_widget: QWidget):
        if not tool_name:
            print('没有设置工具名称!')
            return
        if tool_name in self.items:
            print('工具名称重复!')
            return
        tool_widget.setProperty("isStackedTransparent", False)
        self.tool_list.add_item(tool_name)
        self.tool_stack.addWidget(tool_widget)
        self.items[tool_name] = tool_widget

    def tool_changed(self, text):
        self.tool_stack.setCurrentWidget(self.items[text])