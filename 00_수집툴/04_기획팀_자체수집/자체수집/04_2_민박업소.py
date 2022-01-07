import time
import codecs
import requests
import random
import bs4
from datetime import datetime

def main():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\민박업소_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("LIC_ID|LIC_DATE|NAME|ADDR|TELL\n")

    url_list = getStroeInfo_List_all()

    for url in url_list:
        store_list = getStoreInfo(url['col1'], url['no'])
        print(url['col1'], url['no'])
        for store in store_list:
            outfile.write(u'%s|' % store['lic_id'])
            outfile.write(u'%s|' % store['lic_date'])
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        time.sleep(random.uniform(1,2))

    outfile.close()

def getStoreInfo_list(intPageNo):
    url = 'https://safestay.visitkorea.or.kr/usr/mbkinfo/map/mapSelectDetail.kto'
    data = {
        'currentMenuSn': '105',
        # 'pageIndex': '2',
        'pageUnit': '12',
        'searchGubun1': 'ALL',
        'searchGubun2': '',
        'searchGubun4': '',
        'lodgeSn': '',
        'totalSearchText': '',
    }
    data['pageIndex'] = intPageNo
    pageString = requests.post(url = url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    # tbody = bsObj.find('ul',{"class":"clearfix"})
    li = bsObj.find_all('li')
    result = []
    for info in li:
        try:
            col1 = info.find('a')['href']
            col1 = str(col1).replace("javascript:fnSelectDetail(","").replace(")","")
        except: pass
        else:
            if col1.isdigit() == True : result.append({'col1':col1, 'no':intPageNo})
            else : pass
    return result

# def getStoreInfo(col1, no):
#     url = 'https://safestay.visitkorea.or.kr/usr/mbkinfo/map/mapSelectDetail.kto'
#     data = {
#         'currentMenuSn': '105',
#         # 'pageIndex': '2',
#         'pageUnit': '12',
#         'searchGubun1': 'ALL',
#         'searchGubun2': '',
#         'searchGubun4': '',
#         # 'lodgeSn': '',
#         'totalSearchText': '',
#     }
#     data['lodgeSn'] = col1
#     data['pageUnit'] = no
#     pageString = requests.post(url = url, data = data).text
#     bsObj = bs4.BeautifulSoup(pageString,"html.parser")
#     result = []
#     name = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(1) > td.col2')).replace('[','').replace(']','')
#     name = name.replace('<td class="col2" headers="lodgeNmTh">','').replace('</td>','').upper()
#     cate = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(1) > td.col4')).replace('[','').replace(']','')
#     cate = cate.replace('<td class="col4" headers="lodgeTypeCdNmTh">', '').replace('</td>', '')
#     addr = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(2) > td')).replace('[','').replace(']','').replace('\r','').replace('\n','').replace('\t','').replace('\n','')
#     addr = addr.replace('<td class="col2" colspan="3" headers="lodgeAddrTh">','').replace('</td>','')
#     if addr.startswith('<span>') == True :
#         addr = addr.split('>')[2]
#     idx = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(3) > td.col2')).replace('[','').replace(']','')
#     idx = idx.replace('<td class="col2" headers="lodgePermitNoTh">', '').replace('</td>', '')
#     date = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(3) > td.col4')).replace('[','').replace(']','').replace('\r','').replace('\n','').replace('\t','')
#     date = date.replace('<td class="col4" headers="lodgePermitDyTh">', '').replace('</td>', '')
#     openinfo = str(bsObj.select('#contents-wraper > section > div > div > table > tbody > tr:nth-child(4) > td.col2')).replace('[','').replace(']','').replace('\r','').replace('\n','').replace('\t','')
#     openinfo = openinfo.replace('<td class="col2" headers="lodgeStateCdNmTh">', '').replace('</td>', '').replace(' ','')
#     result.append({'idx':idx,'name':name,'cate':cate,'addr':addr,'date':date,'openinfo':openinfo})
#     return result

def getStoreInfo(col1, no):
    url = 'https://safestay.visitkorea.or.kr/usr/mbkinfo/intro/introSelectDetail.kto'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '115',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '_ga=GA1.3.1636888894.1579503879; JSESSIONID=2JMf4DrICH4oP8vB6PWZGJjo5zMmd1yJWaCQeAgGardG6E0JJpRnvi0JTm75J5p8; _gid=GA1.3.1981452053.1621923093',
        'Host': 'safestay.visitkorea.or.kr',
        'Origin': 'https://safestay.visitkorea.or.kr',
        'Pragma': 'no-cache',
        'Referer': 'https://safestay.visitkorea.or.kr/usr/mbkinfo/intro/introSelectDetail.kto',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }
    data = {
        'currentMenuSn': '105',
        # 'pageIndex': '2',
        'pageUnit': '12',
        'searchGubun1': 'ALL',
        'searchGubun2': '',
        'searchGubun4': '',
        # 'lodgeSn': '',
        'totalSearchText': '',
    }
    data['lodgeSn'] = col1
    data['pageIndex'] = no
    pageString = requests.post(url = url, data = data, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    lic_id = str(bsObj.select('section > div > dl > dd.bizInfo > ul > li:nth-child(1) > span')).replace('[<span>','').replace('</span>]','')
    lic_date = str(bsObj.select('section > div > dl > dd.bizInfo > ul > li:nth-child(2) > span')).replace('[<span>','').replace('</span>]','').replace('\r','').replace('\n','').replace('\t','')
    name = str(bsObj.select('section > div > dl > dt')).replace('[<dt class="hidden">페이지 메뉴</dt>, <dt>','').replace(' </dt>]','')
    name = name.replace('												','').replace('<span class="flag">','').replace('</span>','').replace('\r','').replace('\n','').replace('\t','').replace('</dt>]','').replace('[한국관광 품질인증/Korea Quality]','').rstrip().lstrip()
    addr = str(bsObj.select('section > div > dl > dd.address > p')).replace('[<p>','').replace(' </p>]','').replace('</p>]','')
    tell = str(bsObj.select('ul > li:nth-child(3) > span > span')).replace('[<span>','').replace('</span>]','').replace('\n','')
    tell = tell.replace('[','').replace(']','')
    result.append({'lic_id':lic_id,'lic_date':lic_date,'name':name,'addr':addr,'tell':tell})
    return result

def getStroeInfo_List_all():
    page = 1
    result = []
    while True:
        result = result + getStoreInfo_list(page)
        if getStoreInfo_list(page) == [] : break
        # elif page == 3 : break
        print(page)
        page+=1
    return result

main()