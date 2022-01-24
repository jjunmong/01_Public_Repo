import sys
import codecs
import requests
import bs4
import json

def main():

    outfile = codecs.open('38_E안경.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page +=1
        if page == getstoreNum(): break
    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://www.eankyoung.co.kr/ajax/get_map_list.cm'
    data = {
        'board_code': 'b201908312bf7e89c92500',
        'search': '',
        'search_mod': 'all',
        # 'page': '2',
        'sort': 'TIME',
    }
    data['page'] = intPageNo
    pageString = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url ,intPageNo)
    div_all = bsObj.select('div')
    result = []
    for info in div_all:
        try:
            name = 'E안경'
            branch = info.find('div',{"class":"tit"}).text.replace(' ','').replace('(주)','').replace('E안경','')
            addr = info.find('p',{"class":"adress"}).text
            tell = info.find('p',{"class":"tell"}).text.replace('phone number','')
            xcord = info.select('input')[0]['value']
            ycord = info.select('input')[1]['value']
        except : pass
        else:
            if branch == '매장안내17': pass
            else :
                result.append({"name": name, "branch": branch,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})
    results = set()
    new_results = []
    for list in result:
        lists = tuple(list.items())
        if lists not in results:
            results.add(lists)
            new_results.append(list)
    return new_results

def getstoreNum():
    url = 'http://www.eankyoung.co.kr/31'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    listNum = bsObj.select('#map_list_fold_b201908312bf7e89c92500 > div.map-list > div.map-toolbar > div.toolbar_top.map-inner > div.head_wrap.clearfix > div.tit > span')
    listNum = str(listNum).split('>')[1]
    listNum = listNum.replace('</span','')
    listNum = int(int(listNum) // 10 + 2)
    return listNum

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

