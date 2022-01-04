# -*- coding: utf-8 -*-

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
        self.txtID.setText('cmms')
        self.txtPW.setText('mappers')

    def checkAuth(self):
        if (self.txtID.text() == 'cmms' and self.txtPW.text() == 'mappers'):
            self.accept()
        else:
            QMessageBox.warning('실패', '없는 아이디 또는 로그인 실패')

class CheckBoxStyle(QtWidgets.QProxyStyle):
    def subElementRect(self, element, option, widget=None):
        r = super().subElementRect(element, option, widget)
        if element == QtWidgets.QStyle.SE_ItemViewItemCheckIndicator:
            r.moveCenter(option.rect.center())
        return r

class Ui_Mainwindow(object):
    def setupUi(self, Mainwindow):
        Mainwindow.setObjectName("Mainwindow")
        Mainwindow.resize(847, 797)
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

        Mainwindow.setWindowTitle('Icon')
        Mainwindow.setWindowIcon(QIcon('logo_6533.png'))

        self.exportOption = QtWidgets.QComboBox(self.centralwidget)
        self.exportOption.setObjectName("exportOption")
        self.gridLayout.addWidget(self.exportOption, 0, 3, 1, 1)
        self.exportOption.addItem('선택')
        self.exportOption.addItem('도로개통정보')
        self.exportOption.addItem('모니터링리스트')
        self.exportOption.addItem('전체리스트')
        self.exportOption.addItem('업데이트내역서')

        self.exportList = QtWidgets.QPushButton(self.centralwidget)
        self.exportList.setObjectName("exportList")
        self.gridLayout.addWidget(self.exportList, 0, 4, 1, 1)

        # self.exportUPDATE = QtWidgets.QPushButton(self.centralwidget)
        # self.exportUPDATE.setObjectName("exportOption")
        # self.gridLayout.addWidget(self.exportUPDATE, 0, 2, 1, 1)

        self.explaination = QtWidgets.QLabel(self.centralwidget)
        self.explaination.setObjectName("explaination")
        self.gridLayout.addWidget(self.explaination, 1, 0, 1, 1)
        self.explaination2 = QtWidgets.QLabel(self.centralwidget)
        self.explaination2.setObjectName("explaination")
        self.gridLayout.addWidget(self.explaination2, 2, 0, 1, 1)
        self.Clear = QtWidgets.QPushButton(self.centralwidget)
        self.Clear.setObjectName("Clear")
        self.gridLayout.addWidget(self.Clear, 1, 4, 2, 1)

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
        self.tableWidget.setColumnCount(23)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 5)
        Mainwindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Mainwindow)
        self.statusbar.setObjectName("statusbar")
        Mainwindow.setStatusBar(self.statusbar)

        self.retranslateUi(Mainwindow)
        QtCore.QMetaObject.connectSlotsByName(Mainwindow)

        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked) #칼럼값 수정 불가, 가능
        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 칼럼값 수정 불가, 불가
        self.tableWidget.setAlternatingRowColors(True)  # 행마다 색깔을 변경 하는 코드
        self.tableWidget.itemDoubleClicked.connect(self.OpenLink)#더블클릭시 url오픈

        self.SHP_EXPORT.clicked.connect(self.shp_export) #shp export
        self.Clear.clicked.connect(self.Clear_contents) #화면의 row 클리어

        self.query_Button.clicked.connect(self.inquiry) #조회 버튼 클릭
        self.column_delete.clicked.connect(self.Hide_column) #칼럼 숨기기 , 취소 버튼
        self.column_delete_cancel.clicked.connect(self.Hide_column_cancel) #숨긴 칼럼 일괄 취소

        self.tableWidget.setSortingEnabled(True)
        #Add filters in column
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

        self.list_view_click() # 프로그램 키면 초기화면 세팅.

        self.tableWidget.cellClicked.connect(self.sellClickCopy)
        self.tableWidget.keyPressEvent =self.keyPressEvent
        self.exportList.clicked.connect(self.ListExportButton)
        self.tableWidget.itemClicked.connect(self.checkchanged)

    def retranslateUi(self, Mainwindow):
        _translate = QtCore.QCoreApplication.translate
        Mainwindow.setWindowTitle(_translate("Mainwindow", "CMMS_LIST"))
        self.query_Button.setText(_translate("Mainwindow", "조 회"))
        self.exportList.setText(_translate("Mainwindow", "LIST추출"))
        self.explaination.setText(_translate("Mainwindow", "select * from cmms.cmms_list where del_flag = '0'이후 쿼리입력. ex)and type = '해당없음' / 마지막 ; 생략"))
        self.explaination2.setText(_translate("Mainwindow","table 의 column 명은 현재 표 칼럼의 두번째 줄의 영문명을 사용."))
        self.Clear.setText(_translate("Mainwindow", "Clear"))
        self.SHP_EXPORT.setText(_translate("Mainwindow", "SHP_EXPORT"))
        self.tableWidget.setToolTip(_translate("Mainwindow", "<html><head/><body><p><br/></p></body></html>"))
        self.column_delete.setText(_translate("Mainwindow", "선택 칼럼 숨기기"))
        self.column_delete_cancel.setText(_translate("Mainwindow", "칼럼 숨기기 취소"))

    #1. DB 접속 함수.
    def db_connect(self):
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw, options="-c search_path=cmms")
        return self.conn

    #DB 접속 버튼으로 초기 화면 불러옴
    def list_view_click(self):
        today = datetime.date.today()
        self.tableWidget.setHorizontalHeaderLabels(
            ['NID\nNID','유형\nTYPE', '제목\nTEXT', 'LCODE\nLCODE', '구축시한\nLIMIT_DATE', '준공일\nCOMPLETE_DATE','높이제한\nHEIGHT_LIMIT', '중량제한\nWEIGHT_LIMIT', '시간제\nTIME_ID', '도로공사종류\nROAD_WORK',
             '실사결과\nRESULT', '실사일정\nREQUEST_DATE','POI상태\nPOI_CAT', 'POI구축일\nPOI_DATE','NET상태\nNET_CAT', 'NET구축일\nNET_DATE','MAP상태\nMAP_CAT', 'MAP구축일\nMAP_DATE', '데이터확인\nDATA_CHECK', '서비스확인\nSERVICE_CHECK', 'URL\nURL',
             '최초생성일\nCREATE_DATE', '최종수정일\nUPDATE_DATE'])
        self.cursor = self.db_connect().cursor()
        self.cursor.execute("select nid, type, text, lcode, limit_date, complete_date, height_limit, weight_limit, time_id,road_work, result, request_date, poi_cat, poi_date, net_cat, net_date, map_cat, map_date, data_check, service_check, url, create_date, update_date from cmms_list where del_flag = '0' order by limit_date")
        rows = self.cursor.fetchall()
        attr = ['해당없음', '구축요청', '완료', '']
        i = 0
        for elem in rows:
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            j = 0
            for t in elem:
                try: a = int(str(t - today).split(' ')[0])
                except: a = 0
                if t == None: t = ''
                if j == 0:
                    # 해당 필드 숫자 형식으로 바꾸기 위함.
                    item = QTableWidgetItem()
                    item.setData(QtCore.Qt.DisplayRole, t)
                    self.tableWidget.setItem(i, j, QTableWidgetItem(item))
                elif j in (12, 14, 16):
                    comboBox = QtWidgets.QComboBox()
                    comboBox.wheelEvent = lambda event: None
                    comboBox.addItems(attr)
                    text = 0
                    if t == '해당없음': text = 0
                    if t == '구축요청': text = 1
                    if t == '완료': text = 2
                    if t == None: text = 3
                    comboBox.setCurrentIndex(text)
                    self.tableWidget.setCellWidget(i, j, comboBox)
                elif j in (13, 15, 17):
                    item = QTableWidgetItem()
                    item.setData(QtCore.Qt.DisplayRole, t)
                    item.setBackground(QtGui.QColor(129, 216, 208))
                    self.tableWidget.setItem(i, j, QTableWidgetItem(item))
                elif j == 20:
                    t = str(t).replace('\\\\', '\\')
                    self.tableWidget.setItem(i, j, QTableWidgetItem(t))
                elif j in (18, 19):
                    chkBoxItem = QTableWidgetItem()
                    if t == 'Yes':
                        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        chkBoxItem.setCheckState(QtCore.Qt.Checked)
                        self.tableWidget.setItem(i, j, QTableWidgetItem(chkBoxItem))
                    else:
                        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                        self.tableWidget.setItem(i, j, QTableWidgetItem(chkBoxItem))
                elif j == 4 and t < today:  # 지연 대상들 빨간색
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                    self.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 102, 102))
                elif j == 4 and a < 11:  # 임박 10일 대상들 노란색
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                    self.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 204, 102))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.statusbar.showMessage('count : ' + str(len(rows)))  # 상태 창에 전체 카운트 출력
        self.db_connect().close()

    def checkchanged(self, item):# 체크박스 체인지 할때의 실행.
        column = item.column()
        try:
            if item.checkState() == QtCore.Qt.Checked:
                if column in (18,19) :
                    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
                    t_port = "5432"  # default postgres port
                    t_dbname = "postgres"
                    t_user = "postgres"
                    t_pw = "rjator"
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
                    print(content, '확인 필드 업데이트 완료')
                else : pass
            elif item.checkState() == QtCore.Qt.Unchecked:
                if column in (18, 19):
                    print('"%s" Unchecked' % item.text())
                    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
                    t_port = "5432"  # default postgres port
                    t_dbname = "postgres"
                    t_user = "postgres"
                    t_pw = "rjator"
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
                    print(content, '확인 필드 업데이트 완료')
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
                if self.keywords[j]:
                    if item.text() not in self.keywords[j]:
                        columnsShow[i] = False
        for key in columnsShow:
            self.tableWidget.setRowHidden(key, not columnsShow[key])

    def columnfilterclicked(self, index):
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
        self.db_connect().close()
        self.statusbar.clearMessage()
        self.tableWidget.clear()
        QMessageBox.warning(self.tableWidget, '알림', '5초 후 에 조회 버튼을 눌러주세요.\n너무 빠르게 재조회 시 테이블이 정상적으로 로딩 되지 않습니다.')

    def inquiry(self): # 조회버튼 클릭시.
        self.db_connect().close()
        today = datetime.date.today()
        try:
            self.statusbar.clearMessage()
            self.db_connect().close()
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(
                ['NID\nNID','유형\nTYPE', '제목\nTEXT', 'LCODE\nLCODE', '구축시한\nLIMIT_DATE', '준공일\nCOMPLETE_DATE','높이제한\nHEIGHT_LIMIT', '중량제한\nWEIGHT_LIMIT', '시간제\nTIME_ID', '도로공사종류\nROAD_WORK',
                 '실사결과\nRESULT', '실사일정\nREQUEST_DATE','POI상태\nPOI_CAT', 'POI구축일\nPOI_DATE','NET상태\nNET_CAT', 'NET구축일\nNET_DATE','MAP상태\nMAP_CAT', 'MAP구축일\nMAP_DATE', '데이터확인\nDATA_CHECK', '서비스확인\nSERVICE_CHECK', 'URL\nURL',
                 '최초생성일\nCREATE_DATE', '최종수정일\nUPDATE_DATE'])
            query = "select nid, type, text, lcode, limit_date, complete_date, height_limit, weight_limit, time_id,road_work, result, request_date, poi_cat, poi_date, net_cat, net_date, map_cat, map_date, data_check, service_check, url, create_date, update_date from cmms_list where del_flag = '0'"+self.query_line.text()+';'
            self.cursor = self.db_connect().cursor()
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            attr = ['해당없음', '구축요청', '완료', '']
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
                    elif j in (12, 14, 16):
                        comboBox = QtWidgets.QComboBox()
                        comboBox.wheelEvent = lambda event: None
                        comboBox.addItems(attr)
                        text = 0
                        if t == '해당없음': text = 0
                        if t == '구축요청': text = 1
                        if t == '완료': text = 2
                        if t == None: text = 3
                        comboBox.setCurrentIndex(text)
                        self.tableWidget.setCellWidget(i, j, comboBox)
                    elif j in (13, 15, 17):
                        item = QTableWidgetItem()
                        item.setData(QtCore.Qt.DisplayRole, t)
                        item.setBackground(QtGui.QColor(129, 216, 208))
                        self.tableWidget.setItem(i, j, QTableWidgetItem(item))
                    elif j == 20:
                        t = str(t).replace('\\\\', '\\')
                        self.tableWidget.setItem(i, j, QTableWidgetItem(t))
                    elif j in (18, 19):
                        chkBoxItem = QTableWidgetItem()
                        if t == 'Yes':
                            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                            chkBoxItem.setCheckState(QtCore.Qt.Checked)
                            self.tableWidget.setItem(i, j, QTableWidgetItem(chkBoxItem))
                        else:
                            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                            self.tableWidget.setItem(i, j, QTableWidgetItem(chkBoxItem))
                    elif j == 4 and t < today:  # 지연 대상들 빨간색
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                        self.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 102, 102))
                    elif j == 4 and a < 11:  # 임박 10일 대상들 노란색
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                        self.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 204, 102))
                    else:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                    j += 1
                i += 1
            self.statusbar.showMessage('count : ' + str(len(rows)))  # 상태 창에 전체 카운트 출력
            self.db_connect().close()
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
        if item.column() == 20:
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

    def updateData(self): # 수정후 엔터 입력시 이벤트에 연결 할 DB 업데이트 문
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
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
                content = str(content[0:4] + '-' + content[4:6] + '-' + content[6:8])
                if content == '--' : content = 'NULL'
            if column == 14: column_name = 'net_cat'
            if column == 15:
                column_name = 'net_date'
                content = str(content[0:4] + '-' + content[4:6] + '-' + content[6:8])
                if content == '--': content = 'NULL'
            if column == 16: column_name = 'map_cat'
            if column == 17:
                column_name = 'map_date'
                content = str(content[0:4] + '-' + content[4:6] + '-' + content[6:8])
                if content == '--': content = 'NULL'
            if column == 18: column_name = 'data_check'
            if column == 19: column_name = 'service_check'
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

    def sellClickCopy(self):
        try:
            select_item = self.tableWidget.currentItem()
            row = select_item.row()
            column = select_item.column()
            content = self.tableWidget.item(row, column).text().strip()
            clipboard = QtGui.QGuiApplication.clipboard()
            clipboard.setText(content)
            event = QtCore.QEvent(QtCore.QEvent.Clipboard)
            app.sendEvent(clipboard, event)
            print(row , column, content)
        except : pass

    def RoadOpenList(self):
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw, options="-c search_path=cmms")
        csv_file = open("도로개통정보.csv", "w")
        writer = csv.writer(csv_file, lineterminator="\n", delimiter='}', quoting=csv.QUOTE_NONE, escapechar='\\')
        csv_file.write("TEXT}NID}TYPE}ROAD_WORK}TIME_ID}COMPLETE_DATE}LIMIT_DATE}NET_DATE\n")
        query = "select text, nid, type, road_work,time_id, complete_date,limit_date,net_date from cmms_list where type not in ('아파트','시설') and net_cat = '구축완료' and del_flag ='0' order by complete_date"
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        for r in row:
            writer.writerow(r)
        csv_file.close()
        self.db_connect().close()

    def EntireList(self):
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw, options="-c search_path=cmms")
        csv_file = open("전체리스트.csv", "w")
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

    def MonitoringList(self):
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw, options="-c search_path=cmms")
        csv_file = open("모니터링리스트.csv", "w")
        writer = csv.writer(csv_file, lineterminator="\n", delimiter='}', quoting=csv.QUOTE_NONE, escapechar='\\')
        csv_file.write("TYPE}TEXT}LCODE}COMPLETE_DATE\n")
        query = "select type, text, lcode, complete_date from cmms_list where del_flag ='0' order by complete_date"
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        for r in row:
            writer.writerow(r)
        csv_file.close()
        self.db_connect().close()

    def ListExportButton(self):# 콤보 박스 별로 실행되는 함수 다르게 설정
        print(self.exportOption.currentText())
        if self.exportOption.currentText() == '도로개통정보':
            self.RoadOpenList()
            QMessageBox.information(self.tableWidget,"도로개통정보", "추출 완료")
        if self.exportOption.currentText() == '모니터링리스트':
            self.MonitoringList()
            QMessageBox.information(self.tableWidget,"모니터링리스트", "추출 완료")
        if self.exportOption.currentText() == '전체리스트':
            self.EntireList()
            QMessageBox.information(self.tableWidget,"전체리스트", "추출 완료")
        if self.exportOption.currentText() == '업데이트내역서':
            self.update_txt_export()
            QMessageBox.information(self.tableWidget,"업데이트내역서", "추출 완료")
        else: pass

    def shp_export(self): ##shp 뽑기 위한 함수 모음.
        # 현재 화면의 nid값을 가져오기.
        try:
            nid_list = []
            for ss in range(0,self.tableWidget.rowCount()+1):
                item = self.tableWidget.item(ss,0)
                if item is not None:
                    txt = item.text()
                    nid_list.append(txt)

            nid_list = str(nid_list).replace('[','(').replace(']',')')

            #화면의 nid값과 일치하는 oracle 좌표 값 csv로 저장.
            LOCATION = r"C:\ora64\instantclient_21_3"
            os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]
            db = cx_Oracle.connect('contentsteam', 'zjsxpscm', '192.168.10.30:1521/imdb', encoding='UTF-8',
                                   nencoding='UTF-8')
            cursor = db.cursor()
            csv_file = open("sdo_geometry.csv", "w")
            writer = csv.writer(csv_file, lineterminator="\n",delimiter='|')
            query = ("SELECT nid, sdo_util.to_wktgeometry(gshape) as cord FROM imduser.tbw_dt_infocol where nid in {}").format(nid_list)
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
                    geo = str(s[1]).replace('POLYGON ', '').replace(', ', '), (').replace(' ', ',').replace(',,',
                                                                                                            ',').replace(
                        '),(', '), (').replace('((', '(').replace('))', ')')
                    data.append({'nid': s[0], 'geos': geo})

            schema = {
                'geometry': 'Polygon',
                'properties': {'id': 'int'},
            }

            # Write a new Shapefile
            with fiona.open('cmms_shp_export', 'w', 'ESRI Shapefile', schema) as c:
                ## If there are multiple geometries, put the "for" loop here
                for ss in data:
                    ids = ss['nid']
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
                    c.write({'geometry': mapping(poly), 'properties': {'id': ids}})
        except :
            QMessageBox.warning(self.tableWidget, '실패', 'row count 가 1000개 이상인지 확인')
        else:
            QMessageBox.information(self.tableWidget, "SHP 추출 완료", "성공")

    def update_txt_export(self):
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        self.conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw, options="-c search_path=cmms")
        outfile = codecs.open('업데이트내역서.txt', 'a')
        query = "select lcode, text, type from cmms_list where map_cat = '완료' and limit_date between "+self.query_line.text()+';'
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        print(row)
        for r in row:
            r = str(r).replace("'","").replace('(','').replace(')','')+' 배경 업데이트'+'\n'
            outfile.write(r)
        outfile.close()
        self.db_connect().close()

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

