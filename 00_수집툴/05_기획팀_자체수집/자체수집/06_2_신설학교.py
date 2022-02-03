import json
import time
import codecs
import requests
import random
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\06_2_신설학교\\') == False : os.makedirs('수집결과\\06_2_신설학교\\')
outfilename = '수집결과\\06_2_신설학교\\신설학교_{}.txt'.format(today)
outfilename_true = '수집결과\\06_2_신설학교\\신설학교_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\06_2_신설학교\\신설학교_{}.log_실패.txt'.format(today)
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
    outfile.write("schlNm|classCnt|ditcNm|eduOffcNm|openSchdYm|pointX|pointY|realAddr|remk\n")
    Code_list = ['B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'I10', 'J10', 'K10', 'L10', 'M10', 'N10', 'O10',
                 'P10', 'Q10', 'R10', 'S10', 'T10', ]

    for code in Code_list:
        store_list = getinfo(code)
        print(code)
        for store in store_list:
            outfile.write(u'%s|' % store['schlNm'])
            outfile.write(u'%s|' % store['classCnt'])
            outfile.write(u'%s|' % store['ditcNm'])
            outfile.write(u'%s|' % store['eduOffcNm'])
            outfile.write(u'%s|' % store['openSchdYm'])
            outfile.write(u'%s|' % store['pointX'])
            outfile.write(u'%s|' % store['pointY'])
            outfile.write(u'%s|' % store['realAddr'])
            outfile.write(u'%s\n' % store['remk'])
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getinfo(regionCode):
    url = 'http://eduinfo.go.kr/portal/theme/newSchInfoDetail.do'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'AJAX': 'true',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '51',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=F6FA417B90A6764235BF19DA6C5F546A',
        'Host': 'eduinfo.go.kr',
        'Origin': 'http://eduinfo.go.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://eduinfo.go.kr/portal/theme/newSchMapPage.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'schlSeq': '',
        'yymmdd': '',
        'searchRg': 'J10',
        'searchOffc': '',
        'searchWd': '',
    }
    data['searchRg'] = regionCode
    jsonData = requests.post(url,headers = headers, data = data)
    josonData = jsonData.text
    josonString = json.loads(josonData)
    entityList = josonString['result']
    print(entityList)
    data = []
    for info in entityList:
        schlNm = info['schlNm']
        classCnt = info['classCnt']
        ditcNm = info['ditcNm']
        eduOffcNm = info['eduOffcNm']
        openSchdYm = info['openSchdYm']
        pointX = info['pointX']
        pointY = info['pointY']
        realAddr = info['realAddr']
        remk = info['remk']
        data.append({'schlNm':schlNm,'classCnt':classCnt,'ditcNm':ditcNm,'eduOffcNm':eduOffcNm,'openSchdYm':openSchdYm,'pointX':pointX,'pointY':pointY,'realAddr':realAddr,'remk':remk})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()