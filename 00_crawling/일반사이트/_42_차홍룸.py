import sys
import codecs
import requests
import bs4
import random
import time

def main():

    outfile = codecs.open('42_차홍룸.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    url_list = getStoreInfo_list()
    for url in url_list:
        store_list = getStoreInfo(url)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])

        time.sleep(random.uniform(0.3, 0.9))
    outfile.close()

def getStoreInfo_list():
    url = 'http://chahongsalon.com/salon/chahong-room/'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    print(url)
    div = bsObj.find('div',{"class":"row large-columns-4 medium-columns-3 small-columns-2"})
    div_all = div.find_all('div',{"class":"page-col col"})
    result = []
    for info in div_all:
        a = info.find('a')['href']
        result.append(a)
    return result

def getStoreInfo(urls):
    url = urls
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString, "html.parser")
    print(url)
    result = []
    name = '차홍룸'
    branch = bsObj.select('div > div > h4 > strong')
    branch = str(branch).replace('[<strong>','').replace('</strong>]','').replace('차홍룸','').replace(' ','')
    infos = bsObj.select('div > div > p > strong')

    try:
        infos = str(infos).split('<br/>')
        addr = infos[0].replace('[<strong>','').lstrip().rstrip()
        tell = infos[1].replace('</strong>','').replace("']","").replace('</strong>]','').replace('예약문의','').replace(':','').replace('','').lstrip().rstrip()
    except:
        try:
            addr = infos[0]
            addr = addr.replace('<strong>','').replace('</strong>','').lstrip().rstrip()
            tell = infos[1]
            tell = tell.replace('예약문의','').replace("']","").replace('</strong>]','').replace(':','').replace('','').replace('<strong>','').replace('</strong>','').replace('<span class="tell">','').replace('</span>','').lstrip().rstrip()
        except:
            try:
                infos = str(infos).split('예약문의 :')
                addr = infos[0].replace("['[<strong>","").replace('</strong>','').replace('<strong>','').lstrip().rstrip()
                tell = infos[1].replace('<span class="tell">','').replace("']","").replace('</strong>]','').replace('</span>','').replace('<strong>','').lstrip().rstrip()
            except :
                infos = bsObj.select('div > div > p')
                infos = str(infos).split('<br/>')
                addr = infos[0].replace('[<p>', '').replace('<strong>','').replace('</strong>','').lstrip().rstrip()
                tell = infos[1].replace('</p>', '').replace('<p>', '').replace("']","").replace('예약문의 : ', '').replace('<strong>','').replace('</strong>','').lstrip().rstrip()
                tell = str(tell.split(',')[0]).replace(']','')
    result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

