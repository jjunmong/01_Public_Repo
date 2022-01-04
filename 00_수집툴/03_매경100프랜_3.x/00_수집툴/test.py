import sys
import time
import codecs
import requests
import random
import json
import bs4

def getStoreInfo_list(intPageNo):
    url = 'http://safestay.visitkorea.or.kr/usr/mbkinfo/mbkinfo/mbkInfoSelectList.kto;jsessionid=74dxLR1nCMEhd82BjwbuVwSuqO7IYqFGhOChkJyhLVZE89F1V5dDjYRr57V2Shl4'
    data = {
        'currentMenuSn': '16',
        # 'pageIndex': '2',
        'lcdSn': '41',
        'mcdVal': '',
        'cdVal': '',
        'lodgeSn': '',
        'totalSearchText': '',
        'searchLodgeTypeCd': '',
        'searchKqmark': '',
        'searchLodgeStateCd': '',
        'searchLodgeSidoCd': '',
        'searchLodgeGugunCd': '',
        'searchLodgePermitStdDy': '',
        'searchLodgePermitEndDy': '',
        'searchText': '',
    }
    data['pageIndex'] = intPageNo
    pageString = requests.post(url = url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            col1 = info.find('a')['href']
            col1 = str(col1).replace("javascript:fnSelectDetail('","").replace("');","")
        except: pass
        else:
            result.append({'col1':col1, 'no':intPageNo})
    return result

def getStroeInfo_List_all():
    page = 1
    result = []
    while True:
        result = result + getStoreInfo_list(page)
        if getStoreInfo_list(page) == [] : break
        print(page)
    return result

def getStoreInfo(col1, no):
    url = 'http://safestay.visitkorea.or.kr/usr/mbkinfo/mbkinfo/mbkInfoSelectDetail.kto'
    data = {
        'currentMenuSn': '16',
        'pageIndex': '2',
        'lcdSn': '41',
        'mcdVal': '',
        'cdVal': '',
        # 'lodgeSn': '',
        'totalSearchText': '',
        'searchLodgeTypeCd': '',
        'searchKqmark': '',
        'searchLodgeStateCd': '',
        'searchLodgeSidoCd': '',
        'searchLodgeGugunCd': '',
        'searchLodgePermitStdDy': '',
        'searchLodgePermitEndDy': '',
        'searchText': '',
    }
    data['lodgeSn'] = col1
    data['pageIndex'] = no
    pageString = requests.post(url = url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(1) > td.col2')).replace('[','').replace(']','')
    name = name.replace('<td class="col2" headers="lodgeNmTh">','').replace('</td>','')
    cate = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(1) > td.col4')).replace('[','').replace(']','')
    cate = cate.replace('<td class="col4" headers="lodgeTypeCdNmTh">', '').replace('</td>', '')
    addr = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(2) > td')).replace('[','').replace(']','').replace('\r','').replace('\n','').replace('\t','').replace('\n','')
    addr = addr.replace('<td class="col2" colspan="3" headers="lodgeAddrTh">','').replace('</td>','')
    idx = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(3) > td.col2')).replace('[','').replace(']','')
    idx = idx.replace('<td class="col2" headers="lodgePermitNoTh">', '').replace('</td>', '')
    date = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(3) > td.col4')).replace('[','').replace(']','').replace('\r','').replace('\n','').replace('\t','')
    date = date.replace('<td class="col4" headers="lodgePermitDyTh">', '').replace('</td>', '')
    openinfo = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(4) > td.col2')).replace('[','').replace(']','').replace('\r','').replace('\n','').replace('\t','')
    openinfo = openinfo.replace('<td class="col2" headers="lodgeStateCdNmTh">', '').replace('</td>', '').replace(' ','')
    result.append({'idx':idx,'name':name,'cate':cate,'addr':addr,'date':date,'openinfo':openinfo})
    return result

print(getStoreInfo(6711,3))