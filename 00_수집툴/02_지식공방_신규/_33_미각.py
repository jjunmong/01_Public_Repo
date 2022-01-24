import sys
import codecs
import requests
import bs4

def main():

    outfile = codecs.open('33_미각.txt', 'w', 'utf-8')
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
    url = 'http://migak.kr/bbs/board.php?bo_table=branch&page={}'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url ,intPageNo)
    tbody = bsObj.find('tbody')
    tr = tbody.findAll('tr')
    result = []
    for info in tr:
        try:
            name = '미각'
            branch = info.select('a')[1]
            branch = str(branch).split('>')
            branch = str(branch[1]).lstrip().rstrip().replace('                </a','').replace(' ','')
            addr = info.find('td',{"class":"td_location"}).text
            tell = info.find('td',{"class":"td_name sv_use"}).text
        except : pass
        else:
            result.append({"name": name, "branch": branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
