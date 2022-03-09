import sys
import codecs
import requests
import bs4

def main():

    outfile = codecs.open('29_렌즈디바.txt', 'w', 'utf-8')
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
    url = "https://lensdiva.com/board/board_list.php"
    data = {
        'board_name': 'branch',
        'view_id': '0',
        # 'page': '2',
    }
    data['page'] = intPageNo
    pageString = requests.get(url, params = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url, intPageNo)
    ul = bsObj.find('tbody')
    li = ul.find_all('tr')
    result = []
    for info in li:
        try:
            name = '렌즈디바'
            branch = info.find('td',{"class":"subject"}).text.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            addr = info.find('td',{"style":"text-align:left;"}).text
            tell = info.select('td')[5]
            tell = str(tell).replace('<td>','').replace('</td>','')
        except : pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
