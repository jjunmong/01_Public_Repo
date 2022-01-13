import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import os
import subprocess
from qt_material import apply_stylesheet, QtStyleTools
import time
import schedule
import functools
from datetime import datetime, date
import traceback
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
import sched

def aa():
    exe = 'C:/01_Python_dev/05_수집툴통합관리/10_1_알리오플러스.exe'
    subprocess.Popen(exe)
    print('aaaaaa')

def reserveCrawl(day_info, time,run):
    today = date.today().day
    if day_info == today:
        return schedule.every().day.at(time).do(run)

reserveCrawl(12,'16:36',aa)
while True :
    schedule.run_pending()

