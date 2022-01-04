import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('57_탐앤탐스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    idx_list = getStore_ID_all()
    for id in idx_list:
        store_list = getStoreInfo(id)
        print(id)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStroeID(sido_name):
    url = "https://www.tomntoms.com/store/domestic_store_search.html"
    data = {}
    data['keyword'] = sido_name
    pageString = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    page = str(bsObj)
    page1 = page.split('var positions = ')[1]
    page1 = str(page1).split('var imageSrc =')[0]
    page1 = page1.replace(';', '')
    page1 = page1.replace('/', '')
    page1 = page1.replace(':', '')
    page1 = page1.replace('"', '')
    page1 = page1.replace('content','"content":')
    page1 = page1.replace('latlng', '"latlng":')
    page1 = page1.replace('title', '"title":')
    page1 = page1.replace('uid', '"uid":')
    page1 = page1.replace("'", '"')
    page1 = page1.replace("'<", '"<')
    page1 = page1.replace("'>", '">')
    page1 = page1.replace('new kakao', '"new kakao')
    page1 = page1.replace('),', ')",')
    page1 = page1.replace('},	]','}	]')
    page1 = page1.replace('\\n', '')
    page1 = page1.replace('#', '')
    page1 = page1.replace('-"content": ', '')
    jsonstring = json.loads(page1)
    result = []
    for info in jsonstring:
        uid = info['uid']
        result.append(uid)
    return result

def getStore_ID_all():
    result = []
    sido_list = ['서울', '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '인천', '대전', '울산', '광주', '대구', '부산', '세종', '제주']

    for sido in sido_list:
        result = result + getStroeID(sido)
        print(sido)
    results = list(set(result))
    return results

def getStoreInfo(intPageNo):
    url = 'https://tomntoms.com/pop/pop_store_info.html?uid={}'.format(intPageNo)
    response = requests.get(url).text
    bsObj = bs4.BeautifulSoup(response,"html.parser")
    result = []
    name = '탐앤탐스'
    branch = bsObj.find('h2',{"class":"tit"}).text
    addr = bsObj.find('p',{"class":"desc"}).text
    tell = bsObj.find('a',{"class":"desc ff-roboto"}).text.replace('T.','')
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()