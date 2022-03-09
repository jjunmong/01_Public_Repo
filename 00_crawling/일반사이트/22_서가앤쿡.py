import bs4
import requests
import codecs
import sys

def main():

    outfile=codecs.open('22_서가앤쿡.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    outfile.close()

def getStoreInfo():
    url = "https://www.seogaandcook.com/sns/bbs/board.php?bo_table=store&sca=서가앤쿡#sec3"
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tbody = bsObj.find_all("div")
    result = []
    for list in tbody:
        try:
            name = "서가앤쿡"
            branch = list.find("div",{"class":"t1"}).text.replace(" ","").rstrip().lstrip().upper()
            addr = list.find("div",{"class":"aa2"}).text.replace("주소","").rstrip().lstrip().upper()
            tell = list.find("div",{"class":"t2"}).text.replace("전화","").replace(".","-").rstrip().lstrip().upper()
        except AttributeError :
            pass
        else :
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()