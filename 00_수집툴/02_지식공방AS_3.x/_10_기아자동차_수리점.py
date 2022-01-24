import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('1_기아_SERVICE.txt', 'w', 'utf-8')
    outfile.write("##NAME|CLASS|BRANCH|ADDR|XCORD|YCORD|TELL|TIME|ETC\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['class'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['time'])
            outfile.write(u'%s\n' % store['etc'])
        page += 1
    outfile.close()

def getStoreInfo(pageNo):
    url = "https://red.kia.com/kr/knet/searchAsaList.do"
    data = {
        'funcobj': 'goPage_comm',
        'searchType': '',
        'searchTypeSub': '',
        'siDoCd': '',
        'siDoNm': '',
        'siGunGuCd': '',
        'siGunGuNm': '',
        'schText': '',
        'schTextType': '',
        'selectType': '',
        'asnCd': '',
        'pagesize': '10',
        'schTextTemp': '',
        'selectTypeTemp': 'all',
        'siDoCdTemp': '',
        'siGunGuCdTemp': ''
    }
    data['currpage'] = pageNo
    jsonData = requests.post(url = url , data = data)
    req = jsonData.text
    response = json.loads(req)
    list = []
    try:
        dataAll = response['searchAsaList']
    except KeyError:
        pass
    else:
        for listinfo in dataAll:
            name = '기아모터스'
            classNm = listinfo['poiClassName']
            asnCd = listinfo['asnCd']
            branch = listinfo['poiName']
            addr = listinfo['addr']
            xCord = listinfo['displayX']
            yCord = listinfo['displayY']
            tell = listinfo['telNo']
            try:
                etc = listinfo['rprTypeNm'].replace('\n','')
            except : etc= ''

            #영업시간 추가 수집
            url = 'https://red.kia.com/kr/knet/selectMainAsnHomePage.do'
            data = {
                'newJoinHmpg': 'Y',
            }
            data['asnCdHmpg'] = asnCd
            pageString = requests.post(url=url, data=data).text
            bsObj = bs4.BeautifulSoup(pageString, "html.parser")
            time = bsObj.select(
                '#content > div > div.graybox.mat10 > dl > dd > div > table > tbody > tr:nth-child(5) > td > p')
            time = str(time).replace('<p>', '').replace('</p>', '').replace('<strong class="gold">', '').replace(
                '</strong>', '').replace('<br/>', '').replace('  ', '').lstrip().rstrip()
            time = time.splitlines()
            a = time[1]
            b = time[2]
            times = a + ' / ' + b

            list.append ({"name":name, "class":classNm ,"branch":branch,"addr":addr,"xcord":xCord,"ycord":yCord,"tell":tell,'time':times,'etc':etc})
    return list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
