import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('128_시몬스침대.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|CORDX|CORDY\n")

    page = 0
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['cordx'])
            outfile.write(u'%s|' % store['cordy'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo(intPageNo):
    url = 'http://www.simmons.co.kr/api/store/selectAgencyAction'
    data = {
        # 'rownum': '1',
        'area_gb':'',
        'agency_nm':'',
    }
    data['rownum'] = intPageNo
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    result = []
    for info in jsonString:
        try:
            name = '시몬스'
            branch = str(info['agency_nm']).replace('시몬스 ','')
            addr = info['doro_addr']
            tell = info['tel']
            cordx = info['gps_y']
            cordy = info['gps_x']
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'cordx':cordx,'cordy':cordy})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()