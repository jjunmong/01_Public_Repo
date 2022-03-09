import sys
import codecs
import requests
import bs4
import json

def main():

    outfile = codecs.open('39_홍대쌀국수.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list==[] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s\n' % store['addr'])

        page +=1

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.hongdaefood.com/board/lists/franchise/page/{}'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    print(url, intPageNo)
    table = bsObj.find('table')
    tr = table.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '홍대쌀국수'
            branch = info.find('a').text.replace(' ','').lstrip().rstrip()
            addr = info.find('td',{"style":"text-align: left;"}).text
        except:
            pass
        else:
            result.append({"name": name, "branch": branch, "addr": addr})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
