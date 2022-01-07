import time
import codecs
import requests
import random
import json
from datetime import datetime
def main():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\GS칼텍스_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TRUCK\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list == None: break
        print(page)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['truck'])
        page += 1

        time.sleep(random.uniform(2,3))

    outfile.close()
    print('수집종료')
def getStoreInfo(intPageNo):
    url = "https://www.kixx.co.kr/api/kixxStory/fillingStationFind".format(intPageNo)
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko,en;q=0.9,ko-KR;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "97",
        "Content-Type": "application/json",
        "Cookie": "XTVID=A200921092243172193; xloc=1920X1080; LOGINSEQ=8803659; XTVID=A200921092243172193",
        "Host": "www.kixx.co.kr",
        "Origin": "https://www.kixx.co.kr",
        "Pragma": "no-cache",
        "Referer": "https://www.kixx.co.kr/refuel/station",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    }
    data ={
        # "pageIdx": "3",
        "pageSize": "10",
        "srcFrchDtlDivCd": "0008,0005",
        "srcFrchNm": "",
        "srcZipAddr": "",
    }
    data["pageIdx"] = intPageNo
    try:
        pageString = requests.post(url = url, data = json.dumps(data), headers = headers).text
        jsonString = json.loads(pageString)
        entitylist = jsonString['result']['fillingStationList']
    except: return None
    result = []
    for info in entitylist:
        try:
            name = 'GS칼텍스'
            branch = info['frchnm']
            addr = info['zipaddr']+ ' '+ info['dtladdr']
            tell = info['tphnno']
            truck = '화물특화주유소'
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'truck':truck})
    results = [dict(t) for t in {tuple(d.items()) for d in result}]
    return results

main()