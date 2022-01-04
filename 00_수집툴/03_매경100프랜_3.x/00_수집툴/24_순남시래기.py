import bs4
import requests
import codecs
import sys

def main():
    outfile=codecs.open('24_순남시래기.txt', 'w', 'utf-8')
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
        page +=1
    outfile.close()

def getStoreInfo(codeNo):
    url = "http://www.soonnam.com/board/index.php?board=map_01&sca=all&type=list&select=&search=&select_type=&select_list=&page={}&now_date=9mqKe".format(codeNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tbody = bsObj.find_all("tr")
    data = []
    for list in tbody:
        try:
            name = "순남시래기"
            branch = list.find("td").text.replace(" ","").rstrip().lstrip().replace("\n","").replace("\t","")
            addr = list.find('td',{"class":"t_left"}).text.replace("\n","").replace("\t","")
            tell = list.select('tr > td')[2].text.replace(" ","").rstrip().lstrip().replace(")","-")
        except :
            pass
        else:
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

