import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('01_미래에셋대우.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list ==[] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page += 1
        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo(page):
    url = 'https://www.miraeassetdaewoo.com/mw/mki/mki3096/a01.json'
    data = {
        'searchText': '',
        'divNo': '',
        # 'currentPage': '1',
    }
    data['currentPage'] = page
    pageString = requests.post(url , data = data).text
    print(page)
    jsonString = json.loads(pageString)
    entityList  = jsonString['branchList']
    result =[]
    for info in entityList:
        name = '미래에셋대우'
        branch = info['BR_NM'].replace(' (사전 예약제 운영)','')
        addr = info['ADDR']
        tell = info['BBR_TEL_NO']
        xcord = info['LOCT_LONGITUDE']
        ycord =info['LOCT_LATITUDE']
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()