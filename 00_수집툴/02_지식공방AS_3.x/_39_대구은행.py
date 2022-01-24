import sys
import time
import codecs
import requests
import random
import json
import bs4
import urllib.parse

def main():

    outfile = codecs.open('39_대구은행.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo():
    url = 'https://www.dgb.co.kr/JEX_EBZ_SM_INAM_BRBAS_R001.jct'
    data = {
        '_JSON_': '%7B%22INQ_DV_CD%22%3A%221%22%2C%22SRCH_NM%22%3A%22%25%25%22%2C%22SLBR_LTT%22%3A35.8588335%2C%22SLBR_LNT%22%3A128.6160568%7D',
        'aap_v': '6c3d2f636d732f6574632f73746f5f65627a5f63687a65726f2e6a73705e703d5f4a534f4e5f3d34373465623762363931366161313835323164653537313861633835643738366666376261366132346439623864616566653737376462366238393538613631',
    }
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    entityList = jsonString['REC']
    result = []
    for info in entityList:
        name = '대구은행'
        branch = info['BRC_NM']
        addr = info['ROAD_NM_ATMT_ADDR']
        tell = info['DDD']+'-'+info['TLXCNO']+'-'+info['TLNDNO']
        xcord = info['SLBR_LNT']
        ycord = info['SLBR_LTT']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()