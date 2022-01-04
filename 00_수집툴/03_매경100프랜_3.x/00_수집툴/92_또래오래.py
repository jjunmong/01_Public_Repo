import sys
import requests
import bs4
import codecs
import time
import random
import json
def main():

    outfile = codecs.open('92_또래오래.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    sido_list = ['서울', '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '인천', '대전', '울산', '광주', '대구', '부산', '세종특별자치시', '제주특별자치도']
    for sido in sido_list:
        page = 0
        while True:
            storeList = getStoreInfo(sido,page)
            if storeList == [] : break
            for store in storeList:
                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['branch'])
                    outfile.write(u'%s|' % store['addr'])
                    outfile.write(u'%s|' % store['tell'])
                    outfile.write(u'%s|' % store['xcord'])
                    outfile.write(u'%s\n' % store['ycord'])
            page +=1
            time.sleep(random.uniform(0.3, 0.9))

    outfile.close()


def getStoreInfo(sido,intPageNo):
    url = 'https://www.toreore.com/controller/ajax_shop_search_controller.html'
    data = {
        'sido': '서울',
        'actionMethod': 'search',
        'dataindex': '0',
    }
    data['sido'] = sido
    data['dataindex'] = intPageNo
    pageString = requests.post(url,data = data).text
    jsonString = json.loads(pageString)
    print(sido, intPageNo)
    entityList = jsonString['Listdata']
    result = []
    for info in entityList:
        name = '또래오래'
        branch = info['sname']
        addr = info['addr1']
        tell = info['phone1']
        xcord = info['lng']
        ycord = info['lat']
        result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()