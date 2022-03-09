import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('13_한국쓰리축.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    sido_list = ['서울', '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '인천', '대전', '울산', '광주', '대구', '부산', '세종', '제주']
    for sido in sido_list:
        store_list = getStoreInfo(sido)
        print(sido)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(sido):
    url = 'http://www.koreatriaxle.com/'
    data = {
        'controller': 'Location',
        'action': 'Service',
        # 'SIDO': '인천',
    }
    data['SIDO'] = sido
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ASPSESSIONIDACCACBDQ=LPAFOMFCOKFDBEGDKDKGKBGB',
        'Host': 'www.koreatriaxle.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.koreatriaxle.com/?controller=Location&action=Service&SIDO=%EC%A0%9C%EC%A3%BC',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    }
    pageString = requests.get(url,params = data, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('li')

    result = []
    for info in li :
        try:
            name = '한국쓰리축'
            branch = info.find('strong').text
            infos = str(info.find('address')).replace('\r','').replace('\n','').replace('\t','').replace('<address>','').replace('</address>','').split('<br/>')
            addr = infos[1]
            tell = infos[2]
            if len(addr) < 14 :
                addr = infos[0]
                tell = infos[1]
        except:
            try:
                name = '한국쓰리축'
                branch = info.find('strong').text
                infos = str(info.find('address')).replace('\r','').replace('\n','').replace('\t','').replace('<address>','').replace('</address>','').split('<br/>')
                addr = infos[0]
                tell = infos[1]
                result.append({'name': name, 'branch': branch, 'addr': addr, 'tell': tell})
            except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

