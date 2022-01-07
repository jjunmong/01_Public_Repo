import time
import codecs
import requests
import random
import bs4
from datetime import datetime

def main():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\롯데마트(휴무일)_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("NAME|BRANCH|TELL|WORKTIME|CLOSEDATE|OLDADDR|NEWADDR\n")

    page = 1
    while True:
        store_list = getinfo(page)
        if store_list == []: break;
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['detail_info'])
            outfile.write(u'%s\n' % store['addr'])
        page += 1
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getinfo(intPageNo):
    url = 'http://company.lottemart.com/bc/branchSearch/branchSearch.do?currentPageNo={}&schStrCd=&schRegnCd=&schStrNm=&schBrnchTypeCd=BC0701&schBrnchNm=&tempVal='.format(intPageNo)
    htmlString = requests.get(url).text
    print(url,intPageNo)
    html = bs4.BeautifulSoup(htmlString, 'html.parser')
    li = html.find_all('div',{"class":"bx_type1"})
    data = []
    for info in li :
        try:
            name = '롯데마트몰'
            branch = info.find('h3').text.replace('\t','').replace('\xa0','').replace('\t','').replace('\n','').replace('\r','')
            detail_info = info.find('p').text.replace('\t','').replace('\xa0','').replace('\t','').replace('\n','').replace('\r','').replace('                                                ','').replace('휴점일','|휴점일')
            old_addr1 = info.select('ul')[2]
            old_addr2 = old_addr1.text.replace('\n신','').replace('\n구','|').replace('\n','')
            addr = old_addr2
        except : pass
        else : data.append({"name":name,"branch":branch,"detail_info":detail_info,"addr":addr})
    return data

main()