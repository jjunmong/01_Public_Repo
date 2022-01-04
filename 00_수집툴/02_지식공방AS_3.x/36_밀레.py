import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('36_밀레.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        if len(store_list) < 10 : break
        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.millet.co.kr/board/board.html'
    data = {
        'code': 'millet0615_board6',
        # 'page': '2',
        'board_cate': '',
    }
    data['page'] = intPageNo
    pageString = requests.get(url, params = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        name = '밀레'
        branch = str(info.select('div')[0]).replace('<div class="off-tb-center">','').replace('</div>','')
        addr = str(info.select('div')[3]).replace('<div class="off-tb-left">','').replace('</div>','')
        tell = str(info.select('div')[4]).replace('<div class="off-tb-center">','').replace('</div>','')
        if branch == '매장': pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()