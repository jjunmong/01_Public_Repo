import sys
import time
import codecs
import requests
import random
import json
import bs4

# sido_list = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시', '광주광역시', '대구광역시', '부산광역시', '세종특별자치시', '제주특별자치도']

def main():

    outfile = codecs.open('13_SKY서비스센터.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s\n' % store['addr'])

    outfile.close()

def getStoreInfo():
    url = 'http://shop1.skyxgood.cafe24.com/front/php/b/board_list.php?board_no=5&is_pcver=T'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'cuk_ubp=CUK_8274B71D2_1579236398; _ga=GA1.2.1044662437.1581474233; _hjid=b25ba6f3-08e8-463d-96e3-27efe64026f1; CUK45=cuk45_skyxgood_08c0c16d79da4d49adeaad91199dcbb0; CUK2Y=cuk2y_skyxgood_08c0c16d79da4d49adeaad91199dcbb0; ECSESSID=388dd0b66b451eb350f2b0a42e2771fe; is_pcver=T; is_mobile_force=F; EC_MOBILE_DEVICE=1; basketcount_1=0; atl_epcheck=1; atl_option=1%2C1%2CH; CID=CID89c6477ae781b2bc1c00b42c1c0a470d; CID89c6477ae781b2bc1c00b42c1c0a470d=dd444e2dbc5182804b7f782502ff383d%3A%3A%3A%3A%3A%3Ahttp%3A%2F%2Fisky.co.kr%2F%3A%3A%3A%3A4%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%2Ffront%2Fphp%2Fb%2Fboard_list.php%3Fboard_no%3D5%26is_pcver%3DT%3A%3A1586762475%3A%3A%3A%3Appdp%3A%3A1586762475%3A%3A%3A%3A%3A%3A%3A%3A; EC_BR=13; vt=1586762512',
        'Host': 'shop1.skyxgood.cafe24.com',
        'Referer': 'http://shop1.skyxgood.cafe24.com/front/php/b/board_list.php?board_no=1002&is_pcver=T',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr',{"class":"xans-record-"})
    result = []
    for info in tr:
        name = 'SKY서비스센터'
        branch = info.select('td')[1]
        branch = str(branch).replace('<td class="">','').replace('</td>','')
        addr = info.find('td',{"class":"subject left txtBreak"}).text.replace('\n','').rstrip().lstrip()
        result.append({"name":name,"branch":branch,"addr":addr})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
