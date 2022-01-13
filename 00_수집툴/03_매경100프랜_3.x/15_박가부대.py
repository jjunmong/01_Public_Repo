import bs4
import requests
import codecs
import json
import sys

def main():
    outfile=codecs.open('15_박가부대.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    list = getStoreList()
    for no in list:
        store_list = getStoreInfo(no)
        print(no)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
    outfile.close()

def getStoreList():
    url = "https://wonandone.co.kr/inc/storeMapData.asp"
    data = {
        'KeyBrand': 'b',
        'KeyOrder': 'S',
        'KeyAddr1': '',
        'KeyAddr2': '',
        'KeyWord': '점',
    }
    pageString = requests.post(url, data = data).text
    jsonstring = json.loads(pageString)
    entitylist = jsonstring['items']
    result = []
    for info in entitylist:
        idx = info['store_idx']
        result.append(idx)
    return result

def getStoreInfo(intpageNo):
    url = "https://wonandone.co.kr/inc/storeView.asp?store_idx={}".format(intpageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = '박가부대&치즈닭갈비'
    branch = bsObj.find('h4').text
    addr = str(bsObj.select('#store_view > div.con > div > div.info > div > table > tbody > tr:nth-child(1) > td')).replace('<td>','').replace('</td>','').replace('[','').replace(']','')
    tell = str(bsObj.select('#store_view > div.con > div > div.info > div > table > tbody > tr:nth-child(3) > td')).replace('<td>','').replace('</td>','').split('>')[1].replace(']','')
    time = str(bsObj.select('#store_view > div.con > div > div.info > div > table > tbody > tr:nth-child(4) > td')).replace('<td>','').replace('</td>','').replace('[','').replace(']','')
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
