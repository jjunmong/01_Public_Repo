import bs4
import time
import codecs
import requests
import random
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\03_2_SK엔크린\\') == False : os.makedirs('수집결과\\03_2_SK엔크린\\')
outfilename = '수집결과\\03_2_SK엔크린\\SK엔크린_{}.txt'.format(today)
outfilename_true = '수집결과\\03_2_SK엔크린\\SK엔크린_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\03_2_SK엔크린\\SK엔크린_{}.log_실패.txt'.format(today)

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
    outfile.write("NAME|BRANCH|ADDR|TELL|CODE|XOCRD|YCORD|TRUCK\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['code'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s\n' % store['truck'])
        page += 1
        time.sleep(random.uniform(2,3))

    outfile.close()
    print('수집종료')

def getStoreInfo(intPageNo):
    url = 'https://www.enclean.com/front/fuel/findStationList?page={}&all=&provinceList=&oil=&stationType=all&speedmate=&wash=&self=&netplus=1&stationName=&cityList=&solux=&store='.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHAROSVISITOR=00004c9c0174ae095b9940ca0a5a0161; XTVID=Z202092192122970521; JSESSIONID=Ideo7xkek3G1oUtSOWuDphM6HkO5srP2tvSf3ruirhkqw9PJVNM319JiESTVyofi.ZWNsX2RvbWFpbi9FbmNTZXJ2ZXIyYg==',
        'Host': 'www.enclean.com',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    }
    pageString = requests.get(url , headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            name = 'SK엔크린'
            branch = info.find('span',{"class":"st"}).text
            addr = info.find('td',{"class":"td_addr"}).text
            tell = str(info.select('td')[3]).replace('<td>','').replace('</td>','')
            truck = '내트럭플러스'
            code = str(info.select('a')).split("'")[1]
            url = 'https://www.enclean.com/front/fuel/viewTmapPop?stationId='+code
            pageString = requests.get(url).text
            bsObj = bs4.BeautifulSoup(pageString, "html.parser")
            script = str(bsObj.find_all('script')).split("'")
            xcord = script[1]
            ycord = script[3]
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'code':code,'xcord':xcord,'ycord':ycord,'truck':truck})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()