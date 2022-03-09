import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('71_중한자동차서비스센터.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1

        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://zhmotors.wdw.kr/bbs/board.php?bo_table=map&page={}'.format(intPageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '중한자동차서비스센터'
            try:
                branch = info.find('td').text
                branch1 = branch.split('\n')
                branch2 = str(branch1[2]).replace('\t','').replace('\n','').lstrip().rstrip().replace(' ','')
            except :
                branch2 = branch
            addr =str(info.select('td')[2]).replace('<td align="center">','').replace('</td>','').replace('\r','').replace('\t','').replace('\n','').lstrip().rstrip()
            tell =str(info.select('td')[1]).replace('<td align="center">','').replace('</td>','').replace('\r','').replace('\t','').replace('\n','').lstrip().rstrip()

        except: pass
        else:
            if branch == '판매거점':
                pass
            else:
                result.append({'name':name,'branch':branch2,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()