import sys
import requests
import bs4
import codecs
import time
import random

def main():

    outfile = codecs.open('86_청춘쌀핫도그.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s\n' % store['addr'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(intPageNo):
    url = 'https://chungchunhotdog.com/bizdemo32468/store/sub1.php?&com_board_search_code=&com_board_search_value1=&com_board_search_value2=&com_board_page=&&com_board_id=9&&com_board_category_code=&com_board_search_code=&com_board_search_value1=&com_board_search_value2=&com_board_page={}'.format(intPageNo)
    pageString = requests.get(url)
    print(intPageNo)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    div = bsObj.find('div',{"class":"brd_photo_list"})
    td = div.find_all('table')
    result = []
    for info in td:
        name = '청춘쌀핫도그'
        branch = info.find('span',{"class":"gallery_title"}).text.replace('\r','').replace('\n','').replace('\t','')
        if branch.startswith('[') == True : branch = str(branch.split(']')[1]).replace(' ','')
        addr = info.find('td',{"class":"gallery_etc"}).text.replace('\r','').replace('\n','').replace('\t','').replace(' [매장주소 : ','')
        result.append({'name':name,'branch':branch,'addr':addr})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()