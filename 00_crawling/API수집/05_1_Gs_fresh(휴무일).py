import json
import time
import codecs
import requests
import random
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\05_1_GS_THE_FRESH(휴무일)\\') == False : os.makedirs('수집결과\\05_1_GS_THE_FRESH(휴무일)\\')
outfilename = '수집결과\\05_1_GS_THE_FRESH(휴무일)\\GS_THE_FRESH(휴무일)_{}.txt'.format(today)
outfilename_true = '수집결과\\05_1_GS_THE_FRESH(휴무일)\\GS_THE_FRESH(휴무일)_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\05_1_GS_THE_FRESH(휴무일)\\GS_THE_FRESH(휴무일)_{}.log_실패.txt'.format(today)

def main():
    try:
        Crawl_run()
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

def Crawl_run():
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("CODE|NAME|BRANCH|ADDR|TELL|XCORD|YCORD|CLOSEDATE1|CLOSEDATE2|CLOSEDATE3|CLOSEDATE4|TIME\n")

    pages = pageCount()

    for page in range(1,pages):
        store_list = getStoreInfo(page)
        print(page)
        if store_list == []: break;
        for store in store_list:
            outfile.write(u'%s|' % store['code'])
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s|' % store['closedate1'])
            outfile.write(u'%s|' % store['closedate2'])
            outfile.write(u'%s|' % store['closedate3'])
            outfile.write(u'%s|' % store['closedate4'])
            outfile.write(u'%s\n' % store['time'])
        page += 1
        time.sleep(random.uniform(0.3, 0.6))
    outfile.close()

def getStoreInfo(pageNum):
    url = "http://gsthefresh.gsretail.com/thefresh/ko/market-info/find-storelist"
    data = {
       'searchType': '',
       # 'pageNum': '2',
       'listCnt': '3',
       'pagingCnt': '10',
       'pagingNowIdx': '1',
       'totlPageNum': '1',
       'stb1': '',
       'stb2': '',
       'searchShopName':'',
       'CSRFToken': '7dd36a66-c1b7-47c8-9d31-15267599a282'
    }
    data['pageNum'] = pageNum
    req = requests.get(url, params = data).text
    data = json.loads(req)
    data_all = data['results']
    result = []
    for info in data_all :
            code = info['shopCode']
            name = "GS THE FRESH"
            branch = info['shopName'].rstrip().lstrip().upper()
            addr = info['address'].rstrip().lstrip()
            try:
                tell = info['phone'].rstrip().lstrip().replace(')','-')
            except :
                tell = ''
            xcord = info['lat']
            ycord = info['longs']
            closedate1 = info['closedDate1']
            closedate2 = info['closedDate2']
            closedate3 = info['closedDate3']
            closedate4 = info['closedDate4']
            timeEDH = info['timeEDH']
            timeEDM = info['timeEDM']
            timeSTH = info['timeSTH']
            timeSTM = info['timeSTM']
            try:
                time = timeSTH +':'+ timeSTM +'-'+ timeEDH +':'+ timeEDM
            except: time = ''
            result.append({"code":code,"name":name,"branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord,"closedate1":closedate1,"closedate2":closedate2,"closedate3":closedate3,"closedate4":closedate4,"time":time})
    return result

def pageCount():
    url = "http://gsthefresh.gsretail.com/thefresh/ko/market-info/find-storelist"
    data = {
       'searchType': '',
       'pageNum': '1',
       'listCnt': '3',
       'pagingCnt': '10',
       'pagingNowIdx': '1',
       'totlPageNum': '1',
       'stb1': '',
       'stb2': '',
       'searchShopName':'',
       'CSRFToken': '7dd36a66-c1b7-47c8-9d31-15267599a282'
    }
    req = requests.get(url, params = data).text
    data = json.loads(req)
    page_count = data['pagination']['totalNumberOfResults']
    page_result = int(page_count / 3 + 1)
    return page_result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

