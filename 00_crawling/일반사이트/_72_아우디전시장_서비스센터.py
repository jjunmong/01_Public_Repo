import sys
import time
import requests
import random
import codecs
import bs4
import json
sido_list = ['서울', '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '인천', '대전', '울산', '광주', '대구', '부산', '세종', '제주']
def main():

    outfile = codecs.open('72_아우디서비스센터.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    url_list = getStore_list()

    for url in url_list:
        store_list = getStoreInfo(url)
        print(url)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

    outfile = codecs.open('72_아우디전시장.txt', 'w', 'utf-8')
    dict_keys1 = getStoreInfoDealer('서울')[1]
    dict_keys2 = str(dict_keys1).replace('dict_keys', '').replace('[', '').replace(']', '').replace('(', '').replace(
        ')', '').replace(',', '|').replace("'", "").replace(' ', '')
    outfile.write("%s\n" % dict_keys2)

    key_list = []
    for key in dict_keys1:
        key_list.append(key)

    for sido in sido_list:
        try:
            store_list = getStoreInfoDealer(sido)[0]
            print(sido)
        except:
            print(sido, '수집 가능 한 리스트가 없어 해당 지역은 패스')
            pass
        else:

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

def getStore_list():
    url = 'https://www.audi.co.kr/kr/web/ko/service/service-center.20210406055130.headless.html'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    a = bsObj.find_all('a',{"class":"nm-layerLink nm-link nm-el-lk nm-el-lk-01 nm-at-lk-b nm-el-lk-ast"})
    result = []
    for info in a:
        link_lsit = info['href']
        link = str(link_lsit).split('/servicepopup/')[1].replace('.html','')
        result.append(link)
    return result

def getStoreInfo(url_list):
    url = 'https://www.audi.co.kr/kr/web/ko/service/service-center/servicepopup/{}.20210406055130.headless.html'.format(url_list)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = '아우디서비스센터'
    infos = bsObj.find('div',{"class":"audi-copy-m nm-content-paragraph__text"}).text
    infos = infos.split(':')
    print(infos)
    branch = bsObj.find('h3').text
    addr = str(infos[1]).replace('T e l ','').lstrip().rstrip()
    tell = str(infos[2]).replace('e-mail ','').replace('E-mail','').lstrip().rstrip()
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result


def getStoreInfoDealer(region):
    url = 'https://dealersearch.audi.com/api/json/v2/audi-kor/city'
    data = {
        # 'q': '서울',
        'clientId': 'b95656b9c4',
    }
    data['q'] = region
    result = []
    try:
        pageString = requests.get(url, params = data).text
        jsonString = json.loads(pageString)
        entityList = jsonString['partners']

    except : pass
    else:
        dict_key = ''
        for info in entityList:
            vendorId = info['vendorId']
            name = info['name']
            url = info['url']
            phone= info['contactDetails']['phone']['display']
            chainName = info['chainName']
            addr = info['address']['city']+' '+info['address']['street']
            latitude = info['address']['latitude']
            longitude = info['address']['longitude']
            result_dict = {'name':name,'vendorId':vendorId,'url':url,'phone':phone,'chainName':chainName,'addr':addr,'latitude':latitude,'longitude':longitude}
            dict_key = result_dict.keys()
            result.append(result_dict)
        return result, dict_key

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()