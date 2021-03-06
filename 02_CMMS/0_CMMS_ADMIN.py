# -*- coding: utf-8 -*-
import requests
from pyproj import Proj, transform, Transformer
import json
import cx_Oracle
import psycopg2
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
import os
import webbrowser
import csv
from shapely.geometry import mapping, Polygon
import fiona
import codecs
import datetime
from fiona import _shim, schema
import io
import re
import time
from shapely import wkt
import traceback
from DB_daily_update import oracle_export
from DB_daily_update import postgresql_backup_update

class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.ui()
        self.setWindowTitle('Longin')
        self.setWindowIcon(QIcon('logo_6533.png'))

    def ui(self):
        self.txtID = QLineEdit(self)
        self.txtPW = QLineEdit(self)
        self.txtPW.setEchoMode(QLineEdit.Password)
        btn = QPushButton('로그인', self)
        btn.clicked.connect(self.checkAuth)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.txtID)
        vbox.addWidget(self.txtPW)
        vbox.addWidget(btn)
        self.txtID.setText('cmms_admin')
        self.txtPW.setText('mappers')

    def checkAuth(self):
        if (self.txtID.text() == 'cmms_user' and self.txtPW.text() == 'mappers'):
            self.accept()
        elif (self.txtID.text() == 'cmms_admin' and self.txtPW.text() == 'mappers'):
            self.accept()
        else:
            QMessageBox.warning('실패', '없는 아이디 또는 로그인 실패')

class CheckBoxStyle(QtWidgets.QProxyStyle):
    def subElementRect(self, element, option, widget=None):
        r = super().subElementRect(element, option, widget)
        if element == QtWidgets.QStyle.SE_ItemViewItemCheckIndicator:
            r.moveCenter(option.rect.center())
        return r

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("""
        1. 셀 편집 = 셀 더블 클릭  \n
        2. 저장 = 입력이 완료된 이후 SPACE \n
        (콘솔창에 업데이트 완료라는 메시지가 출력 되어야 DB저장이 완료)  \n
        3. 셀 범위 복사 = 원하는 영역 드래그 후 Ctr + C  \n
        4. 리스트 추출 = 추출 하고자 하는 리스트를 선택 란에서 선택 후 추출 버튼 클릭.  \n
        5. SHP 추출 = 조회 기능을 통해 원하는 리스트를 조회 한 뒤 SHP 버튼 클릭  \n
        (1000개 미만의 row만 가능)  \n
        6. 선택 창에서 DB동기화 선택 후 LIST 추출 클릭 시 Oracle DB 동기화(admin 버전만 가능)
        # 하늘색 영역 이외에는 수정해도 DB에 저장 되지 않음.  
        """)
        layout.addWidget(self.label)
        self.setLayout(layout)

class Ui_Mainwindow(object):
    def setupUi(self, Mainwindow):
        self.w = None
        Mainwindow.setObjectName("Mainwindow")
        Mainwindow.resize(847, 797)
        Mainwindow.setWindowTitle('Icon')
        Mainwindow.setWindowIcon(QIcon('logo_6533.png'))
        self.centralwidget = QtWidgets.QWidget(Mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.query_line = QtWidgets.QLineEdit(self.centralwidget)
        self.query_line.setText("")
        self.query_line.setObjectName("query_line")
        self.gridLayout.addWidget(self.query_line, 0, 0, 1, 1)
        self.query_Button = QtWidgets.QPushButton(self.centralwidget)
        self.query_Button.setObjectName("query_Button")
        self.gridLayout.addWidget(self.query_Button, 0, 1, 1, 1)
        self.count_label = QtWidgets.QLabel(self.centralwidget)
        self.count_label.setText("")
        self.count_label.setObjectName("count_label")
        self.gridLayout.addWidget(self.count_label, 2, 0, 1, 1)
        self.exportOption = QtWidgets.QComboBox(self.centralwidget)
        self.exportOption.setObjectName("exportOption")
        self.gridLayout.addWidget(self.exportOption, 0, 3, 1, 1)
        self.exportOption.addItem('선택')
        self.exportOption.addItem('도로개통정보')
        self.exportOption.addItem('모니터링리스트')
        self.exportOption.addItem('전체리스트')
        self.exportOption.addItem('업데이트내역서')
        self.exportOption.addItem('DB동기화')
        self.exportList = QtWidgets.QPushButton(self.centralwidget)
        self.exportList.setObjectName("exportList")
        self.gridLayout.addWidget(self.exportList, 0, 4, 1, 1)
        self.explanation_detail = QtWidgets.QPushButton(self.centralwidget)
        self.explanation_detail.setObjectName("exportOption")
        self.gridLayout.addWidget(self.explanation_detail, 0, 2, 1, 1)
        self.explanation = QtWidgets.QLabel(self.centralwidget)
        self.explanation.setObjectName("explanation")
        self.gridLayout.addWidget(self.explanation, 1, 0, 1, 1)
        self.explanation2 = QtWidgets.QLabel(self.centralwidget)
        self.explanation2.setObjectName("explanation")
        self.gridLayout.addWidget(self.explanation2, 2, 0, 1, 1)
        self.Clear = QtWidgets.QPushButton(self.centralwidget)
        self.Clear.setObjectName("Clear")
        self.gridLayout.addWidget(self.Clear, 1, 4, 2, 2)
        self.SHP_EXPORT = QtWidgets.QPushButton(self.centralwidget)
        self.SHP_EXPORT.setObjectName("DB접속")
        self.gridLayout.addWidget(self.SHP_EXPORT, 1, 3, 2, 1)
        self.column_delete = QtWidgets.QPushButton(self.centralwidget)
        self.column_delete.setObjectName("칼럼삭제")
        self.gridLayout.addWidget(self.column_delete, 1, 2, 2, 1)
        self.column_delete_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.column_delete_cancel.setObjectName("칼럼삭제취소")
        self.gridLayout.addWidget(self.column_delete_cancel, 1, 1, 2, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(self.column_len())
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 5)
        Mainwindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Mainwindow)
        self.statusbar.setObjectName("statusbar")
        Mainwindow.setStatusBar(self.statusbar)

        self.retranslateUi(Mainwindow)
        QtCore.QMetaObject.connectSlotsByName(Mainwindow)

        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 칼럼값 수정 불가, 불가
        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)  # 칼럼값 수정 불가, 가능
        self.tableWidget.setAlternatingRowColors(True)  # 행마다 색깔을 변경 하는 코드
        self.tableWidget.itemDoubleClicked.connect(self.OpenLink)#더블클릭시 url오픈

        self.SHP_EXPORT.clicked.connect(self.shp_export) #shp export
        self.Clear.clicked.connect(self.Clear_contents) #화면의 row 클리어

        self.query_Button.clicked.connect(self.inquiry) #조회 버튼 클릭
        self.column_delete.clicked.connect(self.Hide_column) #칼럼 숨기기 , 취소 버튼
        self.column_delete_cancel.clicked.connect(self.Hide_column_cancel) #숨긴 칼럼 일괄 취소

        self.tableWidget.setSortingEnabled(True)
        # Add filters in column
        self.tableWidgetHeader = self.tableWidget.horizontalHeader()
        self.tableWidgetHeader.sectionDoubleClicked.connect(self.columnfilterclicked)
        self.keywords = dict([(i, []) for i in range(self.tableWidget.columnCount())])
        self.checkBoxs = []
        self.col = None
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection) #드래그 셀렉션
        #header 사이즈 컨텐츠 길이에 맞게
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(10, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(11, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(12, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(13, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(14, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(15, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(16, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(17, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(18, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(19, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(20, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(21, QHeaderView.ResizeToContents)

        self.list_view() # 프로그램 키면 초기화면 세팅.

        # self.tableWidget.cellClicked.connect(self.cellClickCopy)
        self.tableWidget.keyPressEvent =self.keyPressEvent
        self.exportList.clicked.connect(self.ListExportButton)
        self.tableWidget.itemClicked.connect(self.checkchanged)
        self.explanation_detail.clicked.connect(self.show_new_window)
        self.exportOption.currentIndexChanged.connect(self.combobox_update_button_click)
        self.query_line.returnPressed.connect(self.inquiry)  # 엔터버튼 누르면 조회버튼 누르는 것과 동일한 기능.

    def retranslateUi(self, Mainwindow):
        _translate = QtCore.QCoreApplication.translate
        Mainwindow.setWindowTitle(_translate("Mainwindow", "CMMS_LIST"))
        self.query_Button.setText(_translate("Mainwindow", "조 회"))
        self.exportList.setText(_translate("Mainwindow", "LIST추출/Update"))
        self.explanation_detail.setText(_translate("Mainwindow", "주요기능안내"))
        self.explanation.setText(_translate("Mainwindow", "select * from cmms.cmms_list where del_flag = '0' and 이후 쿼리입력. ex)type = '해당없음' / 마지막 ; 생략"))
        self.explanation2.setText(_translate("Mainwindow","table 의 column 명은 현재 표 칼럼의 두번째 줄의 영문명을 사용."))
        self.Clear.setText(_translate("Mainwindow", "Clear"))
        self.SHP_EXPORT.setText(_translate("Mainwindow", "SHP_EXPORT"))
        self.tableWidget.setToolTip(_translate("Mainwindow", "<html><head/><body><p><br/></p></body></html>"))
        self.column_delete.setText(_translate("Mainwindow", "선택 칼럼 숨기기"))
        self.column_delete_cancel.setText(_translate("Mainwindow", "칼럼 숨기기 취소"))

    def errorLog(self,error: str):
        current_time = time.strftime("%Y.%m.%d/%H:%M:%S", time.localtime(time.time()))
        return (f"[{current_time}] - {error}\n")

    def show_new_window(self):#기능 설명 팝업창
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()
        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    def coulmn_list(self):
        with open('config.txt') as data:
            line = data.readline()
        line = str(line).replace('my_column_list = ', '').split(',')
        line = str(line).replace('[', '').replace(']', '').replace('\n','')
        return line

    def column_len(self):
        with open('config.txt') as data:
            line = data.readline()
        line = str(line).replace('my_column_list = ','').split(',')
        return len(line)

    #1. DB 접속 함수.
    def db_connect(self):
        t_host = ""  # either "localhost", a domain name, or an IP address.
        t_port = # default postgres port
        t_dbname = 
        t_user = 
        t_pw = 
        self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw, options="-c search_path=cmms")
        return self.conn

    def replace_all(self, text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    def getUpdateDate(self):
        self.cursor = self.db_connect().cursor()
        query = "select to_char(cmms_update_date,'YYYY-MM-DD HH24:MI:SS') from cmms_list order by cmms_update_date desc limit 1;"
        self.cursor = self.db_connect().cursor()
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        row = str(row).replace('(','').replace(',)','')
        return row


    #DB 접속 버튼으로 초기 화면 불러옴
    def list_view(self):
        try:
            today = datetime.date.today()
            coulmn_list = self.coulmn_list()
            coulmn_list2 = coulmn_list.replace("'","").replace('\\n','')
            replace_rule = {'nid': 'NID\nNID', 'type': '유형\nTYPE', 'text': '제목\nTEXT', 'lcode': 'LCODE\nLCODE',
                            'limit_date': '구축시한\nLIMIT_DATE', 'complete_date': '준공일\nCOMPLETE_DATE',
                            'height_limit': '높이제한\nHEIGHT_LIMIT', 'weight_limit': '중량제한\nWEIGHT_LIMIT',
                            'time_id': '시간제\nTIME_ID', 'road_work': '도로공사종류\nROAD_WORK',
                            'result': '실사결과\nRESULT', 'request_date': '실사일정\nREQUEST_DATE', 'poi_cat': 'POI상태\nPOI_CAT',
                            'poi_date': 'POI구축일\nPOI_DATE', 'net_cat': 'NET상태\nNET_CAT', 'net_date': 'NET구축일\nNET_DATE',
                            'map_cat': 'MAP상태\nMAP_CAT', 'map_date': 'MAP구축일\nMAP_DATE',
                            'data_check': '데이터확인\nDATA_CHECK',
                            'service_check': '서비스확인\nSERVICE_CHECK', 'url': 'URL\nURL',
                            'create_date': '최초생성일\nCREATE_DATE', 'update_date': '최종수정일\nUPDATE_DATE'}
            header_list = self.replace_all(coulmn_list, replace_rule).replace(' ','').replace("'","").replace('\\n', '')
            header_list = header_list.split(',')
            self.tableWidget.setHorizontalHeaderLabels(header_list)
            self.cursor = self.db_connect().cursor()
            query = ("select {} from cmms_list where del_flag = '0' order by limit_date").format(coulmn_list2)
            print(query)
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            i = 0
            for elem in rows:
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                j = 0
                for t in elem:
                    try: a = int(str(t - today).split(' ')[0])
                    except : a = 0
                    if t == None: t = ''
                    if j == 0 :
                        # 해당 필드 숫자 형식으로 바꾸기 위함.
                        item = QTableWidgetItem()
                        item.setData(QtCore.Qt.DisplayRole, t)
                        self.tableWidget.setItem(i, j, QTableWidgetItem(item))
                    elif j in (12,13,14,15,16,17):
                        item = QTableWidgetItem()
                        item.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled )
                        item.setData(QtCore.Qt.DisplayRole, t)
                        item.setBackground(QtGui.QColor(129,216,208))
                        self.tableWidget.setItem(i, j, QTableWidgetItem(item))
                    elif j == 22:
                        t = str(t).replace('\\\\','\\')
                        self.tableWidget.setItem(i, j, QTableWidgetItem(t))
                    elif j in (18, 20) :
                        chkBoxItem = QTableWidgetItem()
                        if t == 'Yes':
                            chkBoxItem.setTextAlignment(QtCore.Qt.AlignCenter)
                            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                            chkBoxItem.setCheckState(QtCore.Qt.Checked)
                            self.tableWidget.setItem(i, j, QTableWidgetItem(chkBoxItem))
                        else:
                            chkBoxItem.setTextAlignment(QtCore.Qt.AlignCenter)
                            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                            self.tableWidget.setItem(i, j, QTableWidgetItem(chkBoxItem))
                    elif j == 4 and a < 0 : # 지연 대상들 빨간색
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                        self.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 102, 102))
                    elif j == 4 and a < 11 : # 임박 10일 대상들 노란색
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                        self.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 204, 102))
                    else:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                    j += 1
                i += 1

            self.statusbar.showMessage('count : '+str(len(rows)) + ' / '+'최근 업데이트 날짜 : '+ str(self.getUpdateDate()))#상태 창에 전체 카운트 출력
            self.db_connect().close()
        except:
            err = traceback.format_exc()
            QMessageBox.warning(Mainwindow,'Error',self.errorLog(str(err)))

    def checkchanged(self, item):# 체크박스 체인지 할때의 실행.
        column = item.column()
        try:
            if item.checkState() == QtCore.Qt.Checked:
                if column in (18,20) :
                    t_host = ""  # either "localhost", a domain name, or an IP address.
                    t_port = # default postgres port
                    t_dbname = 
                    t_user = 
                    t_pw = 
                    self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw,options="-c search_path=cmms")
                    column = item.column()
                    row = item.row()
                    if column == 18 : column_name = 'data_check'
                    else : column_name = 'service_check'
                    content = 'Yes'
                    nid = self.tableWidget.item(row, 0).text()
                    print(column, '/', row, '/',nid)
                    query = "update cmms_list set %s='%s' where nid=%s;" % (str(column_name), content, int(nid))
                    self.cursor = self.conn.cursor()
                    self.cursor.execute(query)
                    self.conn.commit()
                    self.db_connect().close()
                    self.tableWidget.update()
                    print('nid = '+nid+' / '+content+' / 데이터 확인 필드 업데이트 완료')
                    QMessageBox.warning(self.tableWidget, '확인', '데이터 확인 필드 업데이트 완료')
                else : pass
            elif item.checkState() == QtCore.Qt.Unchecked:
                if column in (18, 20):
                    print('"%s" Unchecked' % item.text())
                    t_host = # either "localhost", a domain name, or an IP address.
                    t_port = # default postgres port
                    t_dbname = 
                    t_user = 
                    t_pw = 
                    self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw,options="-c search_path=cmms")
                    column = item.column()
                    row = item.row()
                    print(column, '//', row)
                    if column == 18 : column_name = 'data_check'
                    else: column_name = 'service_check'
                    content = 'No'
                    nid = self.tableWidget.item(row, 0).text()
                    query = "update cmms_list set %s='%s' where nid=%s;" % (str(column_name), content, int(nid))
                    self.cursor = self.conn.cursor()
                    self.cursor.execute(query)
                    self.conn.commit()
                    self.db_connect().close()
                    self.tableWidget.update()
                    print('nid = '+nid+' / '+content+' / 서비스 확인 필드 업데이트 완료')
                    QMessageBox.warning(self.tableWidget, '확인', '서비스 확인 필드 업데이트 완료')
                else: pass
        except : pass

    def slotSelect(self, state):
        for checkbox in self.checkBoxs:
            checkbox.setChecked(QtCore.Qt.Checked == state)

    def menuClose(self):
        self.keywords[self.col] = []
        for element in self.checkBoxs:
            if element.isChecked():
                self.keywords[self.col].append(element.text())
        self.filterdata()
        self.menu.close()

    def clearFilter(self):
        if self.tableWidget.rowCount() > 0:
            for i in range(self.tableWidget.rowCount()):
                self.tableWidget.setRowHidden(i, False)

    def filterdata(self):
        columnsShow = dict([(i, True) for i in range(self.tableWidget.rowCount())])

        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if j in (18,19):
                    pass
                if self.keywords[j]:
                    if item.text() not in self.keywords[j]:
                        columnsShow[i] = False

        for key in columnsShow:
            self.tableWidget.setRowHidden(key, not columnsShow[key])

    def columnfilterclicked(self, index):
        try:
            self.menu = QtWidgets.QMenu()
            self.menu.setStyleSheet('QMenu { menu-scrollable: true; }')
            self.col = index

            data_unique = []
            self.checkBoxs = []

            checkBox = QtWidgets.QCheckBox("Select all", self.menu)
            checkableAction = QtWidgets.QWidgetAction(self.menu)
            checkableAction.setDefaultWidget(checkBox)
            self.menu.addAction(checkableAction)
            checkBox.setChecked(True)
            checkBox.stateChanged.connect(self.slotSelect)

            for i in range(self.tableWidget.rowCount()):
                if not self.tableWidget.isRowHidden(i):
                    item = self.tableWidget.item(i, index)
                    if item.text() not in data_unique:
                        data_unique.append(item.text())
                        checkBox = QtWidgets.QCheckBox(item.text(), self.menu)
                        checkBox.setChecked(True)
                        checkableAction = QtWidgets.QWidgetAction(self.menu)
                        checkableAction.setDefaultWidget(checkBox)
                        self.menu.addAction(checkableAction)
                        self.checkBoxs.append(checkBox)

            btn = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
                                             QtCore.Qt.Horizontal, self.menu)
            btn.accepted.connect(self.menuClose)
            btn.rejected.connect(self.menu.close)
            checkableAction = QtWidgets.QWidgetAction(self.menu)
            checkableAction.setDefaultWidget(btn)
            self.menu.addAction(checkableAction)

            headerPos = self.tableWidget.mapToGlobal(self.tableWidgetHeader.pos())

            posY = headerPos.y() + self.tableWidgetHeader.height()
            posX = headerPos.x() + self.tableWidgetHeader.sectionPosition(index)
            self.menu.exec_(QtCore.QPoint(posX, posY))
        except:
            err = traceback.format_exc()
            QMessageBox.warning(Mainwindow,'Error',self.errorLog(str(err)))

    def copySelection(self): # 드래그 셀렉션 카피
        selection = self.tableWidget.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream).writerows(table)
            QApplication.clipboard().setText(stream.getvalue())

    def Clear_contents(self):     #컨텐츠 모두 지우기
        self.tableWidget.setSortingEnabled(False)
        self.statusbar.clearMessage()
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setSortingEnabled(True)

    def inquiry(self): # 조회버튼 클릭시.
        self.tableWidget.setSortingEnabled(False)
        today = datetime.date.today()
        try:
            self.statusbar.clearMessage()
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(self.column_len())
            coulmn_list = self.coulmn_list()
            coulmn_list2 = coulmn_list.replace("'", "").replace('\\n', '')
            replace_rule = {'nid': 'NID\nNID', 'type': '유형\nTYPE', 'text': '제목\nTEXT', 'lcode': 'LCODE\nLCODE',
                            'limit_date': '구축시한\nLIMIT_DATE', 'complete_date': '준공일\nCOMPLETE_DATE',
                            'height_limit': '높이제한\nHEIGHT_LIMIT', 'weight_limit': '중량제한\nWEIGHT_LIMIT',
                            'time_id': '시간제\nTIME_ID', 'road_work': '도로공사종류\nROAD_WORK',
                            'result': '실사결과\nRESULT', 'request_date': '실사일정\nREQUEST_DATE', 'poi_cat': 'POI상태\nPOI_CAT',
                            'poi_date': 'POI구축일\nPOI_DATE', 'net_cat': 'NET상태\nNET_CAT', 'net_date': 'NET구축일\nNET_DATE',
                            'map_cat': 'MAP상태\nMAP_CAT', 'map_date': 'MAP구축일\nMAP_DATE',
                            'data_check': '데이터확인\nDATA_CHECK',
                            'service_check': '서비스확인\nSERVICE_CHECK', 'url': 'URL\nURL',
                            'create_date': '최초생성일\nCREATE_DATE', 'update_date': '최종수정일\nUPDATE_DATE'}
            header_list = self.replace_all(coulmn_list, replace_rule).replace(' ', '').replace("'", "").replace('\\n', '')
            header_list = header_list.split(',')
            self.tableWidget.setHorizontalHeaderLabels(header_list)
            self.cursor = self.db_connect().cursor()
            if self.query_line.text() == '' : query = ("select {} from cmms_list where del_flag = '0'" + self.query_line.text() + ';').format(coulmn_list2)
            else : query = ("select {} from cmms_list where del_flag = '0' and " + self.query_line.text() + ';').format(coulmn_list2)
            print(query)
            self.cursor = self.db_connect().cursor()
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            self.tableWidget.setRowCount(len(rows))
            i = 0
            for elem in rows:
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                j = 0
                for t in elem:
                    try:
                        a = int(str(t - today).split(' ')[0])
                    except:
                        a = 0
                    if t == None: t = ''
                    if j == 0:
                        # 해당 필드 숫자 형식으로 바꾸기 위함.
                        item = QTableWidgetItem()
                        item.setData(QtCore.Qt.DisplayRole, t)
                        self.tableWidget.setItem(i, j, QTableWidgetItem(item))
                    elif j in (12, 13, 14, 15, 16, 17):
                        item = QTableWidgetItem()
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                        item.setData(QtCore.Qt.DisplayRole, t)
                        item.setBackground(QtGui.QColor(129, 216, 208))
                        self.tableWidget.setItem(i, j, QTableWidgetItem(item))
                    elif j == 22:
                        t = str(t).replace('\\\\', '\\')
                        self.tableWidget.setItem(i, j, QTableWidgetItem(t))
                    elif j in (18, 20):
                        chkBoxItem = QTableWidgetItem()
                        if t == 'Yes':
                            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                            chkBoxItem.setCheckState(QtCore.Qt.Checked)
                            self.tableWidget.setItem(i, j, QTableWidgetItem(chkBoxItem))
                        else:
                            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                            self.tableWidget.setItem(i, j, QTableWidgetItem(chkBoxItem))
                    elif j == 4 and a < 0:  # 지연 대상들 빨간색
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                        self.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 102, 102))
                    elif j == 4 and a < 11:  # 임박 10일 대상들 노란색
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                        self.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 204, 102))
                    else:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                    j += 1
                i += 1
            self.statusbar.showMessage('count : ' + str(len(rows))+ ' / ' +'최근 업데이트 날짜 : '+ str(self.getUpdateDate()))# 상태 창에 전체 카운트 출력
            self.db_connect().close()
            self.tableWidget.setSortingEnabled(True)
            QMessageBox.information(self.tableWidget, "확인", "조회 완료")
        except:
            QMessageBox.warning(self.tableWidget, '실패', '쿼리 문법을 확인해 주세요')

    def Hide_column(self):# 누른 셀 위치의 칼럼 숨기기 / 취소
        column_num = self.tableWidget.currentColumn()
        sender_obj = self.tableWidget.sender()
        if sender_obj.text() == "column 숨기기":
            self.tableWidget.setColumnHidden(column_num, True)
            sender_obj.setText("column 보이기")
        else:
            self.tableWidget.setColumnHidden(column_num, False)
            sender_obj.setText("column 숨기기")
        return

    def Hide_column_cancel(self): # 숨긴 칼럼 일괄 취소
        for ss in range(0,23):
            self.tableWidget.setColumnHidden(ss,False)

    def OpenLink(self, item): # url 칼럼을 더블클릭하면 url, 폴더
        if item.column() == 22:
            for ss in self.tableWidget.selectedItems():
                if str(ss.text()).startswith('http'): webbrowser.open(str(ss.text()))
                else :
                    try:
                        a = r'{}'.format(ss.text())
                        os.startfile(a)
                    except:
                        QMessageBox.warning(self.tableWidget, '실패', '경로가 올바르지 않습니다.')
        else:
            pass

    def keyPressEvent(self, event): #컨트롤 씨 키보드 이벤트.
        if (event.key() == QtCore.Qt.Key_C) and (event.modifiers() & QtCore.Qt.ControlModifier):
            self.copySelection()
        elif event.key() == QtCore.Qt.Key_Space:
            self.updateData()
        else : pass

    def updateData(self): # 수정후 스페이스 입력시 이벤트에 연결 할 DB 업데이트 문
        try:
            t_host = # either "localhost", a domain name, or an IP address.
            t_port = # default postgres port
            t_dbname = 
            t_user = 
            t_pw = 
            self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw,
                                         options="-c search_path=cmms")
            select_item = self.tableWidget.currentItem()
            row = select_item.row()
            column = select_item.column()
            try:
                column_name = ''
                try:
                    content = self.tableWidget.item(row, column).text()
                except : content =''
                if column == 12: column_name = 'poi_cat'
                if column == 13:
                    column_name = 'poi_date'
                    # content = str(content[0:4] + '-' + content[4:6] + '-' + content[6:8])
                    # if content == '--' : content = 'NULL'
                if column == 14: column_name = 'net_cat'
                if column == 15:
                    column_name = 'net_date'
                    # content = str(content[0:4] + '-' + content[4:6] + '-' + content[6:8])
                    # if content == '--': content = 'NULL'
                if column == 16: column_name = 'map_cat'
                if column == 17:
                    column_name = 'map_date'
                    # content = str(content[0:4] + '-' + content[4:6] + '-' + content[6:8])
                    # if content == '--': content = 'NULL'
                if column == 18: column_name = 'data_check'
                if column == 20: column_name = 'service_check'
                nid = self.tableWidget.item(row, 0).text()
                if content == 'NULL' :
                    query = "update cmms_list set %s=%s where nid=%s;" % (str(column_name), content, int(nid))
                else:
                    query = "update cmms_list set %s='%s' where nid=%s;" % (str(column_name), content, int(nid))
                self.cursor = self.conn.cursor()
                self.cursor.execute(query)
                self.conn.commit()
                self.db_connect().close()
                self.tableWidget.update()
                print(content , ' DB update 완료')
            except:
                QMessageBox.warning(self.tableWidget, '실패', '편집 가능한 칼럼이 아니거나 입력 형식을 확인하세요.')
                self.tableWidget.update()
            if self.tableWidget.item(row, 12).text() == '완료' and self.tableWidget.item(row, 13).text() == '':
                QMessageBox.warning(self.tableWidget, '확인', '완료 날짜를 반드시 기입해야 합니다.')
            if self.tableWidget.item(row, 14).text() == '완료' and self.tableWidget.item(row, 15).text() == '':
                QMessageBox.warning(self.tableWidget, '확인', '완료 날짜를 반드시 기입해야 합니다.')
            if self.tableWidget.item(row, 16).text() == '완료' and self.tableWidget.item(row, 17).text() == '':
                QMessageBox.warning(self.tableWidget, '확인', '완료 날짜를 반드시 기입해야 합니다.')
        except :
            err = traceback.format_exc()
            QMessageBox.warning(Mainwindow,'Error',self.errorLog(str(err)))
    # def cellClickCopy(self):
    #     select_item = self.tableWidget.currentItem()
    #     row = select_item.row()
    #     column = select_item.column()
    #     content = self.tableWidget.item(row, column).text().strip()
    #     clipboard = QtGui.QGuiApplication.clipboard()
    #     clipboard.setText(content)
    #     event = QtCore.QEvent(QtCore.QEvent.Clipboard)
    #     app.sendEvent(clipboard, event)
    #     print(row , column, content)

    def RoadOpenList(self):
        try:
            t_host = # either "localhost", a domain name, or an IP address.
            t_port = # default postgres port
            t_dbname = 
            t_user = 
            t_pw = 
            self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw,options="-c search_path=cmms")
            csv_file = open("도로개통정보.csv", "w",encoding='utf-8')
            writer = csv.writer(csv_file, lineterminator="\n", delimiter='|', quoting=csv.QUOTE_NONE, escapechar='\\')
            csv_file.write("TEXT|NID|TYPE|ROAD_WORK|TIME_ID|COMPLETE_DATE|LIMIT_DATE|NET_DATE|NET_CAT\n")
            query = "select text, nid, type, road_work,time_id, complete_date,limit_date,net_date,net_cat from cmms_list where type not in ('아파트','시설') and del_flag ='0' order by complete_date"
            self.cursor = self.conn.cursor()
            self.cursor.execute(query)
            row = self.cursor.fetchall()
            for r in row:
                writer.writerow(r)
            csv_file.close()
            self.db_connect().close()
            QMessageBox.information(self.tableWidget, "도로개통정보", "추출 완료")
        except:
            QMessageBox.warning(self.tableWidget, '알림', '추출 실패')

    def EntireList(self):
        try:
            t_host = # either "localhost", a domain name, or an IP address.
            t_port = # default postgres port
            t_dbname = 
            t_user = 
            t_pw = 
            self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw,options="-c search_path=cmms")
            csv_file = open("전체리스트.csv", "w", encoding='utf-8')
            writer = csv.writer(csv_file, lineterminator="\n", delimiter='}', quoting=csv.QUOTE_NONE, escapechar='\\')
            csv_file.write("TYPE}TEXT}NID}LCODE}COMPLETE_DATE}LIMIT_DATE}RESULT}REQUEST_DATE}REVIEW_DATE}HEIGHT_LIMIT}WEIGHT_LIMIT}ROAD_WORK}TIME_ID}POI_CAT}POI_DATE}NET_CAT}NET_DATE}MAP_CAT}MAP_DATE}DATA_CHECK}SERVICE_CHECK}URL}CREATE_DATE}UPDATE_DATE}DEL_FLAG}CMMS_UPDATE_DATE\n")
            query = "select * from cmms_list where del_flag ='0' order by complete_date"
            self.cursor = self.conn.cursor()
            self.cursor.execute(query)
            row = self.cursor.fetchall()
            for r in row:
                writer.writerow(r)
            csv_file.close()
            self.db_connect().close()
            QMessageBox.information(self.tableWidget, "전체리스트", "추출 완료")
        except:
            QMessageBox.warning(self.tableWidget, '알림', '추출 실패')

    def MonitoringList(self):
        try:
            t_host = # either "localhost", a domain name, or an IP address.
            t_port = # default postgres port
            t_dbname = 
            t_user = 
            t_pw = 
            self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw,options="-c search_path=cmms")
            csv_file = open("모니터링리스트.csv", "w", encoding='utf-8')
            writer = csv.writer(csv_file, lineterminator="\n", delimiter='|', quoting=csv.QUOTE_NONE, escapechar='\\')
            csv_file.write("TYPE|TEXT|LCODE|COMPLETE_DATE\n")
            query = "select type, text, lcode, complete_date from cmms_list where del_flag ='0' order by complete_date"
            self.cursor = self.conn.cursor()
            self.cursor.execute(query)
            row = self.cursor.fetchall()
            for r in row:
                writer.writerow(r)
            csv_file.close()
            self.db_connect().close()
            QMessageBox.information(self.tableWidget, "모니터링리스트", "추출 완료")
        except:
            QMessageBox.warning(self.tableWidget, '알림', '추출 실패')

    def ListExportButton(self):  # 콤보 박스 별로 실행되는 함수 다르게 설정
        print(self.exportOption.currentText())
        if self.exportOption.currentText() == '도로개통정보':
            self.RoadOpenList()
        elif self.exportOption.currentText() == '모니터링리스트':
            self.MonitoringList()
        elif self.exportOption.currentText() == '전체리스트':
            self.EntireList()
        elif self.exportOption.currentText() == '업데이트내역서':
            self.update_txt_export()
        elif self.exportOption.currentText()=='DB동기화':
            oracle_export()
            postgresql_backup_update()
            print('DB 동기화 완료')
        else: QMessageBox.warning(self.tableWidget, '알림', '추출 하고자 하는 리스트를 선택 후 LIST 추출 버튼을 클릭 해 주세요')

    def shp_export(self):  ##shp 뽑기 위한 함수 모음.
        # 현재 화면의 nid값을 가져오기.
        try:
            nid_list = []
            for ss in range(0, self.tableWidget.rowCount() + 1):
                item = self.tableWidget.item(ss, 0)
                if item is not None:
                    txt = item.text()
                    nid_list.append(txt)

            nid_list = str(nid_list).replace('[', '(').replace(']', ')')
            # 화면의 nid값과 일치하는 oracle 좌표 값 csv로 저장.
            LOCATION = r"C:\ora64\instantclient_21_3"
            os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]
            db = cx_Oracle.connect('contentsteam', 'zjsxpscm', '192.168.10.30:1521/imdb', encoding='UTF-8',
                                   nencoding='UTF-8')
            cursor = db.cursor()
            csv_file = open("sdo_geometry.csv", "w")
            writer = csv.writer(csv_file, lineterminator="\n", delimiter='|')
            query = ("SELECT nid, type, limit_date, sdo_util.to_wktgeometry(gshape) as cord FROM imduser.tbw_dt_infocol where nid in {}").format(nid_list)
            print(query)
            r = cursor.execute(query)
            for row in r:
                writer.writerow(row)
            cursor.close()
            db.close()
            print('oracle shape save complete')
            data = []
            with open('sdo_geometry.csv') as w:
                reader = csv.reader(w, delimiter='|')
                for s in reader:
                    geo = str(s[3]).replace('POLYGON ', '').replace(', ', '), (').replace(' ', ',').replace(',,',
                                                                                                            ',').replace(
                        '),(', '), (').replace('((', '(').replace('))', ')')
                    data.append({'nid': s[0], 'type': s[1], 'limit_date': s[2], 'geos': geo})
            schema = {
                'geometry': 'Polygon',
                'properties': {
                    'id': 'int',
                    'type': 'str',
                    'limit_date': 'str'
                }
            }
            # Write a new Shapefile
            with fiona.open('cmms_shp_export', 'w', 'ESRI Shapefile', schema, encoding='euc-kr') as c:
                ## If there are multiple geometries, put the "for" loop here
                for ss in data:
                    ids = ss['nid']
                    type = ss['type']
                    limit_date = ss['limit_date']
                    poly = ss['geos']
                    poly = poly.split(', ')
                    poly_list = []
                    for aa in poly:
                        a = aa.replace('(', '').replace(')', '')
                        a = a.split(',')
                        a1 = float(a[0])
                        a2 = float(a[1])
                        poly_list.append((a1, a2))
                    poly = Polygon(poly_list)
                    c.write({'geometry': mapping(poly), 'properties': {'id': ids, 'type': type, 'limit_date': limit_date}})
        except:
            QMessageBox.warning(self.tableWidget, '실패', 'row count 가 1000개 이상인지 확인')
        else:
            QMessageBox.information(self.tableWidget, "성공", "SHP 추출 완료")

    def combobox_update_button_click(self):
        if self.exportOption.currentText() == '업데이트내역서':
            query = "limit_date between '2022-00-00' and '2022-00-00'"
            self.query_line.setText(query)
        else : pass

    def update_txt_export(self):
        try:
            t_host = # either "localhost", a domain name, or an IP address.
            t_port = # default postgres port
            t_dbname = 
            t_user = 
            t_pw = 
            self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw, options="-c search_path=cmms")
            outfile = codecs.open('업데이트내역서.txt', 'w',encoding='utf-8')
            query = "select lcode, text, type,polygon_text from cmms_list where map_cat = '완료' and " + self.query_line.text() + ';'
            self.cursor = self.conn.cursor()
            self.cursor.execute(query)
            row = self.cursor.fetchall()
            for r in row:
                a = r[3]
                poly = wkt.loads(a)
                center_point = poly.centroid.wkt
                center_point = center_point.replace('POINT (','').replace(')','').split(' ')
                x = center_point[1]
                y = center_point[0]
                transformer = Transformer.from_crs('EPSG:5178', 'EPSG:4326')
                change_xy = transformer.transform(x, y)
                x1 = change_xy[1]
                y1 = change_xy[0]
                url = 'http://api.vworld.kr/req/address?service=address&request=getAddress&version=2.0&crs=epsg:4326&point={},{}&format=json&type=both&zipcode=true&simple=false&key=3EAB6562-19D4-33E5-920A-66E483DBC133'.format(x1, y1)
                response = requests.get(url).text
                jsonString = json.loads(response)
                result = jsonString['response']['result'][0]['structure']
                addr = str(result['level1'] + ' ' + result['level2'] + ' ' + result['level3'] + ' ' + result['level4L']).replace('  ', ' ').strip()
                r = addr+'|'+r[0]+'|'+r[1]+'|'+r[2]+' '+'배경 업데이트'+'\n'
                outfile.write(r)
            outfile.close()
            self.db_connect().close()
            QMessageBox.information(self.tableWidget, "업데이트내역서", "추출 완료")
        except:
            QMessageBox.warning(self.tableWidget, '실패', '쿼리 내용을 확인해 주세요')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    if login.exec_()==QDialog.Accepted:
        checkbox_style = CheckBoxStyle(app.style())
        app.setStyle(checkbox_style)

        Mainwindow = QtWidgets.QMainWindow()
        ui = Ui_Mainwindow()
        ui.setupUi(Mainwindow)
        Mainwindow.show()
        sys.exit(app.exec_())