import requests
import codecs
import time
import sys
import random
import bs4


def main():

    outfile = codecs.open('18_크린위드.txt', 'w', 'utf-8')
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
    url = "http://www.cleanwith.co.kr/bbs/board.php?bo_table=findshop&page={}".format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    print(url, intPageNo)
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '크린위드'
            branches = info.select('a')[2]
            branches = str(branches).split('>')
            branch = branches[1]
            branch = branch.replace('</a','').replace('\n','').replace(' ','').replace('크린위드','')
            addr = info.find('td',{"class":"td_branch_addr"}).text.replace(' / ','')
            tell = info.find('td',{"class":"td_branch_name"}).text
        except: pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()