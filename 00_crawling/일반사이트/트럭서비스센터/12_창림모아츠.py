import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('12_창림모아츠.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list == [] : break
        print(page)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page+=1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.changrim.net/bbs/board.php?bo_table=05_02&page={}'.format(intPageNo)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=gufgg0429reg4tk71lq8j1brk1; 2a0d2363701f23f8a75028924a3af643=MTEyLjE2OS4zMy42Nw%3D%3D; ck_font_resize_rmv_class=; ck_font_resize_add_class=; e1192aefb64683cc97abb83c71057733=MDVfMDI%3D','Host': 'www.changrim.net',
        'Pragma': 'no-cache',
        'Referer': 'http://www.changrim.net/bbs/board.php?bo_table=05_02',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr :
        try:
            name = '창림모아츠'
            branch = info.find('td',{"style":"border-bottom:1px solid #ddd;line-height:1.8em;text-align:center;"}).text.replace('\n','').replace('(주)','').lstrip().rstrip()
            addr = info.find('span',{"style":"font-size: 14pt;"}).text.lstrip().rstrip()
            tell = str(info.select('td')[4]).replace('<td style="border-bottom:1px solid #ddd;font-size:12pt;text-align:center;">','').replace('</td>','')
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})

    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

