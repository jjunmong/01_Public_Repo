import sys
import codecs
import requests
import bs4

def main():

    outfile = codecs.open('32_약손명가.txt', 'w', 'utf-8')
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
    url = 'http://www.beautymade.com/kor/contents.php?code=010501&sca=&sido=&search_target=&search_keyword=&page={}'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    print(url ,intPageNo)
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '약손명가'
            branch = info.select('span')[0]
            branch = str(branch).split('>')
            branch = branch[1].replace('\n','').replace('\t','').replace('</span','').lstrip().rstrip()
            addr = info.select('span')[1]
            addr = str(addr).split('>')
            addr = addr[1].replace('\n','').replace('\t','').replace('</span','').lstrip().rstrip()
            tell = info.select('td')[3]
            tell = str(tell).split('>')
            tell = tell[1].replace('\n','').replace('\t','').replace('</td','').lstrip().rstrip()
        except : pass
        else:
            result.append({"name": name, "branch": branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
