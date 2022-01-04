import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('56_쿠우쿠우.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME|XCORD|YCORD\n")

    urlList = getUrlList()
    for url in urlList :
        store_list = getStoreInfo(url)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['time'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.9, 0.9))
    outfile.close()

def getUrl(pageNo):
    url = 'http://www.qooqoo.co.kr/bbs/board.php'
    params = {
        'bo_table': 'storeship',
    }
    params['page'] = pageNo
    pageString = requests.get(url, params = params)
    print(url, pageNo)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    data = []
    for url in tr:
        try:
            url2 = url.select('a')[2]['href']
        except :
            pass
        else:
            data.append(url2)
    return data

def getUrlList():
    result = []
    page = 1
    while True:
        result = result + getUrl(page)
        if getUrl(page) == []: break
        page += 1
        if page == 30:
            break
    results = list(set(result))
    return results

def getStoreInfo(url):
    url = url
    pageString = requests.get(url)
    print(url)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    result = []
    name = "쿠우쿠우"
    branch = bsObj.select('body > div.wrapper > div > div.basic-body.container > div > div.basic-body-main.right-main.col-md-12 > div.sub-conW > article > section:nth-child(1) > ul > li > h4 > strong')
    branch = str(branch).replace('<strong>','').replace('</strong>','').replace('[','').replace(']','').lstrip().rstrip()
    addr = bsObj.select('body > div.wrapper > div > div.basic-body.container > div > div.basic-body-main.right-main.col-md-12 > div.sub-conW > article > section:nth-child(3) > ul > li')
    addr = str(addr).replace('<li>\n매장주소\xa0:\xa0', '').replace('</li>', '').replace('[','').replace(']','').lstrip().rstrip()
    tell = bsObj.select('body > div.wrapper > div > div.basic-body.container > div > div.basic-body-main.right-main.col-md-12 > div.sub-conW > article > section:nth-child(2) > ul > li')
    tell = str(tell).replace('<li>\n연락처\xa0:\xa0', '').replace('</li>', '').replace('[','').replace(']','').lstrip().rstrip()
    time = bsObj.select('body > div.wrapper > div > div.basic-body.container > div > div.basic-body-main.right-main.col-md-12 > div.sub-conW > article > section:nth-child(4) > ul > li')
    time = str(time).replace('<li>\n영업시간\xa0:\xa0', '').replace('</li>', '').replace('[','').replace(']','').lstrip().rstrip()
    cord = bsObj.select('meta')[9]['content']
    cord = str(cord).split('|')[3]
    cord = str(cord).replace(')}\xa0','').replace('^(','')
    cord = str(cord).split(',')
    ycord = cord[0].lstrip().rstrip()
    xcord = cord[1].lstrip().rstrip()

    result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time,"xcord":xcord,"ycord":ycord})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
