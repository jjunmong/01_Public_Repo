import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('32_연안식당.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORDL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page += 1
        if page == 50 : break;
        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.yeonansikdang.co.kr/board/index.php?board=map_01&sca=all&type=list&select=&search=&page={}'.format(intPageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    entity_list = bsObj.find_all("li",{"class":"store_li"})
    data = []
    for infos in entity_list:
        try:
            name = "연안식당"
            branch = infos.find('p',{'class':'store_tit'}).text.lstrip().rstrip().upper()
            addr = infos.find('span',{'class':'ellipsis'}).text.lstrip().rstrip().upper()
            try:
                tell = infos.find('p',{"class":"store_txt m_t20"}).text.lstrip().rstrip().upper().replace('전화 ','')
            except :
                tell = ''
            cord = infos.select('script')
            cord = str(cord).split(':')
            xcord  = cord[5].replace("'","").replace("},\n\t\t\t\t\tscrollwheel","").lstrip().rstrip()
            ycord = cord[4].replace("'","").replace(", lng","").lstrip().rstrip()
        except:
            pass
        else:
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()