import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('109_핸즈커피.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        print(page)
        if storeList == [] : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page +=1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://handscoffee.com/new_hands/store/sub1-1.php?m_no=1&s_no=5&bo_table=&page={}&chkBox_0=&chkBox_1=&chkBox_2=&chkBox_3=&chkBox_4=&chkBox_5=&chkBox_6=&chkBox_7=&chkBox_8=&chkBox_9=&chkBox_10=&sch_addr1=&sch_addr2=&sch_key='.format(intPageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '핸즈커피'
            branch = info.find('a').text.replace('\n','').replace('\t','').replace('\xa0','').lstrip().rstrip()
            addr = info.find('td',{"class":"bright"}).text
            tell = info.find('div',{"class":"visible_mcall"}).text.replace('\n','').replace('\t','').replace('\xa0','').replace('.','-')
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()