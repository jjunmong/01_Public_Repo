import sys
import codecs
import requests
import bs4
import json

def main():

    outfile = codecs.open('34_으뜸50안경원.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|XCORD|YCORD\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page +=1
        if page == getstoreNum(): break

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://top50glasses.com/ajax/get_map_list.cm'
    data = {
        'board_code': 'b20190531d35ea98f47eb0',
        'search': '',
        'search_mod': 'all',
        'page': '2',
        'sort': 'NAME',
        'status': '',
    }
    data['page'] = intPageNo
    pageString = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url ,intPageNo)
    div_all = bsObj.select('div')
    result = []
    for info in div_all:
        try:
            name = '으뜸50안경'
            branch = info.find('div',{"class":"tit"}).text.replace(' ','')
            addr = info.find('p',{"class":"adress"}).text
            xcord = info.select('input')[0]['value']
            if str(xcord) == 'all' : xcord = ''
            elif str(xcord).startswith('[{"category_cod') == True: xcord = ''
            ycord = info.select('input')[1]['value']
            if str(ycord).startswith('Y') == True : ycord = ''
        except : pass
        else:
            if branch == '142': pass
            elif xcord == '' : pass
            else :
                result.append({"name": name, "branch": branch,"addr":addr,"xcord":xcord,"ycord":ycord})
    results = set()
    new_results = []
    for list in result:
        lists = tuple(list.items())
        if lists not in results:
            results.add(lists)
            new_results.append(list)
    return new_results

def getstoreNum():
    url = 'http://top50glasses.com/map'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    listNum = bsObj.select('#map_list_fold_b20190531d35ea98f47eb0 > div.map-list > div.map-toolbar > div.toolbar_top.map-inner > div.head_wrap.clearfix > div.tit > span')
    listNum = str(listNum).split('>')[1]
    listNum = listNum.replace('</span','')
    listNum = int(int(listNum) // 10 + 2)
    return listNum


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
