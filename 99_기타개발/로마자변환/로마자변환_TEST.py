import requests
import bs4
import codecs
import sys
import json
import time
import random

def main():

    outfile = codecs.open('12345_RESULT.txt', 'w', 'utf-8')

    inputNames = getInputName()
    for input in inputNames:
        result = getStoreInfo(input)
        print(input)
        for results in result:
            outfile.write(u'%s\n' % results['region'])
        time.sleep(random.uniform(1,1.5))

    outfile.close()

#전체
# def getStoreInfo(inputname):
#     url = 'http://roman.cs.pusan.ac.kr/result_all.aspx?input={}'.format(inputname)
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'Accept-Encoding': 'gzip, deflate',
#         'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'Cookie': '_ga=GA1.3.1961033310.1606812148; _gid=GA1.3.1626239124.1606812148; ASP.NET_SessionId=4wzoa1mxbij30k5z1v2ftxtn; _gat=1',
#         'Host': 'roman.cs.pusan.ac.kr',
#         'Pragma': 'no-cache',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
#     }
#     pageString = requests.get(url, headers = headers).text
#     bsObj = bs4.BeautifulSoup(pageString,"html.parser")
#     result = []
#     try:
#         region = bsObj.find('span',{"id":"outputRMAddr"}).text
#         region = str(region).replace('<span id="outputRMAddr">','').replace('</span>','').replace('<span id="outputMRAddr">','')
#         region = region.rstrip().lstrip().replace('  ','')
#     except :
#         region = inputname + '/' + '수집실패'
#         result.append({'region': region})
#         print(region)
#     else:
#         print(region)
#         result.append({'region':region})
#     return result


# 행정구역 전문
def getStoreInfo(inputname):
    url = 'http://roman.cs.pusan.ac.kr/result_address.aspx?input=%{}'.format(inputname)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.3.1961033310.1606812148; _gid=GA1.3.1626239124.1606812148; ASP.NET_SessionId=4wzoa1mxbij30k5z1v2ftxtn; _gat=1',
        'Host': 'roman.cs.pusan.ac.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://roman.cs.pusan.ac.kr/input.aspx?',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    try:
        region = bsObj.find('span',{"id":"outputRMAddr"}).text
        region = str(region).replace('<span id="outputRMAddr">','').replace('</span>','').replace('<span id="outputMRAddr">','')
        region = region.replace('  ',' ').replace('%','').rstrip().lstrip()
    except :
        region = inputname + '/' + '수집실패'
        result.append({'region': region})
        print(region)
    else:
        print(region)
        result.append({'region':region})
    return result

##일반전문
# def getStoreInfo(inputname):
#     url = 'http://roman.cs.pusan.ac.kr/result_normal.aspx?input=%{}'.format(inputname)
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'Accept-Encoding': 'gzip, deflate',
#         'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'Cookie': '_ga=GA1.3.1961033310.1606812148; _gid=GA1.3.1626239124.1606812148; ASP.NET_SessionId=4wzoa1mxbij30k5z1v2ftxtn; _gat=1',
#         'Host': 'roman.cs.pusan.ac.kr',
#         'Pragma': 'no-cache',
#         'Referer': 'http://roman.cs.pusan.ac.kr/input.aspx?',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
#     }
#     pageString = requests.get(url, headers = headers).text
#     bsObj = bs4.BeautifulSoup(pageString,"html.parser")
#     result = []
#     try:
#         region = bsObj.find('span',{"id":"outputRMNormal"}).text
#         print(region)
#         region = str(region).replace('<span id="outputRMNormal">','').replace('</span>','').replace('<span id="outputMRAddr">','')
#         region = region.replace('  ','').replace('%','').rstrip().lstrip()
#     except :
#         region = inputname + '/' + '수집실패'
#         result.append({'region': region})
#         print(region)
#     else:
#         print(region)
#         result.append({'region':region})
#     return result

def getInputName():
    with open('12345.txt') as data:
        lines2 = data.read().splitlines()
    inputName = lines2
    return inputName

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()