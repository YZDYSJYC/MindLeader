# coding=utf-8
# 作者: 拓跋龙
# 功能: 工时记录界面

from qfluentwidgets import SubtitleLabel, TimePicker, BodyLabel, PushButton, ComboBox, TextEdit
from qfluentwidgets.components.date_time.calendar_view import DayCalendarView
from PySide6.QtWidgets import QWidget, QGridLayout, QApplication
from PySide6.QtCore import Qt, QDate

from gui.custom_widgets import MonthPicker
from source.client.tools.work_hours import is_work_day, set_work_hours_to_db, get_curr_day_work_hours, get_work_hours_from_db, \
    query_work_hours

class WorkHours(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QGridLayout(self)
        self._layout.setSpacing(10)
        self.clicked_day = QDate.currentDate()

        self._date = DayCalendarView()
        self._date.itemClicked.connect(lambda date: self.set_date_type(date))
        self._layout.addWidget(self._date, 0, 0, 5, 3, alignment=Qt.AlignmentFlag.AlignTop)

        self.date_type = SubtitleLabel()
        self._layout.addWidget(self.date_type, 0, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.info_label = SubtitleLabel()
        self._layout.addWidget(self.info_label, 0, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        tmp_label = BodyLabel('请选择班次:')
        self._layout.addWidget(tmp_label, 1, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)

        self._select_work_type = ComboBox()
        self._select_work_type.addItems(['8点班次', '8点半班次'])
        self._layout.addWidget(self._select_work_type, 1, 5, 1, 1)

        self._start_time = TimePicker()
        self._layout.addWidget(self._start_time, 2, 3, 1, 1)

        tmp_label = BodyLabel('-')
        self._layout.addWidget(tmp_label, 2, 4, 1, 1)

        self._end_time = TimePicker()
        self._layout.addWidget(self._end_time, 2, 5, 1, 1)

        self._set_work_hours = PushButton('设置工时')
        self._set_work_hours.clicked.connect(lambda: self.set_work_hours())
        self._layout.addWidget(self._set_work_hours, 3, 3, 1, 3)

        self._month_select = MonthPicker()
        self._layout.addWidget(self._month_select, 4, 3, 1, 1)

        self._show_work_hours = PushButton('查看工时')
        self._show_work_hours.clicked.connect(lambda: self.counter_work_hours())
        self._layout.addWidget(self._show_work_hours, 4, 5, 1, 1)

        self.oled_screen = TextEdit()
        self.oled_screen.setReadOnly(True)
        self._layout.addWidget(self.oled_screen, 6, 0, 5, 6)

    def comp_init(self):
        self.set_date_type(QDate.currentDate())

    def set_date_type(self, date):
        self.clicked_day = date
        ret, not_ok = is_work_day(date)
        if not_ok:
            self.date_type.setText(not_ok)
            return
        if ret:
            self.date_type.setText('工作日')
            self.is_work_day = True
        else:
            self.date_type.setText('休息日')
            self.is_work_day = False

        effect_hours, _ = get_work_hours_from_db(self.clicked_day)
        self.set_info_label(effect_hours)

    def set_work_hours(self):
        effect_hours, total_hours = get_curr_day_work_hours(self._start_time.getTime(), self._end_time.getTime())
        if effect_hours < 0:
            self.print_msg('时间异常, 请检查后重新设置!')
            return
        set_work_hours_to_db(self.clicked_day, effect_hours, total_hours, self.is_work_day)
        self.set_info_label(effect_hours)
        if effect_hours == 0 and total_hours == 0:
            self.print_msg('当日工时已清空')
        else:
            self.print_msg('设置成功')

    def set_info_label(self, effect_hours):
        if self.is_work_day:
            if effect_hours == 0:
                self.info_label.setText('今天旷工，牛马还不努力')
            else:
                self.info_label.setText(f'今天工时:{round(effect_hours, 2)}小时')
        else:
            self.info_label.setText('请好好放松')

    def counter_work_hours(self):
        year, month = self._month_select.get_month()
        if not year or not month:
            self.print_msg('请选择年份和月份进行查询')
            return
        effect_hours, total_hours = query_work_hours(year, month)
        self.print_msg(f'{year}年{month}月的有效工时为: {effect_hours}, 总工时为: {total_hours}')

    def print_msg(self, text):
        self.oled_screen.setPlainText(text)
        QApplication.processEvents() # 立即刷新界面