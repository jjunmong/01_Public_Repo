import sys
import codecs
import requests
import bs4
import random
import time

def main():

    outfile = codecs.open('41_투쿨포스쿨.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True :
        store_list = getStoreInfo(page)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
        if page == 4 : break
        time.sleep(random.uniform(0.3, 0.9))
    outfile.close()

def getStoreInfo(intPageNo):
    url = 'https://www.toocoolforschool.com/board/board.html?code=toocool4_board5&page={}&board_cate=6'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    print(url, intPageNo)
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '투쿨포스쿨'
            branch = info.find('div',{"class":"td_wrap store_name"}).text.replace(' ','')
            branch = branch.split(']')
            branch = branch[1].replace('\n','')
            addr = info.find('div',{"class":"sbj"}).text.replace('\n','').lstrip().rstrip()
            tell = info.select('div')[2]
            tell = str(tell).replace('<div class="td_wrap">','').replace('</div>','').lstrip().rstrip()
        except : pass
        else:
            result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
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

