import bs4
import time
import codecs
import requests
import random
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\02_2_테슬라전기차\\') == False : os.makedirs('수집결과\\02_2_테슬라전기차\\')
outfilename = '수집결과\\02_2_테슬라전기차\\02_2_테슬라전기차{}.txt'.format(today)
outfilename_true = '수집결과\\02_2_테슬라전기차\\02_2_테슬라전기차{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\02_2_테슬라전기차\\02_2_테슬라전기차{}.log_실패.txt'.format(today)

def main():
    try:
        Crawl_run()
        outfile = codecs.open(outfilename_true, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '정상 수집 완료'
        outfile.write(write_text)
        outfile.close()
    except:
        if os.path.isfile(outfilename_true):
            os.remove(outfilename_true)
        outfile = codecs.open(outfilename_false, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '수집 실패' + '|' + str(traceback.format_exc())
        outfile.write(write_text)
        outfile.close()

def Crawl_run():
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("BRANCH|ADDR|TELL|CHARGER\n")

    idx_list = getSuperchagersIdx()
    for ss in idx_list:
        print(ss)
    for idx in idx_list:
        store_List = getSuperchagersInfo(idx)
        for store in store_List:
            outfile.write(u'%s|' % store['branch'])

            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['charger'])
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

    outfile = codecs.open(outfilename, 'a', 'utf-8')

    idx_list = getSuperchagersIdx2()
    for ss in idx_list:
        print(ss)
    for idx in idx_list:
        store_List = getSuperchagersInfo2(idx)
        for store in store_List:
            if store['branch'] =='서울 – 강서 수퍼 차저' : pass
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['charger'])

    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getSuperchagersIdx():
    url = 'https://www.tesla.com/ko_KR/findus/list/superchargers/South+Korea'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'buy_flow_locale=ko_KR; ip_lookup_desired_locale=ko_KR; _ga=GA1.2.735327592.1582782185; _gid=GA1.2.601575519.1582782185; _svsid=8709ac2a05144cb3c8a06239dd393797; has_js=1; _gali=find-us-list-container; RT="z=1&dm=tesla.com&si=ykl5h0vivae&ss=k75jwh9q&sl=0&tt=0&bcn=https%3A%2F%2Frumcollector.teslamotors.com%2Fbeacon&r=https%3A%2F%2Fwww.tesla.com%2Fko_KR%2Ffindus%2Flist%2Fsuperchargers%2FSouth%2BKorea&ul=1582868375534"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    }
    pageinfo = requests.get(url, headers = headers).text
    time.sleep(1)
    bsObj = bs4.BeautifulSoup(pageinfo,"html.parser")
    section = bsObj.find('div',{"class":"state"})
    urls = section.find_all('a')
    result =[]
    for info in urls:
        aname = info['href']
        aname2 = aname.split('/')
        aname3 = str(aname2[5:6]).replace('[','').replace(']','').replace("'","")
        result.append(aname3)
    return result

def getSuperchagersInfo(name):
    url = 'https://www.tesla.com/ko_KR/findus/location/supercharger/{}'.format(name)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'buy_flow_locale=ko_KR; ip_lookup_desired_locale=ko_KR; _ga=GA1.2.735327592.1582782185; _svsid=8709ac2a05144cb3c8a06239dd393797; AKA_A2=A; ak_bmsc=5DEEC470BD3954C29EB27EAA9BDB33E648F66751F06400001C585C5E56D6DA61~pl08jKMmY1GduCbtXRUr5+a2IkvG+uCSe5vhBPKfJeq61k5QxWtK0I/DKtJ2TQL7WZSdskmO9dh7HHQ2C6taKiX1KDpYZBag+ueTitY9pbkEY9WP74agm7Ugjp7YUML6+mfrL+GTZVaKqqW4s1q54v4sJ6AO5DNesA5eBGPtby6JU1RqeOEWbAsn6dwhkxWOUFa8lueo5dFDCvLnBUEinCGp4y8LzGBPapKdiOZnnXPNU=; has_js=1; _gid=GA1.2.1463759728.1583110174; ip_info={"ip":"112.169.33.67","location":{"latitude":37.4906,"longitude":127.02},"city":"Seocho","state":"Seoul","state_code":"11","postal":"null","country":"Republic of Korea","country_code":"KR","isStoreIP":false}; bm_sv=7878B8F425918FCF018A3C7C2894EF20~jvtDsvHLAZJMExOVHhyMlRHFG44EhYNE+dyS39ae32NS4vaRRO6rKLjn7Y5y5NpN/l88K0W9O5OSCaNMRqt+tWts6JZm1Y4v4xhVKou0jwVfMVSaxqOgeOxqPejFwBmJW+sz51IZQHLcZC0aReAkPHs0eFHqcj2eSKC7aROoWWk=; _gat_UA-9152935-1=1; RT="r=https%3A%2F%2Fwww.tesla.com%2Fko_KR%2Ffindus%2Flocation%2Fsupercharger%2Fgoyangsupercharger&ul=1583111502461"',
        'referer': 'https://www.tesla.com/ko_KR/findus/list/superchargers/South%20Korea',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    }
    pageinfo = requests.get(url, headers = headers).text
    print(url)
    result = []
    try:
        bsObj = bs4.BeautifulSoup(pageinfo,"html.parser")
        time.sleep(1)
        div = bsObj.find('div',{"class":"panel-panel"})
        result = []
        branch = div.find('h1').text
        addr = div.find('span',{"class":"street-address"}).text
        tell = div.find('span',{"class":"value"}).text
        charger2 = div.select('p')[1]
        charger= str(charger2).replace('<p><strong>충전</strong><br/>','').replace('<br/>',',').replace('</p>','')
    except AttributeError:
        pass
    else:
        result.append({"branch":branch,"addr":addr,"tell":tell,"charger":charger})
    return result

def getSuperchagersIdx2():
    url = 'https://www.tesla.com/ko_KR/findus/list/chargers/South+Korea'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'cookie': 'buy_flow_locale=ko_KR; ip_lookup_desired_locale=ko_KR; _ga=GA1.2.735327592.1582782185; _svsid=8709ac2a05144cb3c8a06239dd393797; _gid=GA1.2.1463759728.1583110174; AKA_A2=A; ak_bmsc=1E56AB7A79AFE188E999C32437281D97173B97368A3A0000D68B5C5E885B6D25~plKyGSWHV+f3NSHnbBX/zuo8ENERnVBCWTlYHzm7ds1LgLpjLRsm7XsrxjO83oiqL6JJ9ot36MokGUV8122FDULeah1pUHQGlEfJO+abmEOTjDe3zNT7FDaqlwdgyu6AQREjX9v+WxWxgumDOU0HX/mtjq2jxKalce8jAQhyvUkT+cmeNs6zYjEmeblZLP/yC9fCb1XYrxXReApEHLbm4yEIfKOXOZm7urxuGbo1uVZlU=; has_js=1; ip_info={"ip":"112.169.33.67","location":{"latitude":37.4906,"longitude":127.02},"city":"Seocho","state":"Seoul","state_code":"11","postal":"null","country":"Republic of Korea","country_code":"KR","isStoreIP":false}; BIGipServer~DMZ_WWW_PRD~ORIGIN-DMZ-WWW-HTTP=!sw400Y5cZBGru0+zYsqf4wyzAMl/Hob+lbAtWrWj9dhDGoqpB62j67rFZVzrMUI7XNEHblCKcbVFGA==; bm_sv=48D96C5E7EA6FB3892725F0757C6498A~YkRyVFdP9cSrAPudAXh6e46P7mpA+sPNY5Gg9yFd4MJSsUsA4/VS9qJQozmjxPK9ByEdNfSgIPkXYZ8POtz6LlLaEWzhrz/B3AlOYYPfptHCydYbahrwfxaNcv5O4lYvoNe8s8Caies6+KwS5U1Z+hPl4OCZzt8y2eDIZMj6wvE=; RT="r=https%3A%2F%2Fwww.tesla.com%2Fko_KR%2Ffindus%2Flocation%2Fcharger%2Fdc28872&ul=1583125115108"',
        'referer': 'https://www.tesla.com/ko_KR/findus/list',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    }
    pageinfo = requests.get(url, headers = headers).text
    time.sleep(1)
    bsObj = bs4.BeautifulSoup(pageinfo,"html.parser")
    section = bsObj.find('div',{"class":"state"})
    urls = section.find_all('a')
    result =[]
    for info in urls:
        aname = info['href']
        aname2 = aname.split('/')
        aname3 = str(aname2[5:6]).replace('[','').replace(']','').replace("'","")
        if aname3 == 'seoulgangseosupercharger' : pass
        else:
            result.append(aname3)
    return result

def getSuperchagersInfo2(name):
    url = 'https://www.tesla.com/ko_KR/findus/location/charger/{}'.format(name)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'buy_flow_locale=ko_KR; ip_lookup_desired_locale=ko_KR; _ga=GA1.2.735327592.1582782185; _svsid=8709ac2a05144cb3c8a06239dd393797; _gid=GA1.2.1463759728.1583110174; AKA_A2=A; ak_bmsc=1E56AB7A79AFE188E999C32437281D97173B97368A3A0000D68B5C5E885B6D25~plKyGSWHV+f3NSHnbBX/zuo8ENERnVBCWTlYHzm7ds1LgLpjLRsm7XsrxjO83oiqL6JJ9ot36MokGUV8122FDULeah1pUHQGlEfJO+abmEOTjDe3zNT7FDaqlwdgyu6AQREjX9v+WxWxgumDOU0HX/mtjq2jxKalce8jAQhyvUkT+cmeNs6zYjEmeblZLP/yC9fCb1XYrxXReApEHLbm4yEIfKOXOZm7urxuGbo1uVZlU=; has_js=1; ip_info={"ip":"112.169.33.67","location":{"latitude":37.4906,"longitude":127.02},"city":"Seocho","state":"Seoul","state_code":"11","postal":"null","country":"Republic of Korea","country_code":"KR","isStoreIP":false}; BIGipServer~DMZ_WWW_PRD~ORIGIN-DMZ-WWW-HTTP=!sw400Y5cZBGru0+zYsqf4wyzAMl/Hob+lbAtWrWj9dhDGoqpB62j67rFZVzrMUI7XNEHblCKcbVFGA==; bm_sv=48D96C5E7EA6FB3892725F0757C6498A~YkRyVFdP9cSrAPudAXh6e46P7mpA+sPNY5Gg9yFd4MJSsUsA4/VS9qJQozmjxPK9ByEdNfSgIPkXYZ8POtz6LlLaEWzhrz/B3AlOYYPfptEdXgd4LARnN6W5CBbYZmvE5q6kgOrBbqjREDcNuWhaA2Y7Okf+Xa/nDWEiKMFrvSA=; _gat_UA-9152935-1=1; _gali=find-us-list-container; RT="r=https%3A%2F%2Fwww.tesla.com%2Fko_KR%2Ffindus%2Flocation%2Fcharger%2Fdc27207&ul=1583125688256"',
        'referer': 'https://www.tesla.com/ko_KR/findus/list/chargers/South+Korea',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    }

    pageinfo = requests.get(url, headers = headers).text
    time.sleep(1)
    print(url)
    result = []
    try:
        bsObj = bs4.BeautifulSoup(pageinfo,"html.parser")
        div = bsObj.find('div',{"class":"panel-pane pane-page-content"})
        branch = div.find('h1').text
        addr = div.find('span',{"class":"street-address"}).text
        tell = div.find('span',{"class":"value"}).text.replace(') ','-').replace('+82-','0')
        charger2 = div.select('p')
        charger = str(charger2).split('<br/>')[1]
    except AttributeError:
        pass
    else:
        result.append({"branch":branch,"addr":addr,"tell":tell,"charger":charger})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()