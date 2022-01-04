import requests
import codecs
import bs4
import sys

def main():
    outfile = codecs.open('26_신전떡볶이.txt', 'w', 'utf-8')
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

def getStoreInfo(codeNo):
    url = "http://sinjeon.co.kr/pg/bbs/board.php?bo_table=store&page={}".format(codeNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tbody = bsObj.find_all("tr")
    data = []
    for list in tbody:
        try:
            name = "신전떡볶이"
            branch = list.select("td")[1].text.replace(" ","").rstrip().lstrip()
            addr = list.find('td',{"class":"td_branch_addr"}).text.rstrip().lstrip()
            tell = list.find('td',{"class":"td_branch_name"}).text.rstrip().lstrip()
        except : pass
        else:
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()