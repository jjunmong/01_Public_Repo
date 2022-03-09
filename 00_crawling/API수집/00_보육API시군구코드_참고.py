import requests
import bs4

def getSidoCode(sidoName):
    url = "http://api.childcare.go.kr/mediate/rest/cpmsapi020/cpmsapi020/request"
    querystring = {"key":"71c59f0ccc3b4b8da812e2db18ca9b56"}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    querystring['arname'] = sidoName
    pageinfo = requests.get(url, params=querystring, headers=headers, timeout = 10).text
    print(url,sidoName)
    soup = bs4.BeautifulSoup(pageinfo,'lxml')
    list = soup.find_all('item')
    data = []
    for info in range(len(list)):
        sidoname = list[info].find('sidoname').text
        sigunname = list[info].find('sigunname').text
        arcode = list[info].find('arcode').text
        # data.append({"sidoname":sidoname,"sigunname":sigunname,"arcode":arcode})
        data.append(arcode)
    return data

def getSidoCode_list():
    sido_list = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시', '광주광역시', '대구광역시', '부산광역시', '세종특별자치시', '제주도']
    result = []
    for sido in sido_list:
        result = result + getSidoCode(sido)
        print(sido, getSidoCode(sido))
    return result

print(getSidoCode_list())
