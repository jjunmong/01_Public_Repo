import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver

def main():

    outfile = codecs.open('29_KDB생명.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo_Basic()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    store_list = dupRemove()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    outfile.close()

def getStoreInfo_Basic():
    driver = webdriver.Chrome(r'C:\chromedriver.exe')
    driver.get('https://www.kdblife.co.kr/ajax.do?scrId=HCSCT003M01P')
    time.sleep(3)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    tbody = soup.find('tbody',{"id":"table_grid01"})
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            name = "KDB생명 금융프라자"
            branch = info.select('td')[0]
            branch = str(branch).replace('<td class="ta-c" style="border-bottom: 1px solid #e5e5e5;">','').replace('<td class="ta-c rows" rowspan="5">','').replace('</td>','').lstrip().rstrip()
            if branch == '금융프라자' :
                branch = '본사'
            addr = info.find('a').text
            tell = info.select('td')[2]
            tell = str(tell).replace('<td class="ta-c" style="border-bottom: 1px solid #e5e5e5;">','').replace('</td>','').lstrip().rstrip()
            if branch == '본사' :
                tell = info.select('td')[3]
                tell = str(tell).replace('<td class="ta-c" style="border-bottom: 1px solid #e5e5e5;">','').replace('</td>','').lstrip().rstrip()
        except:
            pass
        else:
            result.append({"name": name, "branch": branch, "addr": addr, "tell": tell})

    tbody1 = soup.find('tbody',{"id":"table_grid01_01"})
    tr1 = tbody1.find_all('tr')
    for info1 in tr1:
        try:
            name = 'KDB생명 CS BRNACH'
            branch = info1.select('td')[0]
            branch = str(branch).replace('<td class="ta-c">','').replace('<td class="ta-c rows" rowspan="4">','').replace('</td>','').lstrip().rstrip()
            if branch == 'CS Branch' :
                branch = '경인'
            addr = info1.find('a').text
            tell = info1.select('td')[2]
            tell = str(tell).replace('<td class="ta-c">', '').replace('</td>', '').lstrip().rstrip()
            if branch == '경인' :
                tell = info1.select('td')[3]
                tell = str(tell).replace('<td class="ta-c">','').replace('</td>','').lstrip().rstrip()
        except :
            pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def getStoreInfo():
    driver = webdriver.Chrome(r'C:\chromedriver.exe')
    driver.get('https://www.kdblife.co.kr/ajax.do?scrId=HCSCT003M01P')
    time.sleep(3)
    result = []
    for ss in range(10):
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tbody = soup.find('tbody',{"id":"table_grid02"})
        tr = tbody.find_all('tr')
        driver.find_element_by_css_selector('#table_grid_paging > ul > li.next > a').click()
        driver.switch_to.window(driver.window_handles[-1])
        for info in tr:
            name = 'KDB생명'
            branch = info.select('td')[0]
            branch = str(branch).replace('<td class="ta-c">','').replace('</td>', '').lstrip().rstrip()
            addr = info.find('a').text
            tell = info.select('td')[2]
            tell = str(tell).replace('<td class="ta-c">', '').replace('</td>', '').lstrip().rstrip()
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
        time.sleep(2)

    return  result

def dupRemove():
    result = getStoreInfo()
    results = set()
    new_results = []
    for list in result:
        lists = tuple(list.items())
        if lists not in results:
            results.add(lists)
            new_results.append(list)
    return new_results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()