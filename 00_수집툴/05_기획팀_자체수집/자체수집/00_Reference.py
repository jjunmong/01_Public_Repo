import codecs
import requests
import json
from datetime import datetime
import time
import codecs
import requests
import random
import json
from datetime import datetime
import traceback
import os, sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.isfile('수집결과\\21_2_창고114\\') == False: os.makedirs('수집결과\\21_2_창고114\\')


def main():
    try:
        Crawl_run()
        outfilename = '수집결과\\21_2_창고114\\창고114_{}.log_성공.txt'.format(today)
        outfile = codecs.open(outfilename, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '정상 수집 완료'
        outfile.write(write_text)
    except:
        outfilename = '수집결과\\21_2_창고114\\창고114_{}.log_실패.txt'.format(today)
        if os.path.isfile('수집결과\\21_2_창고114\\창고114_{}.log_성공.txt'.format(today)):
            os.remove('수집결과\\21_2_창고114\\창고114_{}.log_성공.txt'.format(today))
        outfile = codecs.open(outfilename, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '수집 실패' + '|' + str(traceback.format_exc())
        outfile.write(write_text)


def Crawl_run():
    outfilename = '수집결과\\21_2_창고114\\창고114_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    dict_keys1 = getStoreInfo()[1]
    dict_keys2 = str(dict_keys1).replace('dict_keys', '').replace('[', '').replace(']', '').replace('(', '').replace(
        ')', '').replace(',', '|').replace("'", "").replace(' ', '')
    outfile.write("%s\n" % dict_keys2)

    key_list = []
    for key in dict_keys1:
        key_list.append(key)

    store_list = getStoreInfo()[0]
    for store in store_list:
        column_num = 0
        while True:
            if column_num == len(key_list):
                break
            elif column_num == len(key_list) - 1:
                outfile.write(u'%s\n' % store[u'%s' % key_list[column_num]])
            else:
                outfile.write(u'%s|' % store[u'%s' % key_list[column_num]])
            column_num += 1
    outfile.close()


def getStoreInfo():
    url = 'http://nlic.go.kr/nlic/searchWare.action?bas_ware_nm=&ser_ware_type=&gis_sido=&gis_sido_nm=%EC%8B%9C%EB%8F%84%EC%84%A0%ED%83%9D&gis_sigu=&gis_sigu_nm=%EC%8B%9C%EA%B5%B0%EA%B5%AC%EC%84%A0%ED%83%9D&ware_use=1&chk_lofa1=T&chk_lofa2=T&chk_lofa3=T&chk_port=T&chk_cust=T&chk_chem=T&chk_food=T&chk_anim=T&chk_mari=T&chk_info=T&chk_all=T&orderType=&pageNum={}&is_ajax=1'.format(
        intPageNo)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    pageString = requests.get(url, headers=headers).text
    jsonString = json.loads(pageString)
    entityList = jsonString['list']
    result = []
    dict_key = ''
    for info in entityList:
        result_dict = {}
        dict_key = result_dict.keys()
        result.append(result_dict)
    return result, dict_key


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()