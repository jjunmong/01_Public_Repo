import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver


def main():

    outfile = codecs.open('25_한국문화예술회관연합회.txt', 'w', 'utf-8')
    outfile.write("NAME|ADDR|OPENDATE|HOMEPAGE|FAX|TELL\n")

    page = getStore_id()
    print(page)
    for num in page:
        store_list = getStoreInfo(num)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['openDate'])
            outfile.write(u'%s|' % store['homepage'])
            outfile.write(u'%s|' % store['fax'])
            outfile.write(u'%s\n' % store['tell'])

        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStore_id():
    driver = webdriver.Chrome(r'C:\chromedriver.exe')
    driver.get('http://www.kocaca.or.kr/Pages/Member/OrgInformation.aspx')

    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    list_id_all = soup.find_all('p')
    data = []
    for id in list_id_all:
        try:
            id = id.find('a')['idorg']
        except :
            pass
        else:
            data.append(id)

    driver.close()

    return data

def getStoreInfo(intPageNo):
    driver = webdriver.Chrome(r'C:\chromedriver.exe')

    url = 'https://www.kocaca.or.kr/Pages/Member/Popup/OrgDetail.aspx?IdOrg={}'.format(intPageNo)

    driver.get(url)
    print(url)

    data=[]
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    name = soup.select('p',{"class":"postcode"})[0].text
    addr = soup.select('td',{"scope":"col"})[0].text
    openDate = soup.select('td',{"scope":"col"})[1].text.replace('\n','/')
    homepage = soup.select('td',{"scope":"col"})[4].text.replace('\n','')
    fax = soup.select('td',{"scope":"col"})[5].text
    tell = soup.select('td',{"scope":"col"})[6].text

    data.append ({"name":name,"addr":addr,"openDate":openDate,"homepage":homepage,"fax":fax,"tell":tell})

    driver.close()

    return data
def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()