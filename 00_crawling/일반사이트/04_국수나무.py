import bs4
import requests
import codecs
import sys

def main():
    outfile = codecs.open('04_NoodleTree.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])
    outfile.close()

def getStoreInfo():
    url = "http://www.namuya.co.kr/board/bbs/board.php?bo_table=franchise_sch"
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    list = bsObj.find_all("li")
    data = []
    for li in list:
        try:
            name = "국수나무"
            branch = li.find("span", {"class":"fl mg_r5 subject ygreen2"}).text.replace(" ","").rstrip().lstrip().upper()
            addr = li.find("span", {"class": "address"}).text.rstrip().lstrip().upper()
            tell = li.find("span", {"class": "tel"}).text.rstrip().lstrip().upper()
            xcord = li['data-lng']
            ycord = li['data-lat']
        except:
            pass
        else:
            data.append({"name": name, "branch": branch, "addr": addr, "tell": tell,"xcord":xcord,"ycord":ycord})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

