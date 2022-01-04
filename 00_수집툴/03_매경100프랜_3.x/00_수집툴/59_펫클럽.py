import sys
import time
import codecs
import requests
import random
import json
import bs4


def main():

    outfile = codecs.open('59_펫클럽.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|TIME\n")

    page = 1
    while True:
        storeList = getStoreInfo(page)
        if storeList == [] : break
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['time'])
        page += 1
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo(page):
    url = 'http://petclubhome.co.kr/product/list.html'
    params = {
        'cate_no': '1150',
        # 'page': '2',
    }
    params['page'] = page
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'ECSESSID=9c609708eaff6ec2d182bf0b58e1c68c; atl_epcheck=1; atl_option=1%2C1%2CH; CUK45=cuk45_okidog_9c609708eaff6ec2d182bf0b58e1c68c; CUK2Y=cuk2y_okidog_9c609708eaff6ec2d182bf0b58e1c68c; CID=CIDc9bb6dacb8737adaedc84917f8338169; CIDc9bb6dacb8737adaedc84917f8338169=5723dcba1601f168c29a543b5f02e4bd%3A%3A%3A%3A%3A%3Ahttp%3A%2F%2Fpetclub.co.kr%2F%3A%3A%3A%3A4%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%2Fabout%2Fmain_03.html%3A%3A1583999525%3A%3A%3A%3Appdp%3A%3A1583999525%3A%3A%3A%3A%3A%3A%3A%3A; vt=1583999620',
        'Host': 'petclubhome.co.kr',
        'Referer': 'http://petclubhome.co.kr/product/list.html?cate_no=1150',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    }
    pageString = requests.get(url , params = params, headers = headers).text
    baObj = bs4.BeautifulSoup(pageString,"html.parser")
    prdList = baObj.find('ul',{"class":"prdList"})
    result = []
    try:
        entityList = prdList.find_all('li')
        print(page , url)

        for info in entityList:
            name = info.find('span').text.replace(' ','|')
            addr = info.find('dt',{"class":"story"}).text
            time = info.find('dt',{"class":"story1"}).text
            time = str(time).replace('영업시간 : ','').replace('★ ','')
            print(time)
            tell = info.find('dt',{"class":"story2"}).text
            tell = str(tell).replace('연락처 : ','')
            print(tell)
            result.append({"name":name,"addr":addr,"tell":tell,"time":time})
    except:
        pass

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()