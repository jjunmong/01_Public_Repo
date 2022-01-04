from selenium import webdriver
import bs4
import time
import codecs
import time
import random
import io

outfile=codecs.open('14_LaLavLa.txt', 'w', 'utf-8')
outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

chromedriver_dir = r'C:\chromedriver.exe'
driver = webdriver.Chrome(chromedriver_dir)
driver.get('http://lalavla.gsretail.com/lalavla/ko/market-info')
time.sleep(1)

def getStore():
    listAll = []
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    tbody = soup.find('tbody')
    tr = tbody.find_all('tr')
    print(tr)
    for info in tr:
        name = "랄라블라"
        branch = info.select('td')[0].text.replace('랄라블라 ','').rstrip().lstrip()
        addr = info.select('dd')[1].text.rstrip().lstrip()
        tell = info.select('dd')[2].text.rstrip().lstrip()
        time = info.select('dd')[0].text.rstrip().lstrip()
        listAll.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time})
    return listAll

### 2020-01-06 기준 28 페이지 까지 존재함.

result = []
for repeat in range(0, 30):
    time.sleep(1)
    nextclick = driver.find_element_by_xpath('//*[@id="pagingTagBox"]/a[3]')
    nextclick.click()
    time.sleep(1)
    result = result + getStore()

results = set()
new_results = []
for list in result:
    lists = tuple(list.items())
    if lists not in results:
        results.add(lists)
        new_results.append(list)

for ss in new_results:
    print(ss)

for result_list in new_results:
    outfile.write(u'%s|' % result_list['name'])
    outfile.write(u'%s|' % result_list['branch'])
    outfile.write(u'%s|' % result_list['addr'])
    outfile.write(u'%s|' % result_list['tell'])
    outfile.write(u'%s|\n' % result_list['time'])

outfile.close()

driver.close()