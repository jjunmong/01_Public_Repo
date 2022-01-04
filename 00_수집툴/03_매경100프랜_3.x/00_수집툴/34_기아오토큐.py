import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('34_기아오토큐.txt', 'w', 'utf-8')
    outfile.write("BRANCH|SERVICENM|TELL|ADDR|XCORD|YCORD\n")

    page = 1
    while True:
        store_List = getinfo(page)
        if len(store_List) < 10 : break
        for store in store_List:
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['serviceNm'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])

        page += 1
        if page == 100: break
    time.sleep(random.uniform(0.3, 0.6))
    outfile.close()

def getinfo(intpageNo):
    url = 'http://red.kia.com/kr/knet/searchAsaList.do'
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
        # 'currpage': '1',
        'pagesize': '10',
        'schTextTemp': '',
        'selectTypeTemp': 'all',
        'siDoCdTemp': '',
        'siGunGuCdTemp': ''
    }
    data['currpage'] = intpageNo
    jsonData = requests.post(url , data = data).text
    jsonString = json.loads(jsonData)
    entityList = jsonString['searchAsaList']
    print(url, data)
    result =[]
    for infos in entityList:
        branch = infos['poiName'].replace('(주)','')
        serviceNm = infos['poiClassName']
        tell = infos['telNo']
        addr = infos['addr']
        xcord = infos['displayX']
        ycord = infos['displayY']
        result.append({"branch":branch,"serviceNm":serviceNm,"tell":tell,"addr":addr,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()