import sys
import time
import requests
import random
import codecs
import bs4
import json

def main():
    url_list = getStoreInfoList()
    outfile = codecs.open('47_볼보트럭.txt', 'w', 'utf-8')
    dict_keys1 = getStoreInfo(url_list[0])[1]
    dict_keys2 = str(dict_keys1).replace('dict_keys', '').replace('[', '').replace(']', '').replace('(', '').replace(
        ')', '').replace(',', '|').replace("'", "").replace(' ', '')
    outfile.write("%s\n" % dict_keys2)

    key_list = []
    for key in dict_keys1:
        key_list.append(key)

    for url in url_list:
        store_list = getStoreInfo(url)[0]
        print(url)
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

def getStoreInfoList():
    url = 'https://www.volvotrucks.kr/ko-kr/tools/dealer-locator.html'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    b = bsObj.findAll('b')
    result = []
    for info in b:
        storeName = info.find('a')['href'].split('/')[10]
        result.append(storeName)
    return result

def getStoreInfo(storeName):
    url = 'https://www.volvotrucks.kr/ko-kr/tools/dealer-locator/{}'.format(storeName)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = bsObj.find('h3').text
    addr = bsObj.select_one('body > div.root.responsivegrid > div > div.responsivegrid.main-grid.aem-GridColumn.aem-GridColumn--default--12 > div > div:nth-child(3) > section > div > div:nth-child(1) > div > div > p:nth-child(3)').text
    tell = bsObj.select_one('body > div.root.responsivegrid > div > div.responsivegrid.main-grid.aem-GridColumn.aem-GridColumn--default--12 > div > div:nth-child(3) > section > div > div:nth-child(1) > div > div > p:nth-child(4)').text
    timeinfo = []
    n= 6
    while True:
        try :
            pinfo = bsObj.select('p')[n].text.replace('\xa0','')
            if pinfo == ''or pinfo =='홈페이지 바로가기>' or pinfo =='홈페이지 바로가기 >': break
            timeinfo.append(pinfo)
        except :
            break
        n+=1
    result_dict={'name': name, 'addr': addr, 'tell': tell, 'timeinfo': timeinfo}
    dict_key = result_dict.keys()
    result.append(result_dict)
    return result,dict_key

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()