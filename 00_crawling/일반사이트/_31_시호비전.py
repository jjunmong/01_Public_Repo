import sys
import codecs
import requests
import bs4

def main():

    outfile = codecs.open('31_시호비전.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreList_dup()

    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.seeho.co.kr/go/store_info.asp?CB=1&CP={}&MN=go10'.format(intPageNo)
    pageString = requests.post(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    print(url ,intPageNo)
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '시호비전'
            branch = info.find('td',{"width":"173"}).text.split(' ')
            branch = branch[0]
            addr = info.find('td',{"width":"300"}).text.replace('&nbsp;','').replace(' ','')
            tell = info.find('td',{"width":"99"}).text
        except : pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def getStoreList_all():
    result = []
    page = 1
    while True:
        result = result + getStoreInfo(page)
        if getStoreInfo(page) == []: break
        page += 1
    return result

def getStoreList_dup():
    result = getStoreList_all()
    results = set()
    new_results = []
    for list in result:
        lists = tuple(list.items())
        if lists not in results:
            results.add(lists)
            new_results.append(list)
    return new_results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
