import time
import codecs
import requests
import json
import random
import sys

def main():

    outfile = codecs.open('54_미스터피자.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|OLDADDR|NEWADDR|TELL\n")

    id_list = getStore_id_list()
    for id in id_list:
        result = getStoreInfo(id)
        print(id)
        for results in result:
            outfile.write(u'%s|' % results['name'])
            outfile.write(u'%s|' % results['branch'])
            outfile.write(u'%s|' % results['oldaddr'])
            outfile.write(u'%s|' % results['newaddr'])
            outfile.write(u'%s\n' % results['tell'])
        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStore_id(sido):
    url = "https://www.mrpizza.co.kr/store/getGugunBranchList.json"
    data = {
        # 'si': '서울특별시',
        'gu': '',
    }
    data['si'] = sido
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    result = []
    for info in jsonString:
        branch_id = info['branch_id']
        result.append(branch_id)
    return result

def getStore_id_list():
    sido_list = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시',
                 '광주광역시', '대구광역시', '부산광역시', '세종특별자치시', '제주특별자치도']
    result = []
    for sido in sido_list:
        result = result + getStore_id(sido)
        print(sido)

    return result

def getStoreInfo(branch_id):
    url = "https://www.mrpizza.co.kr/store/findStoreInfo.json"
    data = {}
    data['branch_id'] = branch_id
    pageString = requests.post(url, data = data).text
    jsonString = json.loads(pageString)
    result = []
    for info in jsonString:
        name = '미스터피자'
        branch = info['branch_nm']
        try:
            oldaddr = info['si'] + ' ' + info['gu'] + ' ' + info['dong'] + ' ' + info['bunji']
        except :
            oldaddr = ''
        try:
            newaddr = info['addr_doro']
        except :
            newaddr = ''
        tell = info['branch_tel1']
        result.append({'name':name,'branch':branch,'oldaddr':oldaddr,'newaddr':newaddr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()