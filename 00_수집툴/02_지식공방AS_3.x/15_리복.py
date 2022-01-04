import requests
import bs4
import json
import codecs
import re

outfile=codecs.open('15_Reebok.txt', 'w', 'utf-8')
outfile.write("NAME|BRANCH|OLD_ADDR|NEW_ADDR|TELL\n")

def getinfo(intPageno):
        json_url = "https://shop.reebok.co.kr/RPF110101.action"
        data = {
            'command': 'LIST_2',
            'gubn': 'first',
            'paramGubn': '',
            'STORE_NM_PRE': '',
            'STORE_ID': '',
            'SIDO_NM': '전체',
            'GUN_NM': '전체',
            'BRAND': '2',
            'STORE_DIVI': '',
            'STORE_DIVI_NM': '',
            'PAGE_LEN': '',
            'CLUB_YN': 'N',
            'REE_DIRECT_YN': 'N',
            'REE_NODIRECT_YN': 'N',
            'CPON_ID': '',
            'EVENT_ID': '',
            'STORE_NM': ''
        }
        data['PAGE_CUR'] = intPageno
        json_string = requests.post(json_url, data=data)
        json_string.encoding = 'utf-8'
        html = json_string.text
        data_list = json.loads(html)
        entity_list = data_list['storeList2']['list']
        print(entity_list)
        store_list = []
        for i in entity_list:
            name = "리복"
            branch = i['STORE_NM'].rstrip().lstrip().upper()
            old_addr1 = i['ADDR'].rstrip().lstrip()
            old_addr2 = i['DTL_ADDR'].rstrip().lstrip()
            old_addr = old_addr1 +" "+ old_addr2
            new_addr = i['DORO_ADDR'].rstrip().lstrip()
            tell = i['TEL_NO'].rstrip().lstrip()
            store_list.append({"name": name, "branch": branch, "old_addr": old_addr,"new_addr":new_addr, "tell": tell})
        return store_list

result = []
for lists in range(0,30):
    result = result + getinfo(lists)

results = set()
new_results = []
for list in result:
    lists = tuple(list.items())
    if lists not in results:
        results.add(lists)
        new_results.append(list)

for ss in new_results:
    print(ss)

for result_list in new_results:
    outfile.write(u'%s|' % result_list['name'])
    outfile.write(u'%s|' % result_list['branch'])
    outfile.write(u'%s|' % result_list['old_addr'])
    outfile.write(u'%s|' % result_list['new_addr'])
    outfile.write(u'%s|\n' % result_list['tell'])
outfile.close()
