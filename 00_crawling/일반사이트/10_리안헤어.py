# 현재 41페이지 까지 50MAX 설정.
import bs4
import requests
import codecs
import sys

def main():
    outfile=codecs.open('10_리안헤어.txt', 'w', 'utf-8')
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
    url = "http://riahn.kr/niabbs5/inc.php?page={}&inc=maejang&sss_key=&ttt_key=&c=".format(pageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tbody = bsObj.find_all("tr")
    result = []
    for list in tbody:
        try:
            name = "리안헤어"
            branch = list.find("td",{"width":"200"}).text.replace("\xa0","").replace("\r","").replace("\n","").replace("\t","").replace(" ","").rstrip().lstrip()
            addr = list.find("td", {"width": "330"}).text.replace("\r","").replace("\n","").replace("\t","")
            tell = list.find("td", {"width": "100"}).text.replace("\r","").replace("\n","").replace("\t","").replace("\xad","")
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

