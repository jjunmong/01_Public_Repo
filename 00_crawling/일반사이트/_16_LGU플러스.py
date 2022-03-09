import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('16_LGU플러스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|NEWADDR|OLDADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['oldaddr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 5

    outfile.close()

def getStoreInfo(intpageNo):
    url = 'http://www.uplus.co.kr/css/sinf/brsc/RetrievePosPageSearch.hpi'
    data = {
        'targetRow': '',
        'sido': '',
        'sigungu': '',
        'dongnm': '',
        'dongInput': '',
        'roadviewyn': '',
        # 'devonTargetRow': '6',
        'devonOrderBy': '',
    }
    data['devonTargetRow'] = intpageNo
    pageString = requests.post(url, data = data).text
    print(url , data)
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    ul = bsObj.find('ul',{"class":"searchShopList nblist"})
    li = bsObj.select('li')
    # print(li)
    result = []
    for info in li:
        try:
            name = 'LGU플러스'
            branch = info.find('strong').text.replace('_','')
            newaddr = info.select('p')[0]
            newaddr = str(newaddr).replace('<p id="roadview0" style="display: block">','').replace('</p>','').replace('<p id="roadview1" style="display: block">','').replace('<p id="roadview2" style="display: block">','').replace('<p id="roadview3" style="display: block">','').replace('<p id="roadview4" style="display: block">','')
            oldaddr = info.select('p')[1]
            oldaddr = str(oldaddr).replace('<p id="jibunview0" style="display: none">','').replace('</p>','').replace('<p id="jibunview1" style="display: none">','').replace('<p id="jibunview2" style="display: none">','').replace('<p id="jibunview3" style="display: none">','').replace('<p id="jibunview4" style="display: none">','')
            tell = info.select('p')[2]
            tell = str(tell).replace('<p>T. ','').replace('</p>','')
        except :
            pass
        else:
            result.append({"name":name,"branch":branch,"newaddr":newaddr,"oldaddr":oldaddr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
