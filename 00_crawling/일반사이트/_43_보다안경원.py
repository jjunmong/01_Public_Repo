import sys
import codecs
import requests
import bs4
import random
import time

def main():

    outfile = codecs.open('43_보다안경원.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True :
        store_list = getStoreInfo(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1

        time.sleep(random.uniform(0.3, 0.9))
    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.vodaeyewear.co.kr/store/store_search?keyword=0&area=0&area2=0&shop_no=0&shop_sort=1&per_page={}'.format(intPageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    print(url, intPageNo)
    div = bsObj.find('div',{"class":"map_list"})
    li = div.find_all('li')
    result = []
    for info in li:
        name = '보다안경원'
        branch = info.find('h4').text.replace('보다안경원','').replace('(','').replace(')','')
        infos = info.find('div',{"class":"map_info"})
        infos = str(infos).split('<br/>')
        addr = infos[0].replace('<div class="map_info">','').rstrip().lstrip()
        tell = infos[1].replace('</div>','')
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

