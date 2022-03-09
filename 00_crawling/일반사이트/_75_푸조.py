import sys
import time
import codecs
import requests
import random
import bs4
import json

def main():

    outfile = codecs.open('75_푸조.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getStoreInfo():
    url = 'https://base.epeugeot.co.kr:506/home/dealers'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ASP.NET_SessionId=45rkhjs4u3pgevux3f1rita3; _ga=GA1.3.171880476.1619154936; _gid=GA1.3.630930614.1619154936; _gat_gtag_UA_34926749_45=1; _ga=GA1.4.171880476.1619154936; _gid=GA1.4.630930614.1619154936; pageviewCount=1; _gat_UA-46336997-1=1; _gat_UA-45190795-1=1; _dc_gtm_UA-46336997-1=1; _dc_gtm_UA-45190795-1=1; _gcl_au=1.1.1079382696.1619154936; _gat_UA-34926749-13=1; pageviewCount=1; _hjTLDTest=1; _hjid=44e67363-3e81-4536-8992-c8eff9c209d9; _hjFirstSeen=1; _psac_gdpr_banner_id=0; _hjAbsoluteSessionInProgress=0; _psac_gdpr_consent_purposes_opposition=; _psac_gdpr_consent_purposes=[cat_ana][cat_com][cat_soc]; _psac_gdpr_consent_cookies=[Google Tag Manager][Google Analytics][AB Tasty][Salesforce Audience Studio (analytics)][Dynamic Yield][Hotjar][IginitionOne (Netmining)][AppNexus][Solocal Xchange][Yahoo][ATG Commerce][Metrigo][MaxPoint][Encore Digital Media][Ozone][OpenX][Glance][Xaxis][Sophus3][Salesforce Audience Studio][Quantcast][Adyoulike][Nextperformance][4w MarketPlace][mPlatform][Bidswitch][Public-Idees][YouTube][Twitter]; _psac_gdpr_consent_given=1',
        'Host': 'base.epeugeot.co.kr:506',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            name = '푸조'
            branch = info.find('td').text
            addr = str(info.select('td')[2]).split(']')[1]
            addr = addr.replace('</td>','').lstrip().rstrip()
            tell = str(info.select('td')[3])
            tell = tell.replace('<td>','').replace('</td>','')
        except:
            pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()