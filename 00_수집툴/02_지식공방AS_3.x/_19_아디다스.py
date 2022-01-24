import codecs
import time
import requests
import sys
import random
import json

def main():

    outfile = codecs.open('19_아디다스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ID|CATEGORY|OLD_ADDR|NEW_ADDR|FLOOR|TELL\n")

    page = 1
    while True :
        store_list = getStores(page)
        if len(store_list) == 0:
            break

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['category'])
            outfile.write(u'%s|' % store['old_addr'])
            outfile.write(u'%s|' % store['new_addr'])
            outfile.write(u'%s|' % store['floor'])
            outfile.write(u'%s|\n' % store['tell'])

        page += 1
        if page == 99 : break

        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStores(intPageNo):
    url = "https://shop.adidas.co.kr/PF110101.action"
    data = {
        'command': 'LIST_2',
        'gubn': 'first',
        'paramGubn': '',
        'STORE_NM_PRE': '',
        'SIDO_NM': '전체',
        'BRAND': '1',
        'STORE_ID': '',
        'STORE_DIVI': '',
        'STORE_DIVI_NM': '',
        'STORE_DIVI_SUB': '',
        'STORE_DIVI_SUB_NM': '',
        'PAGE_LEN': '',
        'CLUB_YN': 'N',
        'DIRECT_YN': 'N',
        'NODIRECT_YN': 'N',
        'OUTLET_YN': 'N',
        'FIRST_CHK': 'Y',
        'CPON_ID': '',
        'EVENT_ID': '',
        'STORE_NM': '',
    }
    data['PAGE_CUR'] = intPageNo
    try :
        urlopen = requests.post(url , data = data).text
    except :
        print('Error calling the API')
        return  None
    response = json.loads(urlopen)
    print(response)
    list_all = response['storeList2']['list']
    data_all = []
    for list in list_all:
        name = "아디다스"
        branch = list['STORE_NM'].replace(' ','').rstrip().lstrip().upper()
        id = list['STORE_ID']
        category = list['STORE_DIVI_NM'].rstrip().lstrip().upper()
        old_addr = list['ADDR'].rstrip().lstrip().upper() + " " + list['DTL_ADDR'].rstrip().lstrip().upper()
        new_addr = list['DORO_ADDR'].rstrip().lstrip().upper()
        tell = list['TEL_NO'].rstrip().lstrip().upper()
        floor = list['DORO_DTL_ADDR']
        data_all.append({"name":name,"branch":branch,"id":id,"category":category,"old_addr":old_addr,"new_addr":new_addr,"floor":floor,"tell":tell})
    return data_all

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()