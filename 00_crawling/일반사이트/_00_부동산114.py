import sys
import codecs
import requests
import bs4
import random
import time

def main():

    outfile = codecs.open('49_부동산114.txt', 'w', 'utf-8')
    outfile.write("GUBUN|NAME|ADDR|DATE1|DATE2\n")

    sido_list = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시',
                 '광주광역시', '대구광역시', '부산광역시', '세종특별자치시', '제주특별자치도']
    for sido in sido_list:
        for num in range(2,6):
            page = 1
            while True:
                store_list = getStoreInfo(sido,page, num)
                if store_list == [] : break
                for store in store_list:
                        outfile.write(u'%s|' % store['gubun'])
                        outfile.write(u'%s|' % store['name'])
                        outfile.write(u'%s|' % store['addr'])
                        outfile.write(u'%s|' % store['date1'])
                        outfile.write(u'%s\n' % store['date2'])
                page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(sido,intPageNo,tabGubun):
    url = 'https://www.r114.com/?_c=lots&_s=info&_m=infolist&_a=index.ajax'
    data ={
        # 'page': '2',
        'Metro': '서울특별시',
        'County': '',
        'Town': '',
        'sortTag': '사업단계',
        'sortTag2': 'DESC',
        'tabGubun': '2',
        'filterParam1': '',
        'filterParam3': '전체',
        'filterParam4': '',
        'filterParam5': '',
        'filterParam6': '',
        'filterParam7': '',
    }
    data['page'] = intPageNo
    data['tabGubun'] = tabGubun
    data['Metro'] = sido
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '244',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'ASPSESSIONIDCSDDRACT=GKENFEKBOEGKNEOLFJADDHMP; ACEUACS=1579483474047131591; ACEFCID=UID-5EEC246F7D6F066E97814CD7; ACEUCI=1; ACEUCI2=1; nvtk=; _ga=GA1.2.2052223262.1592534128; _gid=GA1.2.1212462034.1592534128; foot_navi=opennavi; Memul%5FComplexNm=; Memul%5FComplexCd=; Memul%5FCortarNo=1100000000; fCode=AA%7CAB; Memul%5FAddr=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%7C%7C%7C126%2E9786567859313%7C37%2E566826005485716; Memul%5FMemulType2=01; Memul%5FMemulType1=A01; Memul%5FMemulStyle=0; wcs_bt=8c647232a98f8:1592534204|55e2425a0e97f4:1592534127; _ACU100396=1592534128829131597.1592534206434.1.0.131597M4UIUTK3BAU46.0.0.0.....; _ACR0=b5bf73baf0bb36d94ea044e8d160542777bdf9f4; _ACS100396=1140',
        'Host': 'www.r114.com',
        'Origin': 'https://www.r114.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.r114.com/?_c=lots&_s=info&_m=infolist',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    try:
        pageString = requests.post(url, data = data, headers = headers).text
        bsObj = bs4.BeautifulSoup(pageString,"html.parser")
        print(sido, intPageNo, tabGubun)
        tbody = bsObj.find('tbody',{"class":"InfoList"})
        tr = tbody.find_all('tr')
    except : pass
    result = []
    for info in tr:
        try:
            infos = info['data-info']
            infos = str(infos).split('$')
            gubun = infos[0]
            name = infos[1]
            addr = infos[2]+ ' ' + infos[3]+ ' ' + infos[4]+ ' ' + infos[5]
            date1 = infos[9]
            date2 = infos[10]
        except: pass
        else:
            result.append({"gubun":gubun,"name":name,"addr":addr,"date1":date1,"date2":date2})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

