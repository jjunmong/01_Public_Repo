import bs4
import requests
import codecs
import sys

def main():

    outfile=codecs.open('11_메가엠지씨커피.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if len(store_list) == 1 : break
        for store in store_list:
            if store['branch'] == '매장명검색' : pass
            else:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s\n' % store['addr'])
        page += 1
    outfile.close()

def getStoreInfo(pageNo):
    url = "http://www.megacoffee.me/bbs/board.php?bo_table=store&page={}".format(pageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    store_list = bsObj.findAll("tr",{"bgcolor":"#FFFFFF"})
    data = []
    for td in store_list:
        try:
            name = "메가MGC커피"
            branch = td.select("td")[1].text.replace("\n","").replace(" ","").rstrip().lstrip().upper()
            addr1 = td.select("td")[0].text.replace("\n","").rstrip().lstrip().upper()
            addr2 = td.select("td")[2].text.replace("\n","").rstrip().lstrip().upper()
            addr3 = addr1+addr2
            addr4 = addr3.replace("부산부산","부산").replace("서울서울","서울").replace("경기경기","경기").replace("대전대전","대전")\
                .replace("대구대구","대구").replace("울산울산","울산").replace("인천인천","인천").replace("광주광주","광주").replace("강원강원","강원")\
                .replace("충북충청북도","충청북도").replace("충남충청남도","충청남도").replace("경북경상북도","경상북도")\
                .replace("경남경상남도","경상남도").replace("전북전라북도","전라북도").replace("전남전라남도","전라남도").replace("제주제주","제주")
            addr5 = addr4.replace("경기도도","경기도").replace("경남경남","경상남도").replace("경북경북","경상북도").replace("광주전라남도","전라남도") \
                .replace("전남전남", "전라남도").replace("전남광주광역시","광주광역시").replace("전북전북","전라북도").replace("충남충남","충청남도").replace("충북충북","충청북도")
        except IndexError :
            pass
        except AttributeError :
            pass
        else :
            data.append({"name":name,"branch":branch,"addr":addr5})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()