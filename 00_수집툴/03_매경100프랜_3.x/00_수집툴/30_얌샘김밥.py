import requests
import codecs
import time
import sys
import random
import bs4

def main():

    outfile = codecs.open('30_얌샘김밥.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TIME|TELL\n")

    page = 1
    while True:
        store_List = getStoreInfo(page)
        if len(store_List) < 10 : break
        for store in store_List:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['time_info'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        if page == 60: break
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.yumsem.com/data/shop/page={}'.format(intPageNo)
    data = []
    pageData = requests.get(url)
    print(url)
    pageData.encoding = 'utf-8'
    text = pageData.text
    pageString = bs4.BeautifulSoup(text, "html.parser")
    tr = pageString.find_all("tr")
    for infos in tr:
        try:
            name = "얌샘김밥"
            branch = infos.find('p',{"class":"m_con_b m_name"}).text.replace('\xa0','').rstrip().lstrip().upper()
            addr = infos.select('p')[1].text.rstrip().lstrip().upper()
            time_info = infos.select('p')[2].text.rstrip().lstrip().upper().replace('\xa0','').replace('영업시간 : ','')
            tell = infos.select('p')[3].text.rstrip().lstrip().upper().replace('전화번호 : ','')
        except : pass
        else:
            data.append({"name":name,"branch":branch,"addr":addr,"time_info":time_info,"tell":tell})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()