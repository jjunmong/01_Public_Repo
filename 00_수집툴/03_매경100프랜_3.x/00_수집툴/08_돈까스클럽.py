import requests
import sys
import codecs
import bs4


def main():

    outfile=codecs.open('08_돈까스클럽.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        if page == 300 : break
    outfile.close()

def getStoreInfo(pageNo):
    url ="http://www.tonkatsuclub.co.kr/shopinfo/shop-find-detail.php?seq={}".format(pageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    tbody = bsObj.find_all("tbody")
    data = []
    for list in tbody :
        try :
            name = "돈까스클럽"
            branch = list.select("td")[1].text.replace(" ","").rstrip().lstrip().upper()
            addr = list.select("td")[3].text.rstrip().lstrip().upper()
            tell = list.select("td")[5].text.rstrip().lstrip().upper()
        except : pass
        else :
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()


