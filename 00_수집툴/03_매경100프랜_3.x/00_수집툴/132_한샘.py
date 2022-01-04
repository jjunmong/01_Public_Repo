import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('132_한샘.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XOCRD|YCORD\n")

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
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')
def getStoreInfo(intPageNo):
    url = 'https://www.hanssem.com/shop/shopListWebAjax.do'
    data = {
        'sidoCd': '',
        'sggCd': '',
        # 'curPage': '2',
        'orderCd': 'P',
        'latitude': '',
        'longitude': '',
        'devisionCd': 'ALL',
        'countChangeYN': 'N',
        'shopSearchType': 'shopAddr',
        'shopSearchText': '',
    }
    data['curPage'] = intPageNo
    pageString = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('li')
    result = []
    for info in li:
        try:
            name = '한샘'
            branch = info.find('h4').text
            addr = info.find('p',{"class":"str_address"}).text
            tell = ''
            xcord = info.find('input',{"id":"longitude"})['value']
            ycord = info.find('input',{"id":"latitude"})['value']
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()