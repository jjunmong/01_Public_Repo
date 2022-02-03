import sys
import time
import requests
import random
import codecs
import bs4
import json

def getStoreInfoIdList():
    result = []
    maxPage = int(getStoreInfoId(1)[1] / 10 + 2)
    print('최대 수집 페이지 :',maxPage)
    page =87
    while True:
        result = result + getStoreInfoId(page)[0]
        print(page)
        if page == maxPage: break
        page+=1
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def getStoreInfoId(intPageNo):
    url = 'https://www.kobis.or.kr/kobis/business/mast/thea/findTheaterInfoList.do'
    data ={
        'CSRFToken': 'gdQYH69w44bJazoHKarJYjra0mKmsDAtT9TVAHthb9c',
        # 'pageIndex': '1',
        'theaCd': '',
        'sTheaNm': '',
        'sTheaCd': '',
        'sPermYn': 'Y',
        'sJoinYn': 'Y',
        'sWideareaCd': '',
        'sBasareaCd': '',
        'sSaleStat': '',
        'sSenderCd': '',
    }
    data['pageInex']=intPageNo
    pageString = requests.post(url,data =data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find('tbody').find_all('tr')
    totalcount = int(bsObj.find('em',{"class":"fwb"}).text.replace('총 ','').replace('건',''))
    state = bsObj.find('td',{"class":"last-child"}).text
    result = []
    for info in tbody:
        a = info.find('a')['onclick'].split(',')[2].strip().replace(');return false;','').replace("'","")
        result.append({'code':a,'state':state})
    return result, totalcount

def getStoreInfo(storeCode,state):
    url = 'https://www.kobis.or.kr/kobis/business/mast/thea/findTheaterCodeLayer.do?theaCd={}'.format(storeCode)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = bsObj.find('strong',{"class":"tit"}).text
    tell = bsObj.select_one('#pop_content02 > table.tbl_99 > tbody > tr:nth-child(2) > td:nth-child(2)').text.replace('\r','').replace('\n','').replace('\t','').strip()
    addr = bsObj.select_one('#pop_content02 > table.tbl_99 > tbody > tr:nth-child(4) > td').text.replace('\r','').replace('\n','').replace('\t','').strip()
    result.append({'name': name, 'addr': addr, 'tell': tell,'state':state})
    return result

# for ss in getStoreInfoIdList():
#     print(ss)
print(getStoreInfo('002171','영업'))