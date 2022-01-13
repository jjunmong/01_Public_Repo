# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\01_Python_dev\05_수집툴통합관리\protoType.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

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

DEFAULT_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: lightskyblue;
    width: 10px;
    margin: 1px;
}
"""
LIST_STYLE = """
QListWidget
{
border : 2px solid turquoise;
}
"""

today_day = date.today().day
today_month = date.today().month
today_year = date.today().year

dateDict = {0: '월', 1:'화', 2:'수', 3:'목', 4:'금', 5:'토', 6:'일'}
date = date.today()
datetime_date = datetime.strptime(str(date), '%Y-%m-%d')
today_date = dateDict[date.weekday()]

class Ui_Collect_Manager(object):
    def setupUi(self, Collect_Manager):
        Collect_Manager.setObjectName("Collect_Manager")
        Collect_Manager.resize(1200, 800)
        Collect_Manager.setAutoFillBackground(False)
        apply_stylesheet(app, theme='dark_cyan.xml')
        self.gridLayout = QtWidgets.QGridLayout(Collect_Manager)
        self.gridLayout.setObjectName("gridLayout")
        self.monthLabel = QtWidgets.QLabel(Collect_Manager)
        self.monthLabel.setAutoFillBackground(True)
        self.monthLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.monthLabel.setObjectName("monthLabel")
        self.monthLabel.setStyleSheet("font-size: 15pt;")
        self.gridLayout.addWidget(self.monthLabel, 0, 0, 1, 1)
        self.weekLabel = QtWidgets.QLabel(Collect_Manager)
        self.weekLabel.setStyleSheet("font-size: 15pt;")
        self.weekLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.weekLabel.setObjectName("weekLabel")
        self.weekLabel.setStyleSheet("font-size: 15pt;")
        self.gridLayout.addWidget(self.weekLabel, 0, 1, 1, 1)
        self.dayLabel = QtWidgets.QLabel(Collect_Manager)
        self.dayLabel.setStyleSheet("font-size: 15pt;")
        self.dayLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dayLabel.setObjectName("dayLabel")
        self.gridLayout.addWidget(self.dayLabel, 0, 2, 1, 1)
        self.dayLabel_2 = QtWidgets.QLabel(Collect_Manager)
        self.dayLabel_2.setStyleSheet("")
        self.dayLabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.dayLabel_2.setObjectName("dayLabel_2")
        self.dayLabel_2.setStyleSheet("font-size: 15pt;")
        self.gridLayout.addWidget(self.dayLabel_2, 0, 3, 1, 1)
        self.timeLabel = QtWidgets.QLabel(Collect_Manager)
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setStyleSheet("font-size: 15pt;")
        self.timeLabel.setObjectName("timeLabel")
        self.gridLayout.addWidget(self.timeLabel, 0, 4, 1, 1)
        self.reserveStart = QtWidgets.QPushButton(Collect_Manager)
        self.reserveStart.setStyleSheet("")
        self.reserveStart.setObjectName("reserveStart")
        self.gridLayout.addWidget(self.reserveStart, 0, 5, 1, 1)
        self.toolListLoad = QtWidgets.QPushButton(Collect_Manager)
        self.toolListLoad.setStyleSheet("")
        self.toolListLoad.setObjectName("toolListLoad")
        self.gridLayout.addWidget(self.toolListLoad, 0, 6, 1, 1)
        self.start = QtWidgets.QPushButton(Collect_Manager)
        self.start.setStyleSheet("")
        self.start.setObjectName("start")
        self.gridLayout.addWidget(self.start, 0, 7, 1, 1)
        self.MonthCombobox = QtWidgets.QComboBox(Collect_Manager)
        self.MonthCombobox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.MonthCombobox.setEditable(False)
        self.MonthCombobox.setCurrentText("")
        self.MonthCombobox.setObjectName("MonthCombobox")
        self.MonthCombobox.addItem('')
        self.MonthCombobox.addItem('매월')
        self.gridLayout.addWidget(self.MonthCombobox, 1, 0, 1, 1)
        self.WeekCombobox = QtWidgets.QComboBox(Collect_Manager)
        self.WeekCombobox.setCurrentText("")
        self.WeekCombobox.setObjectName("WeekCombobox")
        self.gridLayout.addWidget(self.WeekCombobox, 1, 1, 1, 1)
        self.WeekCombobox.addItem('')
        self.WeekCombobox.addItem('매주')
        self.WeekCombobox.addItem('격주')
        self.WeekCombobox.addItem('1/3주')
        self.WeekCombobox.addItem('2/4주')
        self.WeekCombobox.addItem('1주')
        self.WeekCombobox.addItem('2주')
        self.WeekCombobox.addItem('3주')
        self.WeekCombobox.addItem('4주')
        self.DayOfWeekcombobox = QtWidgets.QComboBox(Collect_Manager)
        self.DayOfWeekcombobox.setCurrentText("")
        self.DayOfWeekcombobox.setObjectName("DayOfWeekcombobox")
        self.gridLayout.addWidget(self.DayOfWeekcombobox, 1, 2, 1, 1)
        self.DayOfWeekcombobox.addItem('')
        self.DayOfWeekcombobox.addItem('월')
        self.DayOfWeekcombobox.addItem('화')
        self.DayOfWeekcombobox.addItem('수')
        self.DayOfWeekcombobox.addItem('목')
        self.DayOfWeekcombobox.addItem('금')
        self.DayOfWeekcombobox.addItem('토')
        self.DayOfWeekcombobox.addItem('일')
        self.dayComboBox = QtWidgets.QSpinBox(Collect_Manager)
        self.dayComboBox.setMinimum(0)
        self.dayComboBox.setMaximum(31)
        self.dayComboBox.setObjectName("dayComboBox")
        self.gridLayout.addWidget(self.dayComboBox, 1, 3, 1, 1)
        self.timeBox = QtWidgets.QTimeEdit(Collect_Manager)
        self.timeBox.setDisplayFormat("hh:mm")
        self.timeBox.setObjectName("timeBox")
        self.gridLayout.addWidget(self.timeBox, 1, 4, 1, 1)
        self.setUpSave = QtWidgets.QPushButton(Collect_Manager)
        self.setUpSave.setObjectName("setUpSave")
        self.gridLayout.addWidget(self.setUpSave, 1, 5, 1, 1)
        self.ListReset = QtWidgets.QPushButton(Collect_Manager)
        self.ListReset.setObjectName("ListReset")
        self.gridLayout.addWidget(self.ListReset, 1, 6, 1, 1)
        self.exit = QtWidgets.QPushButton(Collect_Manager)
        self.exit.setObjectName("exit")
        self.gridLayout.addWidget(self.exit, 1, 7, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Collect_Manager)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 3, 5, 1, 3)
        self.listWidget = QtWidgets.QListWidget(Collect_Manager)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet(LIST_STYLE)
        self.gridLayout.addWidget(self.listWidget, 2, 0, 2, 5)
        self.progressBar = QtWidgets.QProgressBar(Collect_Manager)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet(DEFAULT_STYLE)
        self.gridLayout.addWidget(self.progressBar, 2, 5, 1, 3)

        self.retranslateUi(Collect_Manager)
        QtCore.QMetaObject.connectSlotsByName(Collect_Manager)

        self.toolListLoad.clicked.connect(self.fileOpneButtonClick)
        self.start.clicked.connect(self.runExeList)
        self.exit.clicked.connect(self.stockExit)
        self.ListReset.clicked.connect(self.removeList)
        self.listWidget.itemClicked.connect(self.clickItem)
        self.setUpSave.clicked.connect(self.clickSetUpSave)
        self.reserveStart.clicked.connect(self.cliclkReserveStart)

    def retranslateUi(self, Collect_Manager):
        _translate = QtCore.QCoreApplication.translate
        Collect_Manager.setWindowTitle(_translate("Collect_Manager", "Collect_Manager"))
        self.monthLabel.setText(_translate("Collect_Manager", "Month주기"))
        self.weekLabel.setText(_translate("Collect_Manager", "Week주기"))
        self.dayLabel_2.setText(_translate("Collect_Manager", "Day"))
        self.dayLabel.setText(_translate("Collect_Manager", "요일"))
        self.timeLabel.setText(_translate("Collect_Manager", "Time"))
        self.reserveStart.setToolTip(_translate("Collect_Manager", "불러온 리스트의 예약 실행 정보에 따라 자동으로 수집 합니다."))
        self.reserveStart.setText(_translate("Collect_Manager", "예약 실행"))
        self.toolListLoad.setText(_translate("Collect_Manager", "수집 툴 불러오기"))
        self.start.setToolTip(_translate("Collect_Manager", "불러와진 수집 툴을 순서대로 실행 합니다."))
        self.start.setText(_translate("Collect_Manager", "시 작"))
        self.setUpSave.setToolTip(_translate("Collect_Manager", "선택한 툴의 예약 실행 정보를 저장 합니다."))
        self.setUpSave.setText(_translate("Collect_Manager", "설정 저장"))
        self.ListReset.setToolTip(_translate("Collect_Manager", "불러온 툴 리스트를 초기화 합니다."))
        self.ListReset.setText(_translate("Collect_Manager", "리스트 초기화"))
        self.exit.setText(_translate("Collect_Manager", "종 료"))

    def stockExit(self):#종료 버튼.
        if os.path.isfile('exe_list.txt'):
            os.remove('exe_list.txt')
        sys.exit(0)

    def errorLog(self,error: str):
        current_time = time.strftime("%Y.%m.%d/%H:%M:%S", time.localtime(time.time()))
        return (f"[{current_time}] - {error}\n")

    def fileOpneButtonClick(self):# 수집툴 불러오기 버튼 클릭 시
        try:
            if os.path.isfile('exe_list.txt'):
                os.remove('exe_list.txt')

            file_name = QtWidgets.QFileDialog.getOpenFileNames()
            for file in file_name[0]:
                self.listWidget.addItem(file)
                with open('exe_list.txt', 'a') as f:
                    f.write(file + '\n')
                f.close()
        except :
            err = traceback.format_exc()
            QMessageBox.warning(Collect_Manager,'Error',self.errorLog(str(err)))

    def runExeList(self):# list 위젯에 추가된 실행 파일 목록들 실행.
        try:
            with open('exe_list.txt') as data:
                lines = data.read().splitlines()
            inputName = lines

            self.progressBar.setMaximum(len(inputName))
            count = 1
            for exe in inputName:
                self.progressBar.setValue(count)
                self.textBrowser.append(exe + ' 수집중')
                run = subprocess.Popen(exe)
                run.wait()
                QtWidgets.QApplication.processEvents()
                count += 1
            data.close()
            os.remove('exe_list.txt')
            self.textBrowser.append('전체 수집 종료')
            print('전체 수집 종료')
        except:
            err = traceback.format_exc()
            QMessageBox.warning(Collect_Manager, 'Error', self.errorLog(str(err)))

    def removeList(self): # 리스트위젯, 텍스트 브라우저 리스트 클리어
        try:
            self.listWidget.clear()
            self.textBrowser.clear()
        except:
            err = traceback.format_exc()
            QMessageBox.warning(Collect_Manager,'Error',self.errorLog(str(err)))

    def clickItem(self):#리스트 위젯의 아이템을 클릭 하면 해당 exe 의 crawl_schedule_config.txt 에 저장된 스케쥴링 값이 뜨게 연결
        try:
            select_exe = str(self.listWidget.currentItem().text()).split('/')
            sep_len = len(select_exe)
            loc_num = sep_len - 1
            exe_name = select_exe[loc_num]

            with open('crawl_schedule_config.txt', 'r', encoding='utf-8') as file:
                schedule_list = file.readlines()

            def find_schedule_value():#선택한 툴 명칭을 config 텍스트 파일에서 찾고 해당 줄을 리턴
                n=0
                while True:
                    if exe_name in schedule_list[n]:
                        return schedule_list[n]
                    n+=1
            schedule_value = find_schedule_value().replace('\n','')

            month = schedule_value.split('|')[1]
            week = schedule_value.split('|')[2]
            datOfWeek = schedule_value.split('|')[3]
            day = int(schedule_value.split('|')[4])
            time = schedule_value.split('|')[5]
            H = int(time.split(':')[0])
            M = int(time.split(':')[1])

            self.MonthCombobox.setCurrentText(month)
            self.WeekCombobox.setCurrentText(week)
            self.DayOfWeekcombobox.setCurrentText(datOfWeek)
            self.dayComboBox.setValue(day)
            self.timeBox.setTime(QtCore.QTime(H,M))
        except:
            err = traceback.format_exc()
            QMessageBox.warning(Collect_Manager,'Error',self.errorLog(str(err)))

    def clickSetUpSave(self):#현재 화면에서 세팅된 값을 읽어서 config 파일에 덮어쓰기.
        try:
            select_exe = str(self.listWidget.currentItem().text()).split('/')
            sep_len = len(select_exe)
            loc_num = sep_len - 1
            exe_name = select_exe[loc_num]

            month = self.MonthCombobox.currentText()
            week = self.WeekCombobox.currentText()
            dayOfweek = self.DayOfWeekcombobox.currentText()
            day = str(self.dayComboBox.value())
            time = self.timeBox.time().toString('hh:mm')
            savelLine = exe_name+'|'+month+'|'+week+'|'+dayOfweek+'|'+day+'|'+time+'\n'

            with open('crawl_schedule_config.txt', 'r', encoding='utf-8') as file:
                schedule_list = file.readlines()

            def findScheduleList():#선택한 툴 명칭을 config 텍스트 파일에서 찾고 해당 줄을 리턴
                n=0
                while True:
                    if exe_name in schedule_list[n]:
                        return n
                    n+=1

            def replace_line(file_name, line_num, text):#수정된 텍스트를 해당 위치로 덮어쓰기.
                lines = open(file_name, 'r', encoding='utf-8').readlines()
                lines[line_num] = text
                out = open(file_name, 'w',encoding='utf-8')
                out.writelines(lines)
                out.close()

            replace_line('crawl_schedule_config.txt',findScheduleList(),savelLine)
        except:
            err = traceback.format_exc()
            QMessageBox.warning(Collect_Manager,'Error',self.errorLog(str(err)))

    def cliclkReserveStart(self):
        self.getRepeatList()
        self.textBrowser.append(str(date.today())+' | '+'수집 대기 중')

        while True:
            schedule.run_pending()
            QtWidgets.QApplication.processEvents()

    def getRepeatList(self):#예약 실행 버튼 클릭 시 crawl_schedule_config.txt 에서 값을 읽어와서 예약 실행 수행.
        try:
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

            def exportRunList():#exe 리스트에 맞는 config값을 더해서 리스트로 반환.
                with open('exe_list.txt', 'r', encoding='cp949') as exe_data:
                    exe_name = exe_data.read().splitlines()
                with open('crawl_schedule_config.txt', 'r', encoding='utf-8') as config_data:
                    config_list = config_data.read().splitlines()
                result = []
                for i in exe_name:
                    n = len(i.split('/')) - 1
                    a = i.split('/')[n]
                    for j in config_list:
                        if a in j:
                            sum_all = i + '|' + j
                            result.append(sum_all)
                exe_data.close()
                config_data.close()
                print(result)
                return result

            def run_crawl(exe):
                subprocess.Popen(exe)

            def reserveCrawl(month, week, dayOfweek, day_info, time, exe):  # param 값을 받아서 예약 실행.

                print('월 : '+month, '주 : '+week, '요일 : '+dayOfweek, '일 : '+day_info, '시간 : '+time, today_day)
                weekNum = getWeekNo(today_year, today_month, today_day)
                time_info = '{}'.format(time)
                hh = int(time_info.split(':')[0])
                mm = int(time_info.split(':')[1])
                run_time = str(today_year)+'-'+str(today_month)+'-'+str(today_day)+' '+str(hh)+':'+str(mm)+':'+'00'
                try:
                    sched = BackgroundScheduler()
                    sched.start()
                    if month == '매월' and int(day_info) == int(today_day): schedule.every().day.at(time_info).do(run_crawl,exe)

                    if week == '매주' and dayOfweek == '월': schedule.every().monday.at(time_info).do(run_crawl,exe)
                    if week == '매주' and dayOfweek == '화': schedule.every().tuesday.at(time_info).do(run_crawl,exe)
                    if week == '매주' and dayOfweek == '수': schedule.every().wednesday.at(time_info).do(run_crawl,exe)
                    if week == '매주' and dayOfweek == '목': schedule.every().thursday.at(time_info).do(run_crawl,exe)
                    if week == '매주' and dayOfweek == '금': schedule.every().friday.at(time_info).do(run_crawl,exe)
                    if week == '매주' and dayOfweek == '토': schedule.every().saturday.at(time_info).do(run_crawl,exe)
                    if week == '매주' and dayOfweek == '일': schedule.every().sunday.at(time_info).do(run_crawl,exe)

                    if week == '격주' and dayOfweek == today_date: sched.add_job(run_crawl(exe), "interval", days="7", start_date=run_time)

                    if week == '1/3주' and weekNum in (1,3) and dayOfweek == today_date: sched.add_job(run_crawl(exe), "date", run_date=run_time)
                    if week == '2/4주' and weekNum in (2,4) and dayOfweek == today_date: sched.add_job(run_crawl(exe), "date", run_date=run_time)

                    if week == '1주' and weekNum == 1 and dayOfweek == today_date: sched.add_job(run_crawl(exe), "date", run_date=run_time)
                    if week == '2주' and weekNum == 2 and dayOfweek == today_date: sched.add_job(run_crawl(exe), "date", run_date=run_time)
                    if week == '3주' and weekNum == 3 and dayOfweek == today_date: sched.add_job(run_crawl(exe), "date", run_date=run_time)
                    if week == '4주' and weekNum == 4 and dayOfweek == today_date: sched.add_job(run_crawl(exe), "date", run_date=run_time)

                    else:
                        pass
                except:
                    err = traceback.format_exc()
                    QMessageBox.warning(Collect_Manager, 'Error', self.errorLog(str(err)))

            def runRepeatCrawl():
                #추출된 리스트의 값을 토대로 예약 정보를 가져와서 예약 실행.
                for i in exportRunList():
                    i = i.split('|')
                    exe = str(i[0])
                    month = i[2]
                    week = i[3]
                    dayOfweek = str(i[4])
                    day_info = i[5]
                    time = str(i[6])
                    self.textBrowser.append(str(date.today())+' | '+exe + "수집")
                    reserveCrawl(month, week, dayOfweek, day_info, time, exe)
                    QtWidgets.QApplication.processEvents()
            return runRepeatCrawl()
        except:
            err = traceback.format_exc()
            QMessageBox.warning(Collect_Manager, 'Error', self.errorLog(str(err)))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Collect_Manager = QtWidgets.QWidget()
    ui = Ui_Collect_Manager()
    ui.setupUi(Collect_Manager)
    Collect_Manager.show()
    sys.exit(app.exec_())
