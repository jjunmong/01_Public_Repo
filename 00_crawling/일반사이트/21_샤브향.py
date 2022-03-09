import bs4
import requests
import codecs
import sys

def main():
    outfile=codecs.open('21_샤브향.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    url_list = getStoreList_all()

    for url in url_list:
        store_list = getStoreInfo(url)
        print(url)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])

    outfile.close()

def getStoreList(intPageNo):
    url = "http://shabuhyang.co.kr/default/online/01.php"
    data = {
        "top": "3",
        "sub": "0",
        "com_board_search_code": "",
        "com_board_search_value1": "",
        "com_board_search_value2": "",
        "com_board_page": "",
        "com_board_id": "21",
        "com_board_category_code": "",
        "com_board_search_code": "",
        "com_board_search_value1": "",
        "com_board_search_value2": "",
        # "com_board_page": "2",
    }
    data['com board page'] = intPageNo
    pageString = requests.get(url, params = data)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tr = bsObj.find_all("tr",{"align":"center"})
    result = []
    for info in tr:
        try:
            a = str(info['onclick']).split('?')[1]
            a = str(a).replace("; return false;'","").replace("'; return false;","")
        except: pass
        else:
            result.append(a)
    return result

def getStoreList_all():
    result = []
    page = 1
    while True:
        result =result + getStoreList(page)
        print(page)
        if getStoreList(page) == [] : break
        page += 1
    return result

def getStoreInfo(infos):
    url = 'http://shabuhyang.co.kr/default/online/01.php?'+infos
    print(url)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    result = []
    td = bsObj.find_all('td',{"class":"board_desc"})
    name = '샤브향'
    branch = str(td[0]).replace('<td class="board_desc">','').replace('\n','').replace('</td>','').replace('\r','').replace('\t','').lstrip().rstrip()
    addr = str(td[2]).replace('<td class="board_desc">','').replace('\n','').replace('</td>','').replace('\r','').replace('\t','').lstrip().rstrip()
    tell = str(td[3]).replace('<td class="board_desc">','').replace('\n','').replace('</td>','').replace('\r','').replace('\t','').lstrip().rstrip()
    time = str(td[1]).replace('<td class="board_desc">','').replace('\n','').replace('</td>','').replace('\r','').replace('\t','').lstrip().rstrip()
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()