# coding=utf-8
# 作者: 拓跋龙
# 功能: 进程管理界面

import traceback
import copy
from functools import partial

import fuzzywuzzy.process
from qfluentwidgets import LineEdit, PushButton, ToolButton, FluentIcon, ToolTipFilter, InfoBar, InfoBarPosition
from PySide6.QtWidgets import QWidget, QGridLayout, QAbstractItemView
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from gui.custom_widgets import Table, CustomMessageBox
from source.client.tools.process import get_processes, kill_process
from source.util.log import log_info

class Process(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QGridLayout(self)
        self._layout.setSpacing(10)

        self.process_edit = LineEdit()
        self.process_edit.setClearButtonEnabled(True)
        # 清空输入框的同时, 列表展示所有项
        self.process_edit.clearButton.clicked.connect(lambda: self.show_all_processes())
        self.process_edit.returnPressed.connect(lambda: self.search_process(self.process_edit.text()))
        self._layout.addWidget(self.process_edit, 0, 0, 1, 3)

        self.sreach_btn = PushButton('搜索')
        self.sreach_btn.clicked.connect(lambda: self.search_process(self.process_edit.text()))
        self._layout.addWidget(self.sreach_btn, 0, 3, 1, 1)

        self.refresh_btn = ToolButton(FluentIcon.UPDATE)
        self.refresh_btn.installEventFilter(ToolTipFilter(self.refresh_btn))
        self.refresh_btn.setToolTip('刷新数据')
        self.refresh_btn.clicked.connect(lambda: self.comp_init())
        self._layout.addWidget(self.refresh_btn, 0, 4, 1, 1)

        header = ['进程名称', '进程号', '操作']
        self.process_table = Table(header)
        self.process_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._layout.addWidget(self.process_table, 1, 0, 5, 5)

    def comp_init(self):
        self.processes_info = get_processes()
        datas = self.add_del_btn_to_process(self.processes_info)
        self.process_table.set_data(datas)

    def add_del_btn_to_process(self, datas):
        def delete_process(process_info, index):
            w = CustomMessageBox('确定要删除进程吗', self)
            if w.exec():
                log_info(f'删除的进程名称: {process_info[0]}, 进程id: {process_info[1]}')
                ok = kill_process(process_info[1])
                if ok:
                    self.process_table.removeRow(index)
                else:
                    InfoBar.success(
                        title='删除失败!',
                        content='所选进程不存在, 请重新查询',
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )

        new_datas = copy.deepcopy(datas)
        for index, process_info in enumerate(new_datas):
            btn = PushButton('删除进程')
            btn.clicked.connect(partial(delete_process, process_info, index))
            process_info.append(btn)
        return new_datas

    def search_process(self, s: str):
        try:
            if not s:
                self.show_all_processes()
                return
            results = fuzzywuzzy.process.extract(s, [process_info[0] for process_info in self.processes_info], limit=20)
            search_result = []
            for result in results:
                if result[1] > 0:
                    search_result.append(result[0])

            datas = [] 
            for process_info in self.processes_info:
                if process_info[0] in search_result:
                    datas.append(process_info)

            self.process_table.clear_data()
            datas = self.add_del_btn_to_process(datas)
            self.process_table.set_data(datas)
        except Exception:
            traceback.print_exc()

    def show_all_processes(self):
        self.process_table.clear_data()
        self.process_table.set_data(self.processes_info)