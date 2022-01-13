import bs4
import requests
import codecs
import sys

def main():
    outfile = codecs.open('23_세븐스타코인노래방.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    url_info = getStoreList_all()
    for url in url_info:
        store_list = getStoreInfo(url)
        print(url)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
    outfile.close()

def getStoreList(intPageNo):
    url = "https://www.7starcoin.co.kr/_new/index/0501.php?code=0501&startPage={}&code=0501&search_item=&search_order=&search_sido=&search_gugun=&search_gubun=&search_amenity=".format(intPageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tbody = bsObj.find_all("tr")
    result = []
    for info in tbody:
        try:
            branch = info.find("a")['href']
        except :
            pass
        else:
            branch = str(branch).split('?')[1]
            if branch.startswith('idx=') == True : result.append(branch)
            else : pass
    return result

def getStoreList_all():
    result = []
    page = 0
    while True:
        result = result + getStoreList(page)
        if getStoreList(page) == [''] : break
        elif getStoreList(page) == '': break
        elif getStoreList(page) == [] :break
        print(page)
        page += 8
    return result

def getStoreInfo(url_info):
    url = "https://www.7starcoin.co.kr/_new/index/storeView.php?"+url_info
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tbody = bsObj.find_all("table")
    data = []
    for list in tbody:
        try:
            name = "세븐스타코인노래방"
            branch = list.select('td')[0].text.replace(" ","").rstrip().lstrip().upper()
            addr =  list.select('td')[1].text.rstrip().lstrip().upper()
            tell = list.select('td')[2].text.replace(" ","").rstrip().lstrip().upper()
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