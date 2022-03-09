import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('17_씨스페이스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s\n' % store['addr'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intpageNo):
    url = 'http://cspace.co.kr/bbs/board.php?bo_table=location&page={}'.format(intpageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=81q5v1j33ev9iu9objm0jf3p65; 2a0d2363701f23f8a75028924a3af643=MTEyLjE2OS4zMy42Nw%3D%3D; ck_font_resize_rmv_class=; ck_font_resize_add_class=; mi_log_vi=EIAQM6QDQ3z4KJIQM7IEX11y; e1192aefb64683cc97abb83c71057733=bG9jYXRpb24%3D; mi_log_c=2020-04-20%2017%3A41%3A47',
        'Host': 'cspace.co.kr',
        'Referer': 'http://cspace.co.kr/bbs/board.php?bo_table=location',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    print(url, intpageNo)
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '씨스페이스'
            infos = info.select('a')
            infos = str(infos).split(',')
            branch = infos[0]
            branch = str(branch).replace('[<a class="select_spot">','').replace('</a>','').replace(' ','')
            addr = infos[1]
            addr = str(addr).replace('<a class="select_spot">','').replace('</a>]','')
        except :
            pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
