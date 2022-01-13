import time
import requests
import random
import json
import codecs
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\11_5_유치원알리미\\') == False : os.makedirs('수집결과\\11_5_유치원알리미\\')
outfilename = '수집결과\\11_5_유치원알리미\\유치원알리미_{}.txt'.format(today)
outfilename_true = '수집결과\\11_5_유치원알리미\\유치원알리미_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\11_5_유치원알리미\\유치원알리미_{}.log_실패.txt'.format(today)

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
    outfile.write("key|officeedu|subofficeedu|kindername|establish|edate|odate|addr|telno|hpaddr|opertime|clcnt3|clcnt4|"
                  "clcnt5|mixclcnt|shclcnt|ppcnt3|ppcnt4|ppcnt5|mixppcnt|shppcnt\n")
    url_list = getUrl()

    for url in url_list:
        store_list = getStoreInfo(url)
        print(store_list)
        for store in store_list:
            outfile.write(u'%s|' % store['key'])
            outfile.write(u'%s|' % store['officeedu'])
            outfile.write(u'%s|' % store['subofficeedu'])
            outfile.write(u'%s|' % store['kindername'])
            outfile.write(u'%s|' % store['establish'])
            outfile.write(u'%s|' % store['edate'])
            outfile.write(u'%s|' % store['odate'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['telno'])
            outfile.write(u'%s|' % store['hpaddr'])
            outfile.write(u'%s|' % store['opertime'])
            outfile.write(u'%s|' % store['clcnt3'])
            outfile.write(u'%s|' % store['clcnt4'])
            outfile.write(u'%s|' % store['clcnt5'])
            outfile.write(u'%s|' % store['mixclcnt'])
            outfile.write(u'%s|' % store['shclcnt'])
            outfile.write(u'%s|' % store['ppcnt3'])
            outfile.write(u'%s|' % store['ppcnt4'])
            outfile.write(u'%s|' % store['ppcnt5'])
            outfile.write(u'%s|' % store['mixppcnt'])
            outfile.write(u'%s\n' % store['shppcnt'])

        time.sleep(random.uniform(0.9, 0.8))

    outfile.close()
def getUrl():
    with open('유치원알리미_URL.txt') as data:
        lines = data.read().splitlines()
    url_list = lines
    return  url_list

def getStoreInfo(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    pageinfo = requests.get(url, headers = headers).text
    time.sleep(0.2)
    print(url)
    data = json.loads(pageinfo)
    list = data['kinderInfo']
    data = []
    for info in list:
        key = info['key']
        officeedu = info['officeedu']
        subofficeedu = info['subofficeedu']
        kindername = info['kindername']
        establish = info['establish']
        edate = info['edate']
        odate = info['odate']
        addr = info['addr']
        telno = info['telno']
        hpaddr = info['hpaddr']
        opertime = info['opertime']
        clcnt3 = info['clcnt3']
        clcnt4 = info['clcnt4']
        clcnt5 = info['clcnt5']
        mixclcnt = info['mixclcnt']
        shclcnt = info['shclcnt']
        ppcnt3 = info['ppcnt3']
        ppcnt4 = info['ppcnt4']
        ppcnt5 = info['ppcnt5']
        mixppcnt = info['mixppcnt']
        shppcnt = info['shppcnt']
        data.append({"key":key,"officeedu":officeedu,"subofficeedu":subofficeedu,"kindername":kindername,"establish":establish
                     ,"edate":edate,"odate":odate,"addr":addr,"telno":telno,"hpaddr":hpaddr,"opertime":opertime,"clcnt3":clcnt3
                     ,"clcnt4":clcnt4,"clcnt5":clcnt5,"mixclcnt":mixclcnt,"shclcnt":shclcnt,"ppcnt3":ppcnt3,"ppcnt4":ppcnt4
                     ,"ppcnt5":ppcnt5,"mixppcnt":mixppcnt,"shppcnt":shppcnt})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()