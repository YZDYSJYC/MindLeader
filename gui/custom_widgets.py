# coding=utf-8
# 作者: 拓跋龙
# 功能: 自定义组件

from typing import Sequence, Union, Iterable
from enum import Enum
import traceback

import darkdetect
import fuzzywuzzy.process
from qfluentwidgets import Theme, StyleSheetBase, LineEdit, PushButton, ListWidget, ExpandSettingCard, FluentIconBase, \
    RadioButton, SettingCard, ConfigItem, SwitchButton, IndicatorPosition, TableWidget, MessageBoxBase, SubtitleLabel, \
    InfoBar, InfoBarPosition, CheckBox, PrimaryPushButton, BodyLabel, components, common, DatePickerBase
from qframelesswindow import FramelessDialog, StandardTitleBar
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QFrame, QLabel, QButtonGroup, QTableWidgetItem, QWidget, QHBoxLayout, \
    QSizePolicy, QSpacerItem, QLineEdit, QTextBrowser
from PySide6.QtCore import Qt, Signal, QObject, QSize, QMetaObject, QDate
from PySide6.QtGui import QIcon, QPixmap

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

class LoginStatus(Enum):
    NOT_LOGIN = 0
    LOGINED = 1
    LOGIN_EXPIRE = 2

class LoginDialog(FramelessDialog, object):
    def __init__(self, login_status: LoginStatus):
        super().__init__()
        self.setup_ui()

        self.login_btn.clicked.connect(lambda: self.accept())
        self.titleBar.closeBtn.clicked.connect(lambda: self.reject())

        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.raise_()

        self.label.setScaledContents(False)
        self.setWindowTitle('om_tools登录窗口')
        self.setWindowIcon(QIcon("config/title.ico"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId())
        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)

        if login_status != LoginStatus.NOT_LOGIN:
            self.username_edit.setText(get_config('Personal', 'Username'))
        if login_status == LoginStatus.LOGIN_EXPIRE:
            InfoBar.error(
                title='',
                content='用户名或密码已过期!',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )

    def setup_ui(self):
        self.setObjectName("Form")
        self.resize(1250, 809)
        self.setMinimumSize(QSize(700, 500))

        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.setSpacing(0)
        self.h_layout.setObjectName("h_layout")

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("config/title.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.h_layout.addWidget(self.label)

        self.widget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(360, 0))
        self.widget.setMaximumSize(QSize(360, 16777215))
        self.widget.setStyleSheet("QLabel {font: 13px 'Microsoft YaHei'}")
        self.widget.setObjectName("widget")
        self.v_layout = QVBoxLayout(self.widget)
        self.v_layout.setContentsMargins(20, 20, 20, 20)
        self.v_layout.setSpacing(9)
        self.v_layout.setObjectName("v_layout")
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.v_layout.addItem(spacerItem)
        self.logo_label = QLabel(self.widget)
        self.logo_label.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_label.sizePolicy().hasHeightForWidth())
        self.logo_label.setSizePolicy(sizePolicy)
        self.logo_label.setMinimumSize(QSize(100, 100))
        self.logo_label.setMaximumSize(QSize(100, 100))
        self.logo_label.setPixmap(QPixmap("config/logo.png"))
        self.logo_label.setScaledContents(True)
        self.v_layout.addWidget(self.logo_label, 0, Qt.AlignHCenter)
        spacer_item = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.v_layout.addItem(spacer_item)
        self.gridLayout = QGridLayout()
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(9)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 1)
        self.v_layout.addLayout(self.gridLayout)
        self.user_label = QLabel(self.widget)
        self.user_label.setText("用户名")
        self.v_layout.addWidget(self.user_label)
        self.username_edit = LineEdit(self.widget)
        self.username_edit.setPlaceholderText("请输入w3账户名")
        self.username_edit.setClearButtonEnabled(True)
        self.v_layout.addWidget(self.username_edit)
        self.pwd_label = QLabel(self.widget)
        self.pwd_label.setText("密码")
        self.v_layout.addWidget(self.pwd_label)
        self.password_edit = LineEdit(self.widget)
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setClearButtonEnabled(True)
        self.v_layout.addWidget(self.password_edit)
        spacer_item = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.v_layout.addItem(spacer_item)
        self.is_save_pwd = CheckBox(self.widget)
        self.is_save_pwd.setChecked(True)
        self.is_save_pwd.setText("记住密码")
        self.v_layout.addWidget(self.is_save_pwd)
        spacer_item = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.v_layout.addItem(spacer_item)
        self.login_btn = PrimaryPushButton(self.widget)
        self.login_btn.setText("登录")
        self.v_layout.addWidget(self.login_btn)
        spacer_item = QSpacerItem(20, 6, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.v_layout.addItem(spacer_item)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.v_layout.addItem(spacer_item)
        self.h_layout.addWidget(self.widget)

        QMetaObject.connectSlotsByName(self)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap("config/login_bg.jpg").scaled(
            self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    # 重写accept函数
    def accept(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        if not username or not password:
            InfoBar.error(
                title='',
                content='请填写用户名或密码!',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
            return

        # 校验账号密码
        ret = True
        if not ret:
            InfoBar.error(
                title='',
                content='用户名或密码错误!',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
            return

        if self.is_save_pwd.isChecked():
            pass
        return super().accept()

class InputSetting(QWidget):

    max_tip_label_width = 0

    def __init__(self, tip: str, defalut_text='') -> None:
        super().__init__()
        self._layout = QHBoxLayout(self)

        self.tip_label = BodyLabel(tip)
        self.tip_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        text_width = self.tip_label.fontMetrics().boundingRect(self.tip_label.text()).width()
        if text_width > InputSetting.max_tip_label_width:
            InputSetting.max_tip_label_width = text_width
        self._layout.addWidget(self.tip_label)

        self.line_edit = LineEdit()
        if defalut_text:
            self.line_edit.setPlaceholderText(defalut_text)
        self.line_edit.setClearButtonEnabled(True)
        self._layout.addWidget(self.line_edit)

        self.setting_btn = PushButton('设置')
        self._layout.addWidget(self.setting_btn)

        self.setFixedHeight(50)

class TextBrowser(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layer = components.widgets.line_edit.EditLayer(self)
        self.scrollDelegate = components.widgets.scroll_area.SmoothScrollDelegate(self)
        StyleSheet.VIEW_INTERFACE.apply(self)
        common.font.setFont(self)

    def contextMenuEvent(self, e):
        menu = components.widgets.menu.TextEditMenu(self)
        menu.exec(e.globalPos(), ani=True)

class MonthPicker(DatePickerBase):
    """ Month picker """

    def __init__(self, parent=None):
        """
        Parameters
        ----------
        parent: QWidget
            parent widget

        """
        super().__init__(parent=parent)
        self.YEAR = '年'
        self.MONTH = '月'
        self._year = None
        self._month = None

        self.setYearFormatter(components.date_time.date_picker.ZhYearFormatter())
        self.setMonthFormatter(components.date_time.date_picker.ZhMonthFormatter())
        self.set_month_format()

    def set_month_format(self):
        """ set the format of date

        Parameters
        ----------
        """
        self.clearColumns()
        y = QDate.currentDate().year()

        self.yearIndex = 0
        self.monthIndex = 1

        self.addColumn(self.YEAR, range(y - 1, y + 100),
                        160, formatter=self.yearFormatter())
        self.addColumn(self.MONTH, range(1, 13),
                        120, formatter=self.monthFormatter())

        self.setColumnWidth(self.monthIndex, self._month_column_width())

    def panelInitialValue(self):
        if any(self.value()):
            return self.value()

        date = QDate.currentDate()
        y = self.encodeValue(self.yearIndex, date.year())
        m = self.encodeValue(self.monthIndex, date.month())
        return [y, m]

    def _month_column_width(self):
        fm = self.fontMetrics()
        wm = max(fm.boundingRect(i).width()
                 for i in self.columns[self.monthIndex].items()) + 20

        return max(80, wm)

    def _onConfirmed(self, value: list):
        year = self.decodeValue(self.yearIndex, value[self.yearIndex])
        month = self.decodeValue(self.monthIndex, value[self.monthIndex])
        self.set_date(year, month)

    def get_month(self):
        return self._year, self._month

    def set_date(self, year, month):
        self._year = year
        self._month = month
        self.setColumnValue(self.yearIndex, f'{year}')
        self.setColumnValue(self.monthIndex, f'{month}')

    def set_year_range(self, items: Iterable):
        self.columns[0].setItems(items)