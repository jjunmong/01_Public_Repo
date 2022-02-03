# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import bs4
import requests
import openpyxl
from PyQt5.QtWidgets import QApplication
import pandas as pd

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox.setText("VIEW수집포함")
        self.checkbox.setGeometry(QtCore.QRect(530, 90, 111, 41))
        self.checkbox.setObjectName("checkbox")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 91, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 58, 91, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 141, 41))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 30, 241, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 68, 241, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        rx = QtCore.QRegExp("[0-9]{30}")  # +++
        val = QtGui.QRegExpValidator(rx)  # +++
        self.lineEdit_3.setValidator(val)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 108, 51, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(360, 50, 191, 16))
        self.label_4.setObjectName("label_4")
        self.Start_crawl = QtWidgets.QPushButton(self.centralwidget)
        self.Start_crawl.setGeometry(QtCore.QRect(530, 40, 111, 41))
        self.Start_crawl.setObjectName("Start_crawl")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 140, 781, 431))
        self.textBrowser.setObjectName("textBrowser")
        self.End_crawl = QtWidgets.QPushButton(self.centralwidget)
        self.End_crawl.setGeometry(QtCore.QRect(650, 40, 111, 41))
        self.End_crawl.setObjectName("End_crawl")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(230, 110, 191, 16))
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.Start_crawl.clicked.connect(self.Crawl_News)
        self.End_crawl.clicked.connect(QCoreApplication.instance().quit)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.lineEdit_3.setValidator(QtGui.QIntValidator(self.centralwidget))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("NewsCrawling", "NewsCrawling"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">시작 날짜</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">종료 날짜</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">호출 페이지 설정</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "입력 예시) 2021.05.28"))
        self.Start_crawl.setText(_translate("MainWindow", "수집 시작"))
        self.End_crawl.setText(_translate("MainWindow", "종료"))
        self.label_5.setText(_translate("MainWindow", "@\'5\' 입력시 5페이지 까지 수집"))

    def Crawl_News(self):
        searchName_list = self.searchList()

        pageNum = self.lineEdit_3.text()
        pageNum1 = int(pageNum)+1
        pageNum2 = (int(pageNum)+1) * 10
        start_day = self.lineEdit.text()
        end_day = self.lineEdit_2.text()

        start_day_daum = self.lineEdit.text()
        end_day_daum = self.lineEdit_2.text()

        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = 'NEWS'
        sheet.append(["검색어", "HEADLINE", "URL", "TIMELINE","MEDIA","CAT"])

        sheet2 = wb.create_sheet()
        sheet2.title = 'NAVER_VIEW'
        sheet2.append(["검색어", "HEADLINE", "URL", "TIMELINE","MEDIA","CAT"])

        for name in searchName_list:
            if name == searchName_list[0] : continue
            for page in range(1, pageNum2, 10):
                try:
                    news_list = self.NaverNewsInfo(name, start_day, end_day, page)
                    print(len(news_list),name, start_day, end_day, page)
                    if len(news_list) < 10 :
                        for news in news_list:
                            sheet.append([name, news['headLine'], news['url'],news['timeLine'], news['cat'], news['media']])
                            QApplication.processEvents()
                        self.textBrowser.append("네이버뉴스" + "  |  " + str(page) + "페이지" + "  |  " + "검색어 : " + str(name))
                        break
                except: pass
                else:
                    for news in news_list:
                        sheet.append([name, news['headLine'], news['url'],news['timeLine'], news['cat'], news['media']])
                        QApplication.processEvents()
                self.textBrowser.append("네이버뉴스"+"  |  "+str(page)+"페이지"+"  |  "+"검색어 : "+str(name))

        self.textBrowser.append("네이버 뉴스 기사 수집 완료")

        for name in searchName_list:
            if name == searchName_list[0]: continue
            for page in range(1, pageNum1):
                try:
                    news_list = self.DaumNewsInfo(name, start_day_daum, end_day_daum,page)
                    print(len(news_list),name, start_day, end_day, page )
                    if len(news_list) < 10:
                        for news in news_list:
                            sheet.append([name, news['headLine'], news['url'],news['timeLine'], news['cat'], news['media']])
                            QApplication.processEvents()
                        self.textBrowser.append("다음뉴스"+"  |  "+str(page)+"페이지"+"  |  "+"검색어 : "+str(name))
                        break
                except : pass
                else:
                    for news in news_list:
                        sheet.append([name, news['headLine'], news['url'],news['timeLine'], news['cat'], news['media']])
                        QApplication.processEvents()
                self.textBrowser.append("다음뉴스"+"  |  "+str(page)+"페이지"+"  |  "+"검색어 : "+str(name))

        self.textBrowser.append("다음 뉴스 기사 수집 완료")

        if self.checkbox.isChecked() :
            for name in searchName_list:
                if name == searchName_list[0]: continue
                for page in range(1, pageNum2, 30):
                    try:
                        news_list = self.NaverViewInfo(name, start_day_daum, end_day_daum, page)
                        print(len(news_list),name, start_day, end_day, page )
                        if len(news_list) < 30:
                            for news in news_list:
                                sheet2.append([name, news['headLine'], news['url'],news['timeLine'], news['cat'], news['media']])
                                QApplication.processEvents()
                            self.textBrowser.append("네이버VIEW"+"  |  "+str(page)+"페이지"+"  |  "+"검색어 : "+str(name))
                            break
                    except: pass
                    else:
                        for news in news_list:
                            sheet2.append([name, news['headLine'], news['url'],news['timeLine'], news['cat'], news['media']])
                            QApplication.processEvents()
                    self.textBrowser.append("네이버VIEW"+"  |  "+str(page)+"페이지"+"  |  "+"검색어 : "+str(name))
            self.textBrowser.append("NAVER VIEW 수집 완료")
        else : pass

        wb.save('뉴스기사수집결과.xlsx')

        # apart = pd.read_excel("뉴스기사수집결과.xlsx")
        # df = pd.DataFrame(apart)
        # ds = df.drop_duplicates(['HEADLINE'], keep='first')
        # ds.to_excel('뉴스기사수집결과_중복제거.xlsx', 'w')

        apart = pd.read_excel("뉴스기사수집결과.xlsx", sheet_name='NEWS')
        df = pd.DataFrame(apart)
        ds = df.drop_duplicates(['HEADLINE'], keep='first')

        apart2 = pd.read_excel("뉴스기사수집결과.xlsx", sheet_name='NAVER_VIEW')
        df2 = pd.DataFrame(apart2)
        ds2 = df2.drop_duplicates(['HEADLINE'], keep='first')

        with pd.ExcelWriter('뉴스기사수집결과_중복제거.xlsx') as writer:
            ds.to_excel(writer, sheet_name='NEWS')
            ds2.to_excel(writer, sheet_name='NAVER_VIEW')

        self.textBrowser.append("전체 수집 완료")

    def searchList(self):
        with open('Crawling_keywords.txt') as data:
            lines = data.read().splitlines()
        SearchList = lines
        return SearchList

    def NaverNewsInfo(self,SearchName, StratDate, EndDate, page):
        url = 'https://search.naver.com/search.naver'
        data = {
            'where': 'news',
            'sm': 'tab_pge',
            # 'query': 'KT 공사',
            'field': '0',
            'sort': '0',
            'photo': '0',
            'pd': '3',
            # 'ds': '2021.05.27',
            # 'de': '2021.05.31',
            # 'cluster_rank': '68',
            'mynews': '0',
            'office_type': '0',
            'office_section_code': '0',
            'news_office_checked': '',
            # 'nso': 'so:r,p:from20210527to20210531,a:all',
            # 'start': '21',
        }
        data['ds'] = str(StratDate)
        data['de'] = str(EndDate)
        data['start'] = page
        data['query'] = SearchName

        pageString = requests.get(url=url, params=data).text
        bsObj = bs4.BeautifulSoup(pageString, "html.parser")
        ul = bsObj.find('ul', {"class": "list_news"})
        li = ul.find_all('li')
        result = []
        for info in li:
            media_info = info.find('div', {"class": "info_group"})

            try:
                media = media_info.find('a').text
            except:
                media = ''

            try:
                url = info.find('a', {"class": "news_tit"})['href']
            except:
                url = ''

            try:
                headLine = info.find('a', {"class": "news_tit"}).text.replace('\xa0', '').replace('\n','')
                headLine = str(headLine).replace('  ','')
            except:
                headLine = ''

            try:
                timeLine = info.find('span', {"class": "info"}).text
                if timeLine.endswith('단') or timeLine.endswith('TOP') == True:
                    timeLine = info.select('span', {"class": "info"})[2]
                    timeLine = str(timeLine).replace('<span class="info">', '').replace('</span>', '')
            except:
                timeLine = ''

            if media == '':
                pass
            else:
                result.append({'searchName':SearchName, "headLine": headLine, "url": url, "timeLine": timeLine,'media': media,'cat':'NAVER_NEWS'})
        return result

    #6월 29일 자로 태그의 값들이 바뀌어서 버전2 로 수정
    #v1
    # def DaumNewsInfo(self, SearchName, StratDate, EndDate, page):
    #     url = 'https://search.daum.net/search'
    #     data = {
    #         'nil_suggest': 'btn',
    #         'w': 'news',
    #         'DA': 'PGD',
    #         'cluster': 'y',
    #         # 'q': 'KT 공사',
    #         # 'sd': '20210527000000',
    #         # 'ed': '20210531235959',
    #         'period': 'u',
    #         # 'p': '2',
    #     }
    #     data['q'] = SearchName
    #     data['sd'] = str(StratDate).replace('.','') + '000000'
    #     data['ed'] = str(EndDate).replace('.','') + '235959'
    #     data['p'] = page
    #     pageString = requests.get(url=url, params=data).text
    #     bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    #     ul = bsObj.find('ul', {"id": "clusterResultUL"})
    #     li = ul.findAll('li')
    #     result = []
    #     for info in li:
    #         mediaInfo = info.find('span', {"class": "f_nb date"}).text
    #         mediaInfo = mediaInfo.split('|')
    #         media = mediaInfo[1].strip()
    #         headLine = info.find('a', {"class": "f_link_b"}).text
    #
    #         url = info.find('a')['href']
    #         timeLine = mediaInfo[0].strip()
    #
    #         result.append({'searchName': SearchName, 'headLine': headLine,'url': url, 'timeLine': timeLine, 'media': media, 'cat': 'DAUM_NEWS'})
    #     return result

    #2021.10.19 헤드라인의 태그 값이 바뀌어서 수정.
    # def DaumNewsInfo(self, SearchName, StratDate, EndDate, page):
    #     url = 'https://search.daum.net/search'
    #     data = {
    #         'nil_suggest': 'btn',
    #         'w': 'news',
    #         'DA': 'PGD',
    #         'cluster': 'y',
    #         'enc': 'utf8',
    #         'cluster_page': '1',
    #         # 'q': 'KT 공사',
    #         # 'sd': '20210527000000',
    #         # 'ed': '20210531235959',
    #         'period': 'u',
    #         # 'p': '2',
    #     }
    #     data['q'] = SearchName
    #     data['sd'] = str(StratDate).replace('.', '') + '000000'
    #     data['ed'] = str(EndDate).replace('.', '') + '235959'
    #     data['p'] = page
    #     pageString = requests.get(url=url, params=data).text
    #     bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    #     ul = bsObj.find('ul', {"class": "list_news"})
    #     li = ul.findAll('li')
    #     result = []
    #     for info in li:
    #         media = info.find('span', {"class": "f_nb"}).text
    #         headLine = info.find('a', {"class": "tit_main ff_dot"}).text
    #         url = info.find('a')['href']
    #         timeLine = info.find('span', {"class": "cont_info"}).text.split(' ')[2]
    #         result.append(
    #             {'searchName': SearchName, 'headLine': headLine, 'url': url, 'timeLine': timeLine, 'media': media,
    #              'cat': 'DAUM_NEWS'})
    #     return result

    def DaumNewsInfo(self, SearchName, StratDate, EndDate, page):
        url = 'https://search.daum.net/search'
        data = {
            'nil_suggest': 'btn',
            'w': 'news',
            'DA': 'PGD',
            'cluster': 'y',
            'enc': 'utf8',
            'cluster_page': '1',
            # 'q': 'KT 공사',
            # 'sd': '20210527000000',
            # 'ed': '20210531235959',
            'period': 'u',
            # 'p': '2',
        }
        data['q'] = SearchName
        data['sd'] = str(StratDate).replace('.', '') + '000000'
        data['ed'] = str(EndDate).replace('.', '') + '235959'
        data['p'] = page
        pageString = requests.get(url=url, params=data).text
        bsObj = bs4.BeautifulSoup(pageString, "html.parser")
        ul = bsObj.find('ul', {"class": "list_news"})
        li = ul.findAll('li')
        result = []
        for info in li:
            try:
                media = info.find('span', {"class": "f_nb"}).text
            except:
                media = ''
            try:
                textinfo = info.find('div', {"class": "wrap_cont"})
                headLine = textinfo.find('a').text
            except:
                headLine = ''
            try:
                url = info.find('a')['href']
            except:
                url = ''
            try:
                timeLine = info.find('span', {"class": "cont_info"}).text.split(' ')[2]
            except:
                timeLine = ''
            result.append(
                {'searchName': SearchName, 'headLine': headLine, 'url': url, 'timeLine': timeLine, 'media': media,
                 'cat': 'DAUM_NEWS'})
        return result

    def NaverViewInfo(self,SearchName, StratDate, EndDate, page):
        url = 'https://s.search.naver.com/p/review/search.naver'
        data = {
            'rev': '44',
            'where': 'view',
            'api_type': '11',
            # 'start': '61',
            # 'query': 'KT 공사',
            # 'nso': 'so:r,p:from20210502to20210503,a:all',
            'nqx_theme': '',
            'main_q': '',
            'mode': 'normal',
            'q_material': '',
            'ac': '1',
            'aq': '0',
            'spq': '0',
            'st_coll': '',
            'topic_r_cat': '',
            'nx_search_query': '',
            'nx_and_query': '',
            'nx_sub_query': '',
            'prank': '31',
            'sm': 'tab_opt',
            'ssc': 'tab.view.view',
            'ngn_country': 'KR',
            'lgl_rcode': '09440104',
            'fgn_region': '',
            'fgn_city': '',
            'lgl_lat': '37.541561',
            'lgl_long': '126.949845',
            '_callback': 'viewMoreContents',
        }
        data['nso'] = 'so:r,p:from{}to{},a:all'.format(str(StratDate).replace('.', ''), str(EndDate).replace('.', ''))
        data['start'] = page
        data['query'] = SearchName
        pageString = requests.get(url=url, params=data).text
        pageString = pageString.replace('\\"', '')
        bsObj = bs4.BeautifulSoup(pageString, "html.parser")
        # print(bsObj)
        li = bsObj.find_all('li')
        result = []
        for info in li:
            try:
                media = info.find('a', {"class": "sub_txt"}).text
            except:
                media = ''
            try:
                url = info.find('a', {"class": "api_txt_lines"})['href']
            except:
                url = ''

            try:
                headLine = info.find('a', {"class": "api_txt_lines"}).text.replace('\xa0', '').replace('\n', '')
                headLine = str(headLine).replace('  ', '')
            except:
                headLine = ''
            try:
                timeLine = info.find('span', {"class": "sub_time"}).text
                if timeLine.endswith('단') or timeLine.endswith('TOP') == True:
                    timeLine = info.select('span', {"class": "info"})[2]
                    timeLine = str(timeLine).replace('<span class="info">', '').replace('</span>', '')
            except:
                timeLine = ''

            if media == '':
                pass
            else:
                result.append(
                    {'searchName': SearchName, 'cat': 'NAVER_VIEW', 'media': media, "headLine": headLine,
                     "url": url, "timeLine": timeLine})
        return result

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
