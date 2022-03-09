import sys
import time
import codecs
import requests
import random
import json
import bs4
import urllib.parse

def main():

    outfile = codecs.open('38_광주은행.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    code_list = getStore_code()
    for code in code_list:
        store_list = getStoreInfo(code)
        print(code)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s\n' % store['tell'])
        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStore_code():
    url = 'https://www.kjbank.com/ib20/act/BHPBKIF010402A10?ib20_cur_mnu=BHPBKIF010402&ib20_cur_wgt=BHPBKIF010402V10'
    data = {
        'INBN_BRN_DVCD': '1',
        'INSL_AREA_DVCD': '',
        'INSL_BRN_NM': '',
        'CHECK_TRAN_KEY': '20210127145707129',
        'action_type': 'act',
        'ib20_cur_mnu': 'BHPBKIF010402',
        'ib20_cur_wgt': 'BHPBKIF010402V10',
        'PROCS_DIV_S1': '1',
        'b_page_id': '',
    }
    pageString = requests.post(url, data = data).text
    pageString = urllib.parse.unquote(pageString)
    jsonString = json.loads(pageString)
    entityList = jsonString['_msg_']['_body_']['GRID00']
    result = []
    for info in entityList:
        code = info['INSL_BRCD']
        result.append(code)
    return result

def getStoreInfo(code):
    url = 'https://www.kjbank.com/ib20/act/BHPBKIF010402A10?ib20_cur_mnu=BHPBKIF010402&ib20_cur_wgt=BHPBKIF010402V10'
    data = {
        'INBN_BRN_DVCD': '1',
        'INSL_AREA_DVCD': '',
        'INSL_BRN_NM': '',
        'CHECK_TRAN_KEY': '20210127145707129',
        'action_type': 'act',
        'ib20_cur_mnu': 'BHPBKIF010402',
        'ib20_cur_wgt': 'BHPBKIF010402V10',
        'PROCS_DIV_S1': '2',
        # 'INSL_BRCD': '',
    }
    data['INSL_BRCD'] = code
    pageString = requests.post(url, data = data).text
    pageString = urllib.parse.unquote(pageString)
    jsonString = json.loads(pageString)
    entityList = jsonString['_msg_']['_body_']
    result = []
    name = '광주은행'
    branch = str(entityList['INSL_BRN_NM']).replace('+',' ')
    addr = str(entityList['INSL_BRN_ADDR']).replace('+',' ')
    tell = entityList['INSL_BRN_TLNO']
    xcord = str(entityList['INSL_BRN_LOTDE_VAL'])
    xcord = xcord[:3] +'.'+xcord[3:]
    ycord = str(entityList['INSL_BRN_LATDE_VAL'])
    ycord = ycord[:2] +'.'+ycord[2:]
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()