# 05-04 params 정보 일부 변경이 있어서 호출 params 수정.
import json
import time
import codecs
import requests
import random
import datetime
from datetime import datetime

def main():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\이마트(휴무일)_{}.txt'.format(today)

    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("NAME|ID|OLD_ADDR|NEW_ADDR|TELL|WORK_TIME|CLOSE_DATE1|CLOSE_DAY1|CLOSE_DATE2|CLOSE_DAY2|CLOSE_DATE3|CLOSE_DAY3"
                  "|XCORD|YCORD\n")

    date = datetime.date.fromtimestamp(time.time())
    month = str(date).split('-')[1]
    year = str(date).split('-')[0]
    print(month)

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

main()