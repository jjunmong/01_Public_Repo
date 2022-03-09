import sys
import codecs
import requests
import bs4
import json

def main():

    outfile = codecs.open('40_크린에이드.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True :
        store_list = getStoreInfo(page)
        if getStoreInfo(page) == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.clean-aid.co.kr/useinfo/ajax.store.php'
    data = {
        'md': 'search',
        'bs': '',
        # 'pg': '2',
        'ar1': '',
        'ar2': '',
        'sf': 'all',
        'area1': '',
        'area2': '',
        'ss': '',
    }
    data['pg'] = intPageNo
    pageString = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    print(url,intPageNo)
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '크린에이드'
            branch = info.find('th').text
            addr = info.find('div',{"class":"adrs"}).text.replace('\xa0','')
            tell = info.find('div',{"class":"call"}).text
        except : pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

