import time
import requests
import random
import json
import codecs
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\12_1_미니스톱\\') == False : os.makedirs('수집결과\\12_1_미니스톱\\')
outfilename = '수집결과\\12_1_미니스톱\\미니스톱_{}.txt'.format(today)
outfilename_true = '수집결과\\12_1_미니스톱\\미니스톱_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\12_1_미니스톱\\미니스톱_{}.log_실패.txt'.format(today)

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
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")
    sidoCode = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    for getinfo in sidoCode:
        store_list = getStoirInfo(getinfo)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoirInfo(sidoCode):
    url = 'https://www.ministop.co.kr/MiniStopHomePage/page/querySimple.do'
    data = {
        'pageId': 'store/store',
        'sqlnum': '3',
        # 'paramInfo': '1:-1:-1:',
        'pageNum': '1',
        'sortGu': '',
        'tm': '1590633352848'
    }
    data['paramInfo']='{}:-1:-1:'.format(sidoCode)
    jsonData = requests.post(url, data = data, verify=False).text
    print(url ,data)
    jsonString = json.loads(jsonData)
    entityList = jsonString['recordList']
    result = []
    for list in entityList:
        infos = list['fields']
        infos_replace = str(infos).replace(',','|').replace("'","")
        splitCount = infos_replace.count('|')
        infos_split =infos_replace.split('|')
        name = '미니스톱'
        if splitCount == 5 :
            branch = infos_split[0].replace('[','').replace("'","").lstrip().rstrip().upper()
            addr = infos_split[1].replace("'","").lstrip().rstrip().upper()
            tell = infos_split[2].replace("'","").lstrip().rstrip().upper()
            xcord = infos_split[5].replace(']','').replace("'","").lstrip().rstrip().upper()
            ycord = infos_split[4].replace("'","").lstrip().rstrip().upper()
        elif splitCount == 6 :
            branch = infos_split[0].replace('[','').replace("'","").lstrip().rstrip().upper()
            addr = infos_split[1] + " " + infos_split[2].replace("'","").lstrip().rstrip().upper()
            tell = infos_split[3].replace("'","").lstrip().rstrip().upper()
            xcord = infos_split[6].replace(']','').replace("'","").lstrip().rstrip().upper()
            ycord = infos_split[5].replace("'","").lstrip().rstrip().upper()
        elif splitCount == 7 :
            branch = infos_split[0].replace('[','').replace("'","").lstrip().rstrip().upper()
            addr = infos_split[1] + " " + infos_split[2] + " " + infos_split[3].replace("'","").lstrip().rstrip().upper()
            tell = infos_split[4].replace("'","").lstrip().rstrip().upper()
            xcord = infos_split[7].replace(']','').replace("'","").lstrip().rstrip().upper()
            ycord = infos_split[6].replace("'","").lstrip().rstrip().upper()
        elif splitCount == 8 :
            branch = infos_split[0].replace('[','').replace("'","").lstrip().rstrip().upper()
            addr = infos_split[1] + " " + infos_split[2] + " " + infos_split[3]+ " " + infos_split[4].replace("'","").lstrip().rstrip().upper()
            tell = infos_split[5].replace("'","").lstrip().rstrip().upper()
            xcord = infos_split[8].replace(']','').replace("'","").lstrip().rstrip().upper()
            ycord = infos_split[7].replace("'","").lstrip().rstrip().upper()
        elif splitCount == 9:
            branch = infos_split[0].replace('[', '').replace("'", "").lstrip().rstrip().upper()
            addr = infos_split[1] + " " + infos_split[2] + " " + infos_split[3] + " " + infos_split[4]+ " " + infos_split[5].replace("'","").lstrip().rstrip().upper()
            tell = infos_split[6].replace("'", "").lstrip().rstrip().upper()
            xcord = infos_split[9].replace(']', '').replace("'", "").lstrip().rstrip().upper()
            ycord = infos_split[8].replace("'", "").lstrip().rstrip().upper()
        elif splitCount == 10:
            branch = infos_split[0].replace('[', '').replace("'", "").lstrip().rstrip().upper()
            addr = infos_split[1] + " " + infos_split[2] + " " + infos_split[3] + " " + infos_split[4]+ " " + infos_split[5]+ " " + infos_split[6].replace("'","").lstrip().rstrip().upper()
            tell = infos_split[7].replace("'", "").lstrip().rstrip().upper()
            xcord = infos_split[10].replace(']', '').replace("'", "").lstrip().rstrip().upper()
            ycord = infos_split[9].replace("'", "").lstrip().rstrip().upper()
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()





