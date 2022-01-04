import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('130_에이스침대.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XOCRD|YCORD")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo(intPageNo):
    url = 'http://m.acebed.com/contents/shop/action/shop_list_more_action.asp'
    data = {
        'ACT': '',
        'cbxAREA1_CD': '',
        'cbxAREA2_CD': '',
        'txtSRM_FRM_CD': '',
        'cbxHNDL_BRD_CD': '',
        'search_EXPRN_ZONE': '',
        'cbxSearch_Type': 'SRM_NM',
        'txtSearch_Word': '',
        # 'txtPage': '6',
        'txtPage_View': '1',
        'txtLastPage': '25',
        'txtAREA1_CD': '',
        'txtAREA2_CD': '',
        'txtHNDL_BRD_CD': '',
        'txtOSRM_FRM_CD': '',
        'cbxSearch_Type': '',
        'blank': '',
    }
    data['txtPage'] = intPageNo
    pageString = requests.post(url, data = data).text
    pageString = pageString.replace(' 				','')
    jsonString = json.loads(pageString)
    entityList = jsonString['DATA_LIST']
    result = []
    for info in entityList:
        try:
            name = '에이스침대'
            branch = str(info['SRM_NM']).replace('ACE','').replace(' ','')
            addr = info['NEW_BSE_ADR']
            tell = info['PHN_N']
            xcord = info['CDT_X']
            ycord = info['CDT_Y']
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()