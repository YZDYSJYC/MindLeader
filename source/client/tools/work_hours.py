# coding=utf-8
# 作者: 拓跋龙
# 功能: 工时相关功能

import datetime
from dataclasses import dataclass

import chinese_calendar
from PySide6.QtCore import QDate, QTime

from source.util.db import get_config, set_config

@dataclass
class TimeNode:
    business_time: QTime
    flexible_business_time: QTime
    noon_rest_time: QTime
    noon_business_time: QTime
    closing_time: QTime
    afnoon_business_time: QTime
    flexible_closing_time: QTime

classes_time = {
    '8点班次': TimeNode(QTime(8, 0), QTime(9, 5), QTime(12, 0), QTime(13, 30), QTime(17, 30), QTime(18, 0), QTime(19, 5)),
    '8点半班次': TimeNode(QTime(8, 30), QTime(9, 35), QTime(12, 30), QTime(14, 00), QTime(18, 00), QTime(18, 30), QTime(19, 35))
}

def is_work_day(date: QDate) -> tuple[bool, str]:
    try:
        date = datetime.date(date.year(), date.month(), date.day())
        return chinese_calendar.is_workday(date), ''
    except Exception as e:
        return None, ''.join(str(arg) for arg in e.args)

def time_diff(start_time: QTime, end_time: QTime):
    time = start_time.secsTo(end_time) / 3600
    return time if time > 0 else 0

# 正点上班
def eval_standard_hours(start_time: QTime, end_time: QTime, classes='8点班次'):
    if end_time < classes_time[classes].noon_rest_time: # 上午下班
        return time_diff(classes_time[classes].business_time, end_time), time_diff(start_time, end_time)
    elif classes_time[classes].noon_rest_time <= end_time < classes_time[classes].noon_business_time: # 中午下班
        return 4, time_diff(start_time, classes_time[classes].noon_rest_time)
    elif classes_time[classes].noon_business_time <= end_time < classes_time[classes].closing_time: # 下午下班
        return time_diff(classes_time[classes].business_time, end_time) - 1.5, time_diff(start_time, end_time) - 1.5
    elif classes_time[classes].closing_time <= end_time < classes_time[classes].afnoon_business_time: # 下午休息时间下班
        return 8, time_diff(start_time, classes_time[classes].closing_time)
    elif classes_time[classes].afnoon_business_time <= end_time: # 晚上下班
        return 8, time_diff(start_time, end_time) - 2
    return 0, 0

# 弹性上班
def eval_flexible_hours(start_time: QTime, end_time: QTime, classes='8点班次'):
    flexible_closing_time = start_time.addSecs(10 * 3600)
    if end_time < classes_time[classes].noon_rest_time: # 上午下班
        return time_diff(start_time, end_time), time_diff(start_time, end_time)
    elif classes_time[classes].noon_rest_time <= end_time < classes_time[classes].noon_business_time: # 中午下班
        return time_diff(start_time, classes_time[classes].noon_rest_time), time_diff(start_time, classes_time[classes].noon_rest_time)
    elif classes_time[classes].noon_business_time <= end_time < classes_time[classes].closing_time: # 下午下班
        return time_diff(start_time, end_time) - 1.5, time_diff(start_time, end_time) - 1.5
    elif classes_time[classes].closing_time <= end_time < classes_time[classes].afnoon_business_time: # 下午休息时间下班
        return time_diff(start_time, classes_time[classes].closing_time) - 1.5, time_diff(start_time, classes_time[classes].closing_time) - 1.5
    elif classes_time[classes].afnoon_business_time <= end_time < flexible_closing_time: # 傍晚下班
        return time_diff(start_time, end_time) - 2, time_diff(start_time, end_time) - 2
    elif flexible_closing_time <= end_time: # 晚上下班
        return 8, time_diff(start_time, end_time) - 2
    return 0, 0

# 迟到
def eval_other_hours(start_time: QTime, end_time: QTime, classes='8点班次'):
    rest_time = 0
    if start_time < classes_time[classes].noon_rest_time:
        rest_time = 2
    elif classes_time[classes].noon_rest_time <= start_time < classes_time[classes].noon_business_time:
        rest_time = time_diff(start_time, classes_time[classes].noon_business_time) + 0.5
    elif classes_time[classes].noon_business_time <= start_time < classes_time[classes].closing_time:
        rest_time = 0.5
    elif classes_time[classes].closing_time <= start_time < classes_time[classes].afnoon_business_time:
        rest_time = time_diff(start_time, classes_time[classes].afnoon_business_time)

    if end_time < classes_time[classes].noon_rest_time: # 上午下班
        return time_diff(start_time, end_time), time_diff(start_time, end_time)
    elif classes_time[classes].noon_rest_time <= end_time < classes_time[classes].noon_business_time: # 中午下班
        return time_diff(start_time, classes_time[classes].noon_rest_time), time_diff(start_time, classes_time[classes].noon_rest_time)
    elif classes_time[classes].noon_business_time <= end_time < classes_time[classes].closing_time: # 下午下班, 休息时间扣除下午的
        return time_diff(start_time, end_time) - rest_time + 0.5, time_diff(start_time, end_time) - rest_time + 0.5
    elif classes_time[classes].closing_time <= end_time < classes_time[classes].afnoon_business_time: # 下午休息时间下班, 休息时间扣除下午的
        return time_diff(start_time, classes_time[classes].closing_time) - rest_time + 0.5, time_diff(start_time, classes_time[classes].closing_time) - rest_time + 0.5
    elif classes_time[classes].afnoon_business_time <= end_time < classes_time[classes].flexible_closing_time: # 傍晚下班
        return time_diff(start_time, end_time) - rest_time, time_diff(start_time, end_time) - rest_time
    elif classes_time[classes].flexible_closing_time <= end_time: # 晚上下班
        return time_diff(start_time, classes_time[classes].flexible_closing_time) - rest_time, time_diff(start_time, end_time) - rest_time
    return 0, 0

def get_curr_day_work_hours(start_time: QTime=None, end_time: QTime=None, classes='8点班次') -> tuple[float, float]:
    '''
        return: 有效工时, 总工时
    '''
    if not classes_time.get(classes):
        return -1, -1
    if not start_time or not end_time: # 旷工
        return 0, 0
    if start_time > end_time:
        return -1, -1
    # 无效上班
    if end_time < classes_time[classes].business_time or start_time >= classes_time[classes].flexible_closing_time:
        return 0, time_diff(start_time, end_time)
    if start_time < classes_time[classes].business_time:
        return eval_standard_hours(start_time, end_time, classes)
    elif classes_time[classes].business_time <= start_time < classes_time[classes].flexible_business_time:
        return eval_flexible_hours(start_time, end_time, classes)
    else:
        return eval_other_hours(start_time, end_time, classes)

def set_work_hours_to_db(date: QDate, effect_hours: float, total_hours: float, is_work_day: bool):
    work_hours_config = get_config('WorkHours')
    year = date.year()
    month = date.month()
    day = date.day()
    year_config = work_hours_config.get(year)
    if year_config is None:
        work_hours_config[year] = {}
    month_config = work_hours_config[year].get(month)
    if month_config is None:
        work_hours_config[year][month] = {}
    if not is_work_day: # 休息日不计入有效工时
        effect_hours = 0
    work_hours_config[year][month][day] = {'effect_hours': effect_hours, 'total_hours': total_hours}
    set_config('WorkHours', work_hours_config)

def get_work_hours_from_db(date: QDate) -> tuple[float, float]:
    work_hours_config = get_config('WorkHours')
    year = date.year()
    month = date.month()
    day = date.day()
    day_config = work_hours_config.get(year, {}).get(month, {}).get(day, {})
    if not day_config:
        return 0, 0
    return day_config['effect_hours'], day_config['total_hours']

def query_work_hours(year: int, month: int) -> tuple[int, int]:
    work_hours_config = get_config('WorkHours')
    year_config = work_hours_config.get(year)
    if not year_config:
        return 0, 0

    month_config = year_config.get(month)
    if not month_config:
        return 0, 0

    effect_hours = 0
    total_hours = 0
    for v in month_config.values():
        effect_hours += v['effect_hours']
        total_hours += v['total_hours']
    return effect_hours, total_hours