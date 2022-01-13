import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('36_오피스디포.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    sidoList = ['서울특별시','경기도','경상남도','경상북도','전라남도','전라북도','충청북도','충청남도','강원도','제주특별자치도'
                ,'세종특별자치시','대전광역시','인천광역시','광주광역시','울산광역시','대구광역시','부산광역시']
    for sido in sidoList:
        store_List = getinfo(sido)
        for store in store_List:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])

    outfile.close()

def getinfo(sidoList):
    url = 'http://www.officedepot.co.kr/company/addFindStore2.do'
    data = {
        # 'mapZone': '경상남도',
        'selectCity': '',
        'selectChk': '',
        'searchGb': '2'
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '54',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'Cookie': 'ACEFCID=UID-5E54D877CBA488895CB09564; CoreID6=07240318605215826187406&ci=90383069; _ga=GA1.3.16991432'
                  '89.1582618741; _gid=GA1.3.580272657.1582618741; cmTPSet=Y; CS5B38769814839_t_uid=54161715018013159.158'
                  '2678134163; CS5B38769814839_t_if=15.0.0.0.null.null.null.0; wcs_bt=s_1fd6ad1455:1582678155; CS5B387'
                  '69814839_t_sst=54161677000001131.1582678154402; JSESSIONID=cbf13faf-3cbe-4f39-ae90-562adc66d3fe; 903'
                  '83069_clogin=l=48885051582678135144&v=1&e=1582680622886',
        'Host': 'www.officedepot.co.kr',
        'Origin': 'http://www.officedepot.co.kr',
        'Referer': 'http://www.officedepot.co.kr/company/findStoreTmp.do',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data['mapZone'] = sidoList
    jsonData = requests.post(url, data=data, headers = headers).text
    print(url, data)
    jsonString = json.loads(jsonData)
    entityList = jsonString['storeList']
    result = []
    for infos in entityList:
        name = "오피스디포"
        branch = infos['storeNm'].replace("오피스디포 ","")
        addr = infos['bizAddr1']
        tell = infos['bizTelNo']
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()