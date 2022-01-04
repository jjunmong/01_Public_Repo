import requests
import bs4
import json
import codecs
####### 20년 10월 기점으로 우수 중소기업 DB제공 중단.
outfile = codecs.open('06_우수중소.txt', 'w', 'utf-8')
outfile.write("##NAME|ADDR\n")

def getInfo(sidoList,pageNo):
    url = "http://sminfo.mss.go.kr/gc/ei/GEI002R0.do"
    data ={
    'mode': '',
    'kedcd': '',
    'cmMenuId': '441010200',
    'clickcontrol': 'disable',
    'locSrchCd': '2',
    'sidoCd': '01',
    'gugunCd': '',
    'gugunNm': '',
    'gugunNm2': '',
    'cmQueryOption': '07',
    'cmTotalRowCount': '0',
    'cmPageNo': '1',
    'cmSortField': '',
    'cmSortOption': '0',
    'tITLESortOption': '2',
    'bZNOSortOption': '2',
    'returnUrl': '',
    'returnCmMenuId': '',
    'iqFlag': 'S',
    'cmRowCountPerPage': '50'
    }
    data['sidoNm'] = sidoList
    data['cmQuery'] = sidoList
    data['cmPageNo'] =pageNo
    res = requests.post(url, data =data).text
    bsObj = bs4.BeautifulSoup(res,'html.parser')
    re = bsObj.find_all('tr')
    dataAll = []
    for ss in re:
        try:
            name = ss.find("a").text.rstrip().lstrip()
            addr = ss.find("p").text.rstrip().lstrip()
        except AttributeError:
            pass
        else:
            dataAll.append({"name":name,"addr":addr})
    return dataAll

sido_list = ["서울","부산","대구","인천","광주","대전","울산","강원","경기","충북","충남","전북","전남","경북","경남","제주","세종"]

result = []
for get in sido_list:
    for number in range(1, 100):
        result = result + getInfo(get, number)
        print(get, number)

for ssd in result:
    print(ssd)

for results in result:
    outfile.write(u'%s|' % results['name'])
    outfile.write(u'%s|\n' % results['addr'])
outfile.close()