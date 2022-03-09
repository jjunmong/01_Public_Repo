import bs4
import codecs
import time
import requests
import sys
import random

def main():

    outfile = codecs.open('17_스프리스.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    store_list = getStores()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    time.sleep(random.uniform(0.3,0.6))

    outfile.close()
def getStores():
    url = "http://m.spris.com/main/kor/store/store.asp?search_kind=&search_shop="
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ASPSESSIONIDSQSBAQCS=MMDPFOECICBKNAMNGBALNLIO',
        'Host': 'm.spris.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.google.co.kr/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    try :
        urlopen = requests.get(url, headers = headers)
        print(urlopen,url)
    except :
        print('Error calling the API')
        return  None

    urlopen.encoding = 'utf-8'
    html = urlopen.text
    bsObj = bs4.BeautifulSoup(html, "html.parser")
    li = bsObj.find_all('li')
    result = []
    for list in li:
        try:
            names = list['data-name']
            names = str(names).lstrip().rstrip()
            names = names.split(' ')
            name = names[0]
            branch = names[1:]
            branch = str(branch).replace('[','').replace(']','').replace(' ','').replace(',','').replace("'","")
            addr = list.select('dd')[1]
            addr = str(addr).replace('<dd>','').replace('</br></dd>','')
            tell = list.find("dd", {"class":"tel"})
            xcord = list['data-xpoint']
            ycord = list['data-ypoint']
        except : pass
        else:
            result.append({"name":name,"branch":branch, "addr":addr, "tell":tell,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()







