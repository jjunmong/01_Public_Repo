import time
import codecs
import requests
import random
import bs4
from datetime import datetime
def main():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\현대오일뱅크_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XOCRD|YCORD|TRUCK\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == '' : break
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s\n' % store['truck'])
        page += 1
        time.sleep(random.uniform(2,3))

    outfile.close()
    print('수집종료')

def getStoreInfo(intPageNo):
    url = 'http://www.oilbankcard.com/card2012/front/boardList.do'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '112',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=8AF1C0FDEDFB5F64040CAFA54247168E; route=1600647760.224.952.473414; SCOUTER=z2uu0m3d71ufum; wcs_bt=1087fb6a1435d5:1600647761; __utma=85185159.1786310449.1600647762.1600647762.1600647762.1; __utmc=85185159; __utmz=85185159.1600647762.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'Host': 'www.oilbankcard.com',
        'Origin': 'http://www.oilbankcard.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.oilbankcard.com/card2012/front/boardList.do?page_num=810&pre_page_num=990&bcode=MAIN_OIL',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data ={
        'bcode': 'SEARCH_OIL',
        'Search_Type': 'CARGO',
        'si': '',
        'gu': '',
        # 'currPage': '2',
        'name': '',
    }
    data['currPage'] = intPageNo
    pageString = requests.post(url, data = data, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '현대오일뱅크'
            infos = str(info.find('a')['href']).split("'")
            branch = infos[5]
            addr = infos[7]
            tell = infos[11]
            xcord = infos[3]
            ycord = infos[1]
            truck_info = str(info.select('img'))
            truck = ''
            if 'picto_list05' in truck_info : truck = '화물차 우대'
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord,'truck':truck})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

main()