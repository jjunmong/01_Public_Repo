import requests
import bs4
import codecs
import random
import time

def main():
    outfile = codecs.open('NICEPARK.txt', 'w', 'utf-8')
    outfile.write("NAME|XCORD|YCORD|ADDR\n")

    page = 1
    while True:
        result = getStoreInfo(page)
        print(page)
        if len(getStoreInfo(page)) < 10:
            for results in result:
                outfile.write(u'%s|' % results['name'])
                outfile.write(u'%s|' % results['xcord'])
                outfile.write(u'%s|' % results['ycord'])
                outfile.write(u'%s\n' % results['addr'])
            break
        else:
            for results in result:
                outfile.write(u'%s|' % results['name'])
                outfile.write(u'%s|' % results['xcord'])
                outfile.write(u'%s|' % results['ycord'])
                outfile.write(u'%s\n' % results['addr'])
        page+=1
        time.sleep(random.uniform(1, 1.3))
    outfile.close()

def getStoreInfo(intPageNo):
    url = 'https://home.nicepark.co.kr:5443/cus/map/map.do'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    }
    data = {
        # 'pageIndex': '80',
        'bbsId': '',
        'csrf': '',
        'searchOption': '',
        'searchValue': '',
    }
    data['pageIndex'] = intPageNo
    urlopen = requests.post(url, headers = header, data = data).text
    bsObj = bs4.BeautifulSoup(urlopen,"html.parser")
    tbody = bsObj.find('tbody')
    tr = tbody.find_all('tr')
    data = []
    for info in tr:
        try:
            name = info.find('a').text
            cord= info.select('a')[1]['href']
            cord = str(cord).split(',')
            ycord = str(cord[1]).replace("'","")
            xcord = str(cord[0]).replace('javascript:drawMap(','').replace("'","")
            addr = info.select('td')[2]
            addr = str(addr).replace('</td>','').replace('<td>','')
        except : pass
        else:
            data.append({'name':name, 'xcord':xcord,'ycord':ycord, 'addr':addr})
    return data

main()