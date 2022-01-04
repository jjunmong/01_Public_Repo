import sys
import codecs
import requests
import bs4
import random
import time

def main():

    outfile = codecs.open('47_볼보트럭.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")


    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo():
    url = 'https://www.volvotrucks.kr/ko-kr/services/buy_truck.html'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'cache-control': 'no-cache',
        'cookie': 'ACEUCI2=1; ACEUCI2=1; _ga=GA1.2.1103130955.1591346770; ACEUACS=1579483474047131591; 18418=7; _gid=GA1.2.169889402.1592201857; AMCVS_733E579F5579DEDA7F000101%40AdobeOrg=1; AMCV_733E579F5579DEDA7F000101%40AdobeOrg=-408604571%7CMCIDTS%7C18429%7CMCMID%7C73305855525026610900234388235413220366%7CMCAAMLH-1592806657%7C11%7CMCAAMB-1592806657%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1592209057s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0; ACEUCI2=1; s_cc=true; _hjid=a3c82678-a45a-4085-a667-09c4f7a3eae4; _hjIncludedInSample=1; __unam=6dd5e7f-17283a8f26d-333e51fc-12; s_sq=%5B%5BB%5D%5D; AWSALB=GtA65jmrZ5/BDvrmbxke0UXgrFbH/wfsfn2ROzLefnuK0H8udqSh7weSEkXHAblI1uS/xSEqOj1p45yH77IM3WHakNrdabTLP7rjMv/N6UuYMZ7eCAfgmKfsVn9B; AWSALBCORS=GtA65jmrZ5/BDvrmbxke0UXgrFbH/wfsfn2ROzLefnuK0H8udqSh7weSEkXHAblI1uS/xSEqOj1p45yH77IM3WHakNrdabTLP7rjMv/N6UuYMZ7eCAfgmKfsVn9B; 18428=10; _ACU109154=1591346772307131597.1592202020565.2.0.131597PIAQRSY5J0IFZ.0.0.0.....; _ACR0=b8d587918aa66d368da5d55e6d3cd5b0cc7eff41; _ACS109154=87; s_ptc=%5B%5BB%5D%5D; s_ht=1592202020431; s_hc=1%7C2%7C2%7C0%7C2; s_tp=3030; s_ppv=mkt-vtc-kr-ko%2Fservices%2Fbuy_truck%2C60%2C60%2C1812; s_tps=79726; s_pvs=2237; gpv_v9=mkt-vtc-kr-ko%2Fservices%2Fbuy_truck',
        'pragma': 'no-cache',
        'referer': 'https://www.volvotrucks.kr/',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div = bsObj.find_all('ul',{"style":"list-style: none;margin: 0.0px;padding: 0.0px;width: 100.0%;overflow: hidden;font-size: 14.0px;border-bottom-color: rgb(221,221,221);border-bottom-width: 1.0px;border-bottom-style: solid;"})
    result = []
    for info in div:
        name = '볼보트럭'
        branch = info.find('a').text.lstrip().rstrip()
        addr = info.select('li')[4]
        addr = str(addr).split('>')[1]
        addr = addr.replace('</li','')
        tell = info.select('li')[2]
        tell = str(tell).replace('<li style="background: url(/content/dam/volvo/volvo-trucks/markets/korea/training/ta_bg.jpg) no-repeat 100.0% 0.0px;list-style: none;margin: 0.0px;padding: 10.0px 0.0px;width: 15.0%;text-align: center;float: left;">',"").replace('</li>','').replace(')','-')
        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

