# coding=utf-8
# 作者: 拓跋龙
# 功能: 自定义组件

from typing import Sequence, Union
from enum import Enum
import traceback

import darkdetect
import fuzzywuzzy.process
from qfluentwidgets import Theme, StyleSheetBase, LineEdit, PushButton, ListWidget, ExpandSettingCard, FluentIconBase, \
    RadioButton, SettingCard, ConfigItem, SwitchButton, IndicatorPosition, TableWidget, MessageBoxBase, SubtitleLabel
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QFrame, QLabel, QButtonGroup, QTableWidgetItem, QWidget, QApplication
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QIcon

from source.util.db import get_config

class CommonSignal(QObject):
    """ Signal bus """

    mica_enable_changed = Signal(bool)

common_signal = CommonSignal()

# 自定义style
class StyleSheet(StyleSheetBase, Enum):

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

        self.tool_search_edit = LineEdit()
        self.tool_search_edit.setClearButtonEnabled(True)
        # 清空输入框的同时, 列表展示所有项
        self.tool_search_edit.clearButton.clicked.connect(lambda: self.show_all_item())
        navitree_layout.addWidget(self.tool_search_edit, 0, 0, 2, 1)

        self.tool_search_btn = PushButton('搜索')
        self.tool_search_btn.setObjectName('ListFrame')
        self.tool_search_btn.clicked.connect(lambda: self.search_item(self.tool_search_edit.text()))
        navitree_layout.addWidget(self.tool_search_btn, 0, 2, 1, 1)

        navitree_frame.setLayout(navitree_layout)
        self._layout.addWidget(navitree_frame, alignment=Qt.AlignmentFlag.AlignTop)

        self.list_widget = ListWidget(self)
        self._layout.addWidget(self.list_widget)

        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self, get_config('System', 'Theme'))

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

class OptionsSettingCard(ExpandSettingCard):
    """ setting card with a group of options """

    optionChanged = Signal(Enum)

    def __init__(self, configItem, icon: Union[str, QIcon, FluentIconBase], title, content=None, texts=None, parent=None):
        """
        Parameters
        ----------
        configItem: Enum
            options config item

        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of setting card

        content: str
            the content of setting card

        texts: List[str]
            the texts of radio buttons

        parent: QWidget
            parent window
        """
        super().__init__(icon, title, content, parent)
        self.texts = texts or []
        self.configItem = configItem
        self.configName = configItem.name
        self.choiceLabel = QLabel(self)
        self.buttonGroup = QButtonGroup(self)

        self.addWidget(self.choiceLabel)

        # create buttons
        self.viewLayout.setSpacing(19)
        self.viewLayout.setContentsMargins(48, 18, 0, 18)
        for text, option in zip(texts, configItem.options):
            button = RadioButton(text, self.view)
            self.buttonGroup.addButton(button)
            self.viewLayout.addWidget(button)
            button.setProperty(self.configName, option)

        self._adjustViewSize()
        self.buttonGroup.buttonClicked.connect(self.__onButtonClicked)

    def __onButtonClicked(self, button: RadioButton):
        """ button clicked slot """
        if button.text() == self.choiceLabel.text():
            return

        value = button.property(self.configName)

        self.choiceLabel.setText(button.text())
        self.choiceLabel.adjustSize()
        self.optionChanged.emit(value)

    def setValue(self, value):
        """ select button according to the value """
        for button in self.buttonGroup.buttons():
            isChecked = button.property(self.configName) == value
            button.setChecked(isChecked)

            if isChecked:
                self.choiceLabel.setText(button.text())
                self.choiceLabel.adjustSize()
                break

class SwitchSettingCard(SettingCard):
    """ Setting card with switch button """

    checkedChanged = Signal(bool)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None,
                 configItem: ConfigItem = None, parent=None):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        configItem: ConfigItem
            configuration item operated by the card

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)
        self.configItem = configItem
        self.switchButton = SwitchButton('关', self, IndicatorPosition.RIGHT)

        if configItem:
            configItem.valueChanged.connect(self.setValue)

        # add switch button to layout
        self.hBoxLayout.addWidget(self.switchButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.switchButton.checkedChanged.connect(self.__onCheckedChanged)

    def __onCheckedChanged(self, isChecked: bool):
        """ switch button checked state changed slot """
        self.setValue(isChecked)
        self.checkedChanged.emit(isChecked)

    def setValue(self, isChecked: bool):
        self.switchButton.setChecked(isChecked)
        self.switchButton.setText('开' if isChecked else '关')

    def setChecked(self, isChecked: bool):
        self.setValue(isChecked)

    def isChecked(self):
        return self.switchButton.isChecked()

class Table(TableWidget):
    def __init__(self, header: list[str], parent=None):
        super().__init__(parent)
        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)
        self.header_len = len(header)
        self.setColumnCount(self.header_len)
        self.setHorizontalHeaderLabels(header)

    def set_data(self, datas: list):
        self.setRowCount(len(datas))
        for i, data in enumerate(datas):
            for j in range(self.header_len):
                if isinstance(data[j], QWidget):
                    self.setCellWidget(i, j, data[j])
                else:
                    self.setItem(i, j, QTableWidgetItem(str(data[j])))
        self.resizeColumnsToContents()

    def clear_data(self):
        self.clearContents()
        self.setRowCount(0)

class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, content: str, parent=None):
        super().__init__(parent)
        self.title_label = SubtitleLabel(content, self)

        # add widget to view layout
        self.viewLayout.addWidget(self.title_label)

        # change the text of button
        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(360)