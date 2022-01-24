import sys
import codecs
import requests
import bs4

def main():

    outfile = codecs.open('27_다비치안경.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    sido_list = ['경기','강원','제주','경상남도','경상북도','전라남도','전라북도','충청남도','충청북도','서울특별시','인천광역시','대전광역시','광주광역시','울산광역시','부산광역시','대구광역시','세종특별자치시']


    for sido in sido_list:
        page = 1
        while True:
            store_list = getStoreInfo(sido, page)
            if store_list ==[] : break
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['tell'])

            page +=1

    outfile.close()


def getStoreInfo(sidoList, intPageNo):
    url = "https://www.davich.com/04_market/01_find.php"
    data = {
        # 'pg': '2',
        # 'sido': '경기',
        'gugun': '',
    }
    data['pg'] = intPageNo
    data['sido'] = sidoList
    pageString = requests.get(url, params = data)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    print(url, sidoList, intPageNo)
    result = []
    li = bsObj.find_all('li',{"class":"pay_left_s"})
    for info in li:
        try:
            name = '다비치안경'
            branch = info.find('td',{"width":"*"}).text
            addr = info.select('a')[2]
            addr = str(addr).split("'")
            addr = str(addr[1]).lstrip().rstrip()
            tell = info.find('td',{"width":"150"}).text
        except: pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
