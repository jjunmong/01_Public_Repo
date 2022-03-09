import sys
import codecs
import requests
import bs4
import re
def main():

    outfile = codecs.open('45_타다대우상용차서비스네트워크.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")


    store_list = getStoreInfo_svc()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    outfile.close()

    outfile = codecs.open('45_타다대우상용차대리점.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo_dealer()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    outfile.close()


def getStoreInfo_dealer():
    url = 'https://www.tata-daewoo.com/guide/network'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',}
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    div = bsObj.find_all('div',{"class":"info"})
    result = []
    for info in div:
        name = '타타대우상용차'
        cat = '딜러'
        branch = info.find('p').text
        addr =  info.find('li').text.replace('· ADD','')
        tell = info.select('li')[1].text.replace('· TEL','')
        result.append({'name':name,'cat':cat,'branch':branch,'addr':addr,'tell':tell})
    return result

def getStoreInfo_svc():
    url = 'https://www.tata-daewoo.com/customer/network'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',}
    pageString = requests.get(url, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content, "html.parser")
    div = bsObj.find_all('div',{"class":"info"})
    result = []
    for info in div:
        name = '타타대우상용차'
        cat = '서비스'
        p = "\(.*\)|\s-\s.*"
        branch = info.find('p').text.replace('㈜','')
        branch = re.sub(p,'',branch)
        addr =  info.find('li').text.replace('· ADD','')
        addr = re.sub(p,'',addr)
        tell = info.select('li')[1].text.replace('· TEL','')
        result.append({'name':name,'cat':cat,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

