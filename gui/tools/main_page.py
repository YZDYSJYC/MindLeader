# coding=utf-8
# 作者: 拓跋龙
# 功能: 工具主界面

from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QLabel, QApplication

from gui.custom_widgets import ListFrame, StyleSheet
from gui.tools.process import Process
from gui.tools.sys_info import SysInfo
from gui.tools.work_hours import WorkHours
from source.util.db import get_config

class ToolPage(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QHBoxLayout()
        # type: Dict[str, QWidget]
        self.items = {}

        self.tool_list = ListFrame(250)
        self.tool_list.list_widget.currentTextChanged.connect(lambda text: self.tool_changed(text))
        self._layout.addWidget(self.tool_list)

        self.tool_stack = QStackedWidget()
        StyleSheet.VIEW_INTERFACE.apply(self.tool_stack, get_config('System', 'Theme'))
        self._layout.addWidget(self.tool_stack)

        self.setObjectName('tool_page')
        self.setLayout(self._layout)

        self.add_sub_tools()

    def add_sub_tools(self):
        self.sys_finfo = SysInfo()
        self.add_sub_tool('系统信息', self.sys_finfo)
        self.process = Process()
        self.add_sub_tool('进程管理', self.process)
        self.work_hours = WorkHours()
        self.add_sub_tool('工时记录', self.work_hours)

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
        interface = self.tool_stack.currentWidget()
        # 点击对应功能时再初始化数据, 提升启动性能
        if hasattr(interface, 'comp_init'):
            mothed = getattr(interface, 'comp_init')
            mothed()