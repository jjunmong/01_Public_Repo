from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import os
import subprocess
from qt_material import apply_stylesheet, QtStyleTools
import time
import schedule
from datetime import datetime, date, timedelta
import traceback
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
today_day = date.today().day
today_month = date.today().month
today_year = date.today().year

def getDate(y, m, d):
    '''y: year(4 digits)
     m: month(2 digits)
     d: day(2 digits'''
    s = f'{y:04d}-{m:02d}-{d:02d}'
    return datetime.strptime(s, '%Y-%m-%d')

def getWeekNo(y, m, d):
    target = getDate(y, m, d)
    firstday = target.replace(day=1)
    if firstday.weekday() == 6:
        origin = firstday
    elif firstday.weekday() < 3:
        origin = firstday - timedelta(days=firstday.weekday() + 1)
    else:
        origin = firstday + timedelta(days=6 - firstday.weekday())
    return (target - origin).days // 7 + 1


weekNum = getWeekNo(today_year, today_month, today_day)

print(weekNum)