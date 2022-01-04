import sys
import requests
import bs4
import codecs
import time
import random
import json


def main():
    outfile = codecs.open('124_올리브영.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    page = 0
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        print(page)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page +=1
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()
    print('수집종료')

def getStoreInfo(intPageNo):
    url = 'https://www.oliveyoung.co.kr/store/store/getStoreListJsonAjax.do'
    data = {
        # 'pageIdx': '2',
        'searchType': 'word',
        'tabType': 'wordTab',
        'openYn': 'N',
        'tcCd': '',
        'psCd': '',
        'usrLat': '37.5157921',
        'usrLng': '127.12317879999999',
        'searchWord': '',
    }
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'c109f1b728296cc321984462b441ffee=1609140762765; JSESSIONID=lWOFqmGt211S4dHV1Ba87SKg37IeDlb2tuGjzacQWa74LiL8VJYOO7hMB1gn8sLg.cE95bWFsbF9kb21haW4vb3ltcHByZDMx; WMONID=M2IXvyDnkMj; RB_PCID=1598516794279903392; sch_check=yes; _trs_id=eY14171%3F414052%3F%3E6%3F; oliveyoung_CID=78a31f9bd8b0412894ac2f6973f18547; PCID=15985167950028834195893; EG_GUID=a1bc1c6d-adf6-4a1a-b684-061cc084ea6e; NetFunnel_Main=; _gid=GA1.3.1629131730.1609140761; _gat=1; _gat_UA-181867310-1=1; _trs_sid=G%5B6464566%3C5276%5Bg%5B36353%3D636270%3D%3C4%3D; _trs_flow=; wcs_bt=s_3ee47970f314:1609140763; _ga_GMKKBJ29S2=GS1.1.1609140760.1.1.1609140762.58; _ga=GA1.3.955389855.1598516795; RB_SSID=zR3mWM6X0Y',
        'Host': 'www.oliveyoung.co.kr',
        'Pragma': 'no-cache',
        'Referer': 'https://www.oliveyoung.co.kr/store/store/getStoreMain.do',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data['pageIdx'] = intPageNo
    pageString = requests.get(url,params = data, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('li')
    result = []
    for info in tr:
        try:
            name = '올리브영'
            branch = info.find('a').text
            addr = info.find('p',{"class":"addr"}).text
            tell = info.find('div',{"class":"call"}).text
            xcord = info.find('input',{"class":"lng"})['value']
            ycord = info.find('input', {"class": "lat"})['value']
        except:pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()