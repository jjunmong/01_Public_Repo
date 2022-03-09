import sys
import codecs
import requests
import bs4

def main():

    outfile = codecs.open('26_에이치스타일.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list ==[] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])

        page +=1

    outfile.close()

def getStoreInfo(intPageNo):
    url = "http://www.hstylehairsalon.com/shop/search.asp"
    data = {
        # 'page': '1',
        'localCode': '',
        'shopName': ''
    }
    data['page'] = intPageNo
    pageString = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url, intPageNo)
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '에이치스타일'
            branch1 = info.find('td', {"class": "name"}).text.replace('H스타일','').replace('H스타일','').replace('Hstyle','').replace('.','').replace(' ','').replace('헤어살롱','')
            branch2 = str(branch1).split(')')
            try:
                branch = branch2[1]
            except :
                branch = branch1
            addr = info.find('td', {"class": "add"}).text
            tell =info.find('td', {"class": "tel"}).text
        except : pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
