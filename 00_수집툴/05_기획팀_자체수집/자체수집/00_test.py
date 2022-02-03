import bs4
import time
import codecs
import requests
import random
from datetime import datetime
import traceback
import os,sys
import json
import re

def getStoreInfo():
    url = 'https://www.factoryon.go.kr/bbs/frtblRecsroomBbsList.do'
    data = {
        'selectBbsSn': '0',
        'pageIndex': '1',
        'searchCondition': '01',
        'searchKeyword': '',
        'searchBbsCode': '',
        'pageUnit': '50',
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    response = requests.post(url, data=data, headers = headers).text
    pageString = bs4.BeautifulSoup(response, "html.parser")
    tbody = pageString.find('tbody')
    tr = tbody.find_all('tr')
    dataexport = []
    for info in tr:
        try:
            a = info.find('a').text[:8].replace('(', '').replace('.', '')
            a = re.sub(r'[^0-9]', '', a)
        except : pass
        else : dataexport.append(a)
    date_max = max(dataexport)
    data_max_fix1 = '(' + date_max[0:4] + '.' + date_max[4:] + '월)_산단내_신규입주계약업체리스트'
    data_max_fix2 = '(' + date_max[0:4] + '.' + date_max[4:] + '월말기준)_산단공관할단지내_입주업체리스트'
    data_max_fix3 = '(' + date_max[0:4] + '.' + date_max[4:] + '월말기준)_전국(개별,계획)입주업체현황'
    data_max_fix4 = '(' + date_max[0:4] + '.' + date_max[4:] + '월말기준)_전국_지식산업센터현황'
    data_max_fix5 = '(' + date_max[0:4] + '.' + date_max[4:] + '월말기준)_전국등록공장현황'
    result = [data_max_fix1, data_max_fix2, data_max_fix3, data_max_fix4, data_max_fix5]
    return result

getStoreInfo()