import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('35_오피스넥스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")


    store_List = getinfo()
    for store in store_List:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    outfile.close()

def getinfo():
    url = 'http://www.officenex.com/company/mapInfo.do#m_tab01'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find_all('tr')
    print(url)
    result =[]
    for infos in tbody:
        try:
            name = "오피스넥스"
            branch = infos.find("th", {"class": "first"}).text
            info3 = infos.select('td')
            info2 = str(info3).replace('\r','').replace('\n','').replace('\t','')
            info = info2.split('<')
            addr = str(info[1]).replace('td class="addr">','')
            tell= str(info[4:5]).replace("['td>","").replace("']","").replace(')','-')
        except : pass
        else:
            if branch == "매장": pass
            else:
                result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()