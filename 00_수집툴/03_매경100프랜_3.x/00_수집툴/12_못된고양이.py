import bs4
import requests
import codecs
import sys

def main():

    outfile=codecs.open('12_못된고양이.txt', 'w', 'utf-8')
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
            outfile.write(u'%s|\n' % store['tell'])
        page += 1
    outfile.close()

def getStoreInfo(pageNo):
    url = "http://n-cat.co.kr/wordpress/index.php/direction-list/?pageid={}".format(pageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.findAll("tr")
    data = []
    for list in tbody:
        try:
            name = "못된고양이"
            branch = list.find("td",{"class":"kboard-list-branch"}).text.replace(" ","").rstrip().lstrip().upper()
            addr = list.find("a").text.replace("\t","").rstrip().lstrip().upper()
            tell = list.find("td", {"class":"kboard-list-tel"}).text.rstrip().lstrip().upper()
        except AttributeError :
            pass
        else :
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
