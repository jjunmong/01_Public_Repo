import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('35_블랙야크.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCODR|YCORD\n")

    sido_list = ['서울', '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '인천', '대전', '울산', '광주', '대구', '부산', '세종', '제주']

    for sido in sido_list:
        store_list = getStoreInfo(sido)
        print(sido)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3,0.6))

    for sido in sido_list:
        store_list = getStoreInfo_kids(sido)
        print(sido)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo(sido):
    url = 'http://member.blackyak.com/memberutil/store/store_20190411/ajax_storelist.asp'
    data = {
        'isZoom': '9',
        'isbk': '',
        'keyword': '',
        'lat': '37.561562',
        'lon': '126.977877',
        'geotype': 'N',
        # 'region': '서울',
        '_': '1611540624076',
    }
    data['region'] = sido
    pageString = requests.get(url, data = data).text
    jsonString = json.loads(pageString)
    result = []
    for info in jsonString:
        name = '블랙야크'
        branch = info['info1']
        branch = str(branch).replace('<br><span>BAC</span>','').replace('[직영점]','').replace(' ','')
        addr = info['info3']
        tell = info['info2']
        xcord = info['lng']
        ycord = info['lat']
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})
    return result


def getStoreInfo_kids(sido):
    url = 'http://member.blackyak.com/memberutil/store/store_20190411/ajax_storelist.asp'
    data = {
        'isZoom': '11',
        'isbk': 'y',
        'keyword': '',
        'lat': '37.561562',
        'lon': '126.977877',
        'geotype': 'N',
        # 'region': '서울',
        '_': '1611540624079',
    }
    data['region'] = sido
    pageString = requests.get(url, data = data).text
    jsonString = json.loads(pageString)
    result = []
    for info in jsonString:
        name = '블랙야크'
        branch = info['info1']
        branch = str(branch).replace('<br><span>BAC</span>','').replace('[직영점]','').replace(' ','')
        addr = info['info3']
        tell = info['info2']
        xcord = info['lng']
        ycord = info['lat']
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()