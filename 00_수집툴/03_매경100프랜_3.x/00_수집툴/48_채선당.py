import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('48_채선당등.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == []: break;

        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])

        page += 1

        if page == 70: break

        time.sleep(random.uniform(0.6, 0.9))

def getStoreInfo(pageNo):
    url = 'https://www.chaesundang.co.kr/sub/03/sub_1.asp'
    data= {
        # 'page': '2',
        'code1': '',
        'code2': '',
        's_word': '',
    }
    data['page'] = pageNo
    pageString = requests.get(url, params=data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url, pageNo)
    li = bsObj.find('tbody')
    tr = li.find_all('tr')
    result = []
    for info in tr:
        try :
            name = info.select('a')[0].text
            branch = info.select('a')[1].text
            addr = info.select('a')[2].text
            tell = info.select('td')[2].text.replace(')','-')
        except :
            pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
