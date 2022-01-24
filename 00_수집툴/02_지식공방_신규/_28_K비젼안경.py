import sys
import codecs
import requests
import bs4

def main():

    outfile = codecs.open('28_K비젼안경.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

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
    url = "https://www.kvisionoptical.com/store"
    data = {
        '/store': '',
        'focus': 'sub_menu',
        # 'pgn_page': '2',
    }
    data['pgn_page'] = intPageNo
    pageString = requests.get(url, params = data)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    print(url, intPageNo)
    ul = bsObj.find('ul',{"class":"store_lists clearfix pt25"})
    li = ul.find_all('div',{"class":"wrapper"})
    result = []
    for info in li:
        try:
            name = 'K비젼안경'
            branch = info.find('h4').text.replace('K비젼안경','').replace(' ','')
            addr = info.find('p').text
            tell = info.select('a')[1]['href']
            tell = str(tell).replace('tel:','')
        except: pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
