import bs4
import requests
import codecs
import sys

def main():
    outfile = codecs.open('05_김가네김밥.txt', 'w', 'utf-8')
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
    url = "http://gimgane.co.kr/board/index.php?board=map_01&sca=all&type=list&select=&search=&page={}".format(pageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    tr = bsObj.find_all('tr')
    data = []
    for info in tr :
        try:
            name = "김가네김밥"
            branch = info.find("td",{"class":"t_center"}).text.replace(" ","").rstrip().lstrip().upper()
            addr = info.find("td",{"class":"ellipsis"}).text.rstrip().lstrip().upper()
            tell = info.select("td",{"class":"t_center"})[2].text.rstrip().lstrip().upper()
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