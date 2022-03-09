import bs4
import requests
import codecs

def main():

    outfile=codecs.open('14_바보스.txt', 'w', 'utf-8')
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
    outfile.close()

def getStoreInfo(pageNo):
    url = "http://www.babos.co.kr/store-locator/branch.html?code=&v=&category=&page={}&keyfield=&Area_Sido_Num=&key=&year=&search_type=&Shop_Name2=".format(pageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find("tbody")
    data = []
    for list in tbody:
        try:
            name = "바보스"
            branch = list.find("a").text.replace(" ","").rstrip().lstrip().upper()
            addr = list.find("td", {"class": "alignL"}).text.rstrip().lstrip().upper()
            tell = list.select('td')[3].text.rstrip().lstrip().upper()
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

