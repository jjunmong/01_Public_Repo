import requests
import bs4
import codecs
import random
import time

def getStoreInfo():
    url = 'http://www.tmap.co.kr/my_tmap/my_map_tip/map_tip.do'
    header = {
        'Cookie': 'JSESSIONID=3ACDDB682FD82148692F5B57D410B73B.instance01; _ga=GA1.3.258983104.1638772856',
        'Host': 'www.tmap.co.kr',
        'Origin': 'http://www.tmap.co.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://www.tmap.co.kr/my_tmap/my_map_tip/map_tip.do',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    }
    data = {
        'searchKeyword': '서울 주차장',
        'x': '0',
        'y': '0',
        'cpId': '',
    }
    urlopen = requests.post(url, headers = header, data = data).text
    bsObj = bs4.BeautifulSoup(urlopen,"html.parser")
    print(bsObj)

print(getStoreInfo())