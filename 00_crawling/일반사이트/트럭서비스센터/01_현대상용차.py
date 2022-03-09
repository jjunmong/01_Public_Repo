import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('01_현대상용차_블루핸즈.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME|XCORD|YCORD\n")

    page = 0
    while True:
        store_list = getStoreInfo(page)
        if store_list == [] : break
        print(page)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['time'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page+=5
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

    outfile = codecs.open('01_현대상용차_소상특장전담.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo2()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'https://www-trucknbus.hyundai.com/kr/service-network/selectBluehandsList'
    data = {
        # 'rnum': '15',
        'sido': '',
        'sigu': '',
        'map_ycoo_nm': '',
        'map_xcoo_nm': '',
        'cmd_cd': '',
        'cmd_nm': '',
        'spcl_cs': 'N',
        'spcl_hitech': 'N',
        'spcl_eco': 'N',
        'spcl_cnt': '0',
        'lag_truck': 'N',
        'mid_truck': 'N',
        'lag_bus': 'N',
        'mid_bus': 'N',
        'filter_cnt': '0',
        'oper_day': 'N',
        'oper_night': 'N',
        'oper_holiday': 'N',
        'time_cnt': '0',
    }
    data['rnum']=intPageNo
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    entityList = jsonString['resultData']['branchList']
    result = []
    for info in entityList:
        try:
            name = '현대자동차 상용블루핸즈'
            branch = info['asn_nm'].replace('(주)', '').replace('㈜', '').replace('(유)', '').lstrip().rstrip()
            addr = info['pbz_adr'].lstrip().rstrip()
            tell = info['repn_tn'].lstrip().rstrip()
            time = info['biz_strt_ctm'] + '~' + info['biz_fnh_ctm'].lstrip().rstrip()
            xcord = info['lng'].lstrip().rstrip()
            ycord = info['lat'].lstrip().rstrip()
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time,'xcord':xcord,'ycord':ycord})
    return result


def getStoreInfo2():
    url = 'https://www.hyundai.com/kr/ko/e/vehicles/porter2-special/intro#afterService'
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    table = bsObj.find('table',{"class":"table-type01"})
    tr = table.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '현대상용차 소상특장전담 블루핸즈'
            branch = str(info.select('td')[0]).replace('<td>','').replace('</td>','').replace('(합)', '').replace('㈜', '').replace('(유)', '').lstrip().rstrip()
            addr = info.find('td',{"class":"text-left"}).text
            tell = str(info.select('td')[3]).replace('<td>','').replace('</td>','').lstrip().rstrip()
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

