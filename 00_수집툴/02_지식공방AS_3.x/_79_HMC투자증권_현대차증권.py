import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('79_HMC투자증권(현대차증권).txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    time.sleep(random.uniform(0.3,0.6))
    outfile.close()
def getStoreInfo():
    url = 'https://www.hmsec.com/goMenu.do?scr_menu_id=CO0105'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=L8j7FXfiraXswkxR6zV4YLZdtKTm8Iu8rkPp6IUw11xlqu3Spbbtwc4d7aIdq6Mj.cGhtcGFwX2RvbWFpbi9waG1wYXAwMV9jb25obWc=',
        'Host': 'www.hmsec.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.hmsec.com/main.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div = bsObj.find("div",{"class":"list_map"})
    tr = div.find_all("tr")
    result = []
    for info in tr:
        try:
            name = '현대차증권'
            branch = info.find('td').text
            addr = info.find('a').text
            tell = str(info.select('td')[2]).replace('<td class="ta_c">','').replace('</td>','')
            cord = str(info.find('a')['onclick']).split(',')
            xcord = str(cord[1]).strip().replace("'","")
            ycord = str(cord[2]).strip().replace("'","").replace('); return false;','')
        except:
            pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,"xcord":xcord,"ycord":ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()