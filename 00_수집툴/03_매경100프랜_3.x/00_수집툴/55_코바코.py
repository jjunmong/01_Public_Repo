import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('55_코바코.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|OFFDAY|XCORD|YCORD\n")

    urlList = getUrlList()
    for url in urlList :
        store_list = getStoreInfo(url)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['offday'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.9, 0.9))
    outfile.close()

def getUrl(pageNo):
    url = 'http://www.cobaco.com/store01.html'
    params = {
        'category': 'shop',
        'code': 'cobaco_shop',
        # 'page': '2',
        'keyfield': '',
        'key': '',
        'sido': '',
        'gugun': '',
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
            url2 = url.find('button')['onclick']
            url2 = str(url2).replace("fnStoreView('","").replace("');","")
            url = 'http://www.cobaco.com/layer02.html?uid=' + url2
        except :
            pass
        else:
            data.append(url)
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
    name = "코바코"
    branch = bsObj.select('#content > div > div:nth-child(2) > table > tbody > tr:nth-child(4) > td:nth-child(2)')
    branch = str(branch).replace('[','').replace(']','').replace('<td>', '').replace('</td>', '')
    addr = bsObj.select('#content > div > div:nth-child(2) > table > tbody > tr:nth-child(5) > td:nth-child(2)')
    addr = str(addr).replace('[', '').replace(']', '').replace('<td>', '').replace('</td>', '').replace('<td colspan="3">','').replace('  ',' ')
    tell = bsObj.select('#content > div > div:nth-child(2) > table > tbody > tr:nth-child(4) > td:nth-child(4)')
    tell = str(tell).replace('[', '').replace(']', '').replace('<td>', '').replace('</td>', '')
    offday = bsObj.select('#subContents > div > div.sub-contents-box > div.board-box.store-detail-info > table > tbody > tr:nth-child(3) > td')
    offday = str(offday).replace('[', '').replace(']', '').replace('<td>', '').replace('</td>', '')
    cord = bsObj.select('script')
    cord = str(cord).split("center: new kakao.maps.LatLng(")
    cord = str(cord[1]).split(',')
    xcord = str(cord[1]).replace(')','').lstrip().rstrip()
    ycord = cord[0].lstrip().rstrip()
    result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"offday":offday,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
