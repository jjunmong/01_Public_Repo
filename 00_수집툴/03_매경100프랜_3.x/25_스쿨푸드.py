import bs4
import codecs
import requests
import time
import sys

def main():
    outfile=codecs.open('25_스쿨푸드.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
        page += 1
    outfile.close()

def getStoreInfo(intPageNo):
    url = "http://www.schoolfood.co.kr/store/store.html?page={}&lcode=&mcode=&keyword=&code=".format(intPageNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    ul = bsObj.find_all("ul",{"class":"txt_list"})
    result = []
    for info in ul:
        try:
            name = '스쿨푸드'
            branch = info.find('div',{"class":"des"}).text.replace('\n','').replace('\t','').replace(' ','')
            addr = str(info.select('div')[8]).replace('<div class="des">','').replace('</div>','').lstrip().rstrip()
            tell = str(info.select('div')[10]).replace('<div class="des">','').replace('</div>','').lstrip().rstrip()
            time = str(info.select('div')[6]).replace('<div class="des">','').replace('</div>','').lstrip().rstrip()
        except : pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'time':time})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()


