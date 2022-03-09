import requests
import bs4
import codecs
import sys

def main():
    outfile = codecs.open('01_JMTjokbal.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if len(store_list) == 1 : break
        for store in store_list:
            if store['addr'] == 'HOME > 매장안내 > 가맹점안내':
                pass
            else:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|\n' % store['tell'])
        page += 1
    outfile.close()

def getStoreInfo(pageNo):
    url = "http://xn--o39au8jxvg8ncxvw6e18c.com/index.php?sd=3&sc=3_2&bCode=&s_name=&s_name2=&page=2&sd=3&sc=3_2&page={}".format(pageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    listall = bsObj.find_all(bgcolor = "#ffffff")
    data = []
    for tds in listall:
        try:
            storelist = tds.findAll("td")
            no=1
            name = "가장맛있는족발"
            branch = storelist[no].text.replace(" ","").rstrip().lstrip().upper()
            addr = storelist[no+1].text.rstrip().lstrip().upper()
            tell = storelist[no+2].text.rstrip().lstrip().upper()
        except:
            pass
        else:
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell})

    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()



