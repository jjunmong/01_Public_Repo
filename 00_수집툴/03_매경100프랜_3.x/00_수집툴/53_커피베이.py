import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('53_커피베이.txt', 'w', 'utf-8')
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
    url = 'http://www.coffeebay.com/home/store/store_area'
    params = {
        'sido': '',
        'gugun': '',
        'sc_column': '',
        'sc_string': '',
        'svc_wifi_at': '',
        'svc_catering_at': '',
        'svc_event_at': '',
        'svc_24hr_at': '',
        'svc_smok_at': '',
        'svc_park_at': '',
        'svc_kidsrm_at': '',
        'svc_bookrm_at': '',
        'svc_pwdrrm_at': '',
        'svc_meetrm_at': '',
        'svc_bizrm_at': '',
        # 'per_page': 20
    }
    params['per_page'] = pageNo
    pageString = requests.get(url, params = params)
    print(url, pageNo)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    table = bsObj.find('table',{"class":"tbl-board list address-list"})
    tr = table.find_all('tr')
    data = []
    for url in tr:
        try:
            url2 = url.find('a')['href']
            url = 'http://www.coffeebay.com' + url2
        except :
            pass
        else:
            data.append(url)
    return data

def getUrlList():
    result = []
    for store in range(0, 1500, 20):
        result = result + getUrl(store)
        if getUrl(store) == [] : break
    return result

def getStoreInfo(url):
    url = url
    pageString = requests.get(url)
    print(url)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    result = []
    name = "커피베이"
    branch = bsObj.select('#subContents > div > div.sub-contents-box > h3')
    branch = str(branch).replace('[','').replace(']','').replace('<h3 class="store-detail-info-title">','').replace('</h3>','')
    addr = bsObj.select('#subContents > div > div.sub-contents-box > div.board-box.store-detail-info > table > tbody > tr:nth-child(1) > td')
    addr = str(addr).replace('[', '').replace(']', '').replace('<td>', '').replace('</td>', '')
    tell = bsObj.select('#subContents > div > div.sub-contents-box > div.board-box.store-detail-info > table > tbody > tr:nth-child(2) > td')
    tell = str(tell).replace('[', '').replace(']', '').replace('<td>', '').replace('</td>', '')
    time = bsObj.select('#subContents > div > div.sub-contents-box > div.board-box.store-detail-info > table > tbody > tr:nth-child(3) > td')
    time = str(time).replace('[', '').replace(']', '').replace('<td>', '').replace('</td>', '')
    ycord = bsObj.select('#lat_val')
    ycord = str(ycord).replace('[<input id="lat_val" type="hidden" value="','').replace('"/>]','')
    xcord = bsObj.select('#lng_val')
    xcord = str(xcord).replace('[<input id="lng_val" type="hidden" value="', '').replace('"/>]', '')
    if time == ' ~ ' : time = ''
    else : time = time
    result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time,"xcord":xcord,"ycord":ycord})
    return result
def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
