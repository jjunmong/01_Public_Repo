import json
import datetime
import time
import codecs
import requests
import random
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\05_3_이마트정보(휴무일)\\') == False : os.makedirs('수집결과\\05_3_이마트정보(휴무일)\\')
outfilename = '수집결과\\05_3_이마트정보(휴무일)\\이마트(휴무일)_{}.txt'.format(today)
outfilename_true = '수집결과\\05_3_이마트정보(휴무일)\\이마트(휴무일)_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\05_3_이마트정보(휴무일)\\이마트(휴무일)_{}.log_실패.txt'.format(today)
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
    outfile.write("NAME|ID|OLD_ADDR|NEW_ADDR|TELL|WORK_TIME|CLOSE_DATE1|CLOSE_DAY1|CLOSE_DATE2|CLOSE_DAY2|CLOSE_DATE3|CLOSE_DAY3"
                  "|XCORD|YCORD\n")

    month = str(datetime.today()).split('-')[1]
    year = str(datetime.today()).split('-')[0]
    print(year, month)

    store_list = getInfo(month, year)
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['id'])
        outfile.write(u'%s|' % store['old_addr'])
        outfile.write(u'%s|' % store['new_addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['work_time'])
        outfile.write(u'%s|' % store['close_date1'])
        outfile.write(u'%s|' % store['close_day1'])
        outfile.write(u'%s|' % store['close_date2'])
        outfile.write(u'%s|' % store['close_day2'])
        outfile.write(u'%s|' % store['close_date3'])
        outfile.write(u'%s|' % store['close_day3'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getInfo(month, year):
    url = 'https://store.emart.com/branch/searchList.do'
    data={
        'srchMode': 'jijum',
        'areaId': '',
        'sHanSort': '',
        'eHanSort': '',
        # 'year': '2021',
        # 'month': '02',
        'jMode': 'true',
        'keyword': '',
        'searchType': '',
        'searchOption': ''
    }
    data['month'] = month
    data['year'] = year
    jsonString = requests.post(url, data = data).text
    print(url,data)
    jsonData = json.loads(jsonString)
    entityList = jsonData['dataList']
    data = []
    for info in entityList:
        name = info['NAME']
        id = info['ID']
        old_addr = info['ADDRESS3']
        new_addr = info['ADDRESS1']
        tell = info['CULTURE_TEL']
        work_time = info['STORE_SHOPPING_TIME']
        close_date1 = info['HOLIDAY_DAY1_YYYYMMDD']
        close_day1 = info['HOLIDAY_DAY1_DAY']
        close_date2 = info['HOLIDAY_DAY2_YYYYMMDD']
        close_day2 = info['HOLIDAY_DAY2_DAY']
        close_date3 = info['HOLIDAY_DAY3_YYYYMMDD']
        close_day3 = info['HOLIDAY_DAY3_DAY']
        xcord = info['MAP_X']
        ycord = info['MAP_Y']
        data.append({'name':name,'id':id,'old_addr':old_addr,'new_addr':new_addr,'tell':tell,'work_time':work_time,'close_date1':close_date1
                     ,'close_day1':close_day1,'close_date2':close_date2,'close_day2':close_day2,'close_date3':close_date3,'close_day3':close_day3
                     ,'xcord':xcord,'ycord':ycord})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()