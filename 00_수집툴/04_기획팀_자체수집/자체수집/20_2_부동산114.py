import requests
import bs4
from dateutil.relativedelta import relativedelta
import time
import random
import codecs
from datetime import datetime
import traceback
import os, sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\20_2_부동산114\\') == False : os.makedirs('수집결과\\20_2_부동산114\\')
outfilename = '수집결과\\20_2_부동산114\\부동산114_{}.txt'.format(today)
outfilename_true = '수집결과\\20_2_부동산114\\부동산114_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\20_2_부동산114\\부동산114_{}.log_실패.txt'.format(today)

def main():
    try:
        getIdAll()
        getStoreInfo_all()
        outfile = codecs.open(outfilename_true, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '정상 수집 완료'
        outfile.write(write_text)
        outfile.close()
    except:
        if os.path.isfile(outfilename_true):
            os.remove(outfilename_true)
        outfile = codecs.open(outfilename_false, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '수집 실패' + '|' + str(traceback.format_exc())
        outfile.write(write_text)
        outfile.close()

def getIdAll():
    sido_list = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시',
                 '광주광역시', '대구광역시', '부산광역시', '세종특별시', '제주도']

    six_months_later = datetime.now() + relativedelta(months=6)
    six_months_later = str(six_months_later).split(' ')[0]
    six_months_later_part1 = str(six_months_later).split('-')[0]
    six_months_later_part2 = str(six_months_later).split('-')[1]
    MinDate = six_months_later_part1 + six_months_later_part2

    six_months_before = datetime.now() - relativedelta(months=6)
    six_months_before = str(six_months_before).split(' ')[0]
    six_months_before_part1 = str(six_months_before).split('-')[0]
    six_months_before_part2 = str(six_months_before).split('-')[1]
    MaxDate = six_months_before_part1 + six_months_before_part2

    date_list = []
    n = 0
    while True:
        if n == 7 : break
        dateInfo = str(datetime.now() + relativedelta(months=n)).split(' ')[0]
        year = dateInfo.split('-')[0]
        month = int(dateInfo.split('-')[1])
        date_list.append({'year':year,'month':month})
        n+=1

    outfile = codecs.open('114_id_list.txt', 'w')
    for sido in sido_list:
        for date in date_list:
            page = 1
            while True:
                year = date['year']
                month = date['month']
                print('sido',sido,'|','year',year,'|','month',month,'|','page',page)
                if getStoreId(sido, page, year, MinDate, MaxDate, month) == [] :break
                for ids in getStoreId(sido, page, year, MinDate, MaxDate, month):
                    outfile.write(str(ids)+'|'+str(sido)+'|'+str(year)+'|'+str(month)+'\n')
                page +=1
    outfile.close()

def getStoreId(Sido, intPageNo, Year, MinDate, MaxDate, Month):
    url = 'https://www.r114.com/?_c=lots&_m=ipjuinfo&_a=ipjuajax'
    data = {
        'type_g': '',
        'ArrType_g': '',
        'orderby': '입주시기',
        'ordersort': 'desc',
        # 'page': '1',
        # 'addr1': '서울특별시',
        'addr2': '',
        'addr3': '',
        # 'minDate': '202107',
        # 'maxDate': '202207',
        # 'year': '2022',
        # 'month': '1',
        # 'addr1search': '서울특별시',
    }
    data['addr1'] = Sido
    data['addr1search'] =Sido
    data['page'] = intPageNo
    data['minDate'] = MinDate
    data['maxDate'] = MaxDate
    data['year'] = Year
    data['month'] = Month
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    pageString = requests.post(url,data = data, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    a = bsObj.find_all('a')
    result = []
    for info in a:
        try:
            onclick = info['onclick']
            idInfo = str(onclick).split(', ')[1].replace('");','').replace('"','')
            typeInfo = str(onclick).split(', ')[0].replace('goDetail(','').replace('"','')
        except : pass
        else:
            result.append(idInfo+'|'+typeInfo)
    return result
########################################################################################################################
def getStoreInfo_all():
    with open('114_id_list.txt') as data:
        lines = data.read().splitlines()
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("name|cat|addr|size|date|construc|tell|img\n")

    for info in lines:
        aptcode=info.split('|')[0]
        type_g=info.split('|')[1]
        sido=info.split('|')[2]
        year=info.split('|')[3]
        month=info.split('|')[4]
        store_info = getStoreInfo(aptcode,type_g,sido,year,month)
        print(aptcode, type_g, sido, year, month)
        for info in store_info:
            outfile.write(u'%s|' % info['name'])
            outfile.write(u'%s|' % info['cat'])
            outfile.write(u'%s|' % info['addr'])
            outfile.write(u'%s|' % info['size'])
            outfile.write(u'%s|' % info['date'])
            outfile.write(u'%s|' % info['construc'])
            outfile.write(u'%s|' % info['tell'])
            outfile.write(u'%s\n' % info['img'])
        time.sleep(random.uniform(0.9, 1.2))
    outfile.close()
    data.close()

def getStoreInfo(aptcode,type_g,sido,year,month):
    url = 'https://www.r114.com/'
    data={
        '_c': 'lots',
        '_m': 'lotsinfodetail',
        # 'type_g': 'A',
        'ArrType_g': '',
        'orderby': '입주시기',
        'ordersort': 'desc',
        'page': '1',
        # 'addr1': '경기도',
        'addr2': '',
        'addr3': '',
        # 'year': '2022',
        # 'month': '7',
        'detail': 'ipju',
        # 'aptcode': 'A02740017470001',
    }
    data['type_g'] = type_g
    data['addr1'] = sido
    data['year'] = year
    data['month'] = month
    data['aptcode'] = aptcode
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    pageString = requests.get(url,params = data, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    table = bsObj.find('table',{"class":"tbl_type1 type2 mgt2"})
    tbody = table.find('tbody')
    result = []
    n= 0
    while True:
        try : tbody.select('th')[n].text
        except : break
        else:
            if tbody.select('th')[n].text =='종류' : n1 = n
            if tbody.select('th')[n].text =='주소' : n2 = n
            if tbody.select('th')[n].text =='규모' : n3 = n
            if tbody.select('th')[n].text =='시기' : n4 = n
            if tbody.select('th')[n].text =='건설사' : n5 = n
            if tbody.select('th')[n].text =='문의' : n6 = n
        n+=1
    name = bsObj.find('h4',{"class":"fl bunyangDanjiName"}).text
    cat = tbody.select('td')[n1].text.replace('\xa0', ' ').replace('\n', '')
    addr = tbody.select('td')[n2].text.replace('\xa0', ' ').replace('\n', '')
    size = tbody.select('td')[n3].text.replace('\xa0', ' ').replace('\n', '')
    date = tbody.select('td')[n4].text.replace('\xa0', ' ').replace('\n', '')
    try: construc = tbody.select('td')[n5].text.replace('\xa0', ' ').replace('\n', '').replace('\r', '')
    except : construc = ''
    try:tell = tbody.select('td')[n6].text.replace('\xa0', ' ').replace('\n', '').replace('\r', '')
    except: tell = ''
    try:img = bsObj.find('img', {"class": "BatchImage"})['src']
    except:img=''
    result.append({'name':name,'cat': cat, 'addr': addr, 'size': size, 'date': date, 'construc': construc, 'tell': tell,'img':img})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
