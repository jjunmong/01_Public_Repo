#쌩 중복 제거 케이스 75_육쌈냉면 참고


# print(url.status_code)
# print(url.headers['content-type'])
#################################################################
import re

def test():
    s='韓子는 싫고, 한글은 nice하다. English 쵝오 -_-ㅋㅑㅋㅑ ./?!'
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') # 한글과 띄어쓰기를 제외한 모든 글자
  # hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')  # 위와 동일
    result = hangul.sub('', s) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
    print (result)
    result = hangul.findall(s) # 정규식에 일치되는 부분을 리스트 형태로 저장
    print(result)

test()

#################################################################
remove_text = 'asdf(asdf)'

print(re.sub(r'\([^)]*\)', '', remove_text))


# 원하는 정보가 있는 위치 찾기

soup.select('원하는 정보')  # select('원하는 정보') -->  단 하나만 있더라도, 복수 가능한 형태로 되어있음

soup.select('태그명')
soup.select('.클래스명')
soup.select('상위태그명 > 하위태그명 > 하위태그명')
soup.select('상위태그명.클래스명 > 하위태그명.클래스명')    # 바로 아래의(자식) 태그를 선택시에는 > 기호를 사용
soup.select('상위태그명.클래스명 하~위태그명')              # 아래의(자손) 태그를 선택시에는   띄어쓰기 사용
soup.select('상위태그명 > 바로아래태그명 하~위태그명')
soup.select('.클래스명')
soup.select('#아이디명')                  # 태그는 여러개에 사용 가능하나 아이디는 한번만 사용 가능함! ==> 선택하기 좋음
soup.select('태그명.클래스명)
soup.select('#아이디명 > 태그명.클래스명)
soup.select('태그명[속성1=값1]')

../*           : 현재 노드의 부모 노드의 자식 요소 노드를 모두 선택함.

//*            : 현재 문서의 모든 요소 노드를 선택함.

//priority[@*] : 어떠한 종류의 속성 노드라도 적어도 하나 이상 가지고 있는 <priority>요소를 모두 선택함.



from pyproj import Proj, transform
import numpy as np
import pandas  as pd

# Projection 정의
# UTM-K
proj_UTMK = Proj(init='epsg:5178') # UTM-K(Bassel) 도로명주소 지도 사용 중

# WGS1984
proj_WGS84 = Proj(init='epsg:4326') # Wgs84 경도/위도, GPS사용 전지구 좌표

# UTM-K -> WGS84 샘플
x1, y1 = 961114.519726,1727112.269174
x2, y2 = transform(proj_UTMK,proj_WGS84,x1,y1)
print(x2,y2)

# WGS84 -> UTM-K 샘플
x1, y1 = 127.07098392510115, 35.53895289091983
x2, y2 = transform(proj_WGS84, proj_UTMK, x1, y1)
print(x2,y2)

# x, y 컬럼을 이용하여 UTM-K좌표를 WGS84로 변환한 Series데이터 반환
def transform_utmk_to_w84(df):
    return pd.Series(transform(proj_UTMK, proj_WGS84, df['x'], df['y']), index=['x', 'y'])

df_xy = pd.DataFrame([
                                        ['A', 961114.519726,1727112.269174],
                                        ['B', 940934.895125,1685175.196487],
                                        ['C', 1087922.228298,1761958.688262]
                                    ], columns=['id', 'x', 'y'])

df_xy[['x_w84', 'y_w84']] = df_xy.apply(transform_utmk_to_w84, axis=1)

sido_list = ['서울', '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '인천', '대전', '울산', '광주', '대구', '부산', '세종', '제주']
sido_list = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시', '광주광역시', '대구광역시', '부산광역시', '세종특별자치시', '제주특별자치도']
sido_list = ['sido01','sido02','sido03','sido04','sido05','sido06','sido07','sido08','sido09','sido10','sido11','sido12','sido13','sido14','sido15','sido16','sido17']
sidolist = {
    '서울': {'종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구'},
    '광주': {'동구','서구','남구','북구','광산구'},
    '대구': {'중구','동구','서구','남구','북구','수성구','달서구','달성군'},
    '대전': {'동구','중구','서구','유성구','대덕구'},
    '부산': {'중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구','금정구','강서구','연제구','수영구','사상구','기장군'},
    '울산': {'중구','남구','동구','북구','울주군'},
    '인천': {'중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군','남구'},
    '경기': {'수원시','성남시','의정부시','안양시','부천시','광명시','평택시','동두천시','안산시','고양시','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시','용인시','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주군','연천군','가평군','양평군'},
    '강원': {'춘천시','원주시','강릉시','동해시','태백시','속초시','삼척시','홍천군','횡성군','영월군','평창군','정선군','철원군','화천군','양구군','인제군','고성군','양양군'},
    '경남': {'창원시','진주시','통영시','사천시','김해시','밀양시','거제시','양산시','의령군','함안군','창녕군','고성군','남해군','하동군','산청군','함양군','거창군','합천군'},
    '경북': {'포항시','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','군위군','의성군','청송군','영양군','영덕군','청도군','고령군','성주군','칠곡군','예천군','봉화군','울진군','울릉군'},
    '전남': {'목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완도군','진도군','신안군'},
    '전북': {'전주시','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군'},
    '충남': {'천안시','공주시','보령시','아산시','서산시','논산시','계룡시','금산군','연기군','부여군','서천군','청양군','홍성군','예산군','태안군','당진시'},
    '충북': {'청주시','충주시','제천시','청원군','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군'},
    '제주': {'제주시','서귀포시'},
    '세종': {''}
}

sidolist = {
    '서울': {"강남구","강동구","강서구","관악구","광진구","구로구","금천구","노원구","도봉구","마포구","서대문구","서초구","성동구","성북구","송파구","양천구","영등포구","용산구","은평구"},
    '광주': {"광산구","남구","동구","북구","서구"},
    '대구': {'중구','동구','서구','남구','북구','수성구','달서구','달성군'},
    '대전': {'동구','중구','서구','유성구','대덕구'},
    '부산': {"강서구","금정구","기장군","남구","동구","동래구","부산진구","북구","사상구","사하구","서구","수영구","연제구","영도구","중구","해운대구"},
    '울산': {'중구','남구','동구','북구','울주군'},
    '인천': {'중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군','남구'},
    '경기도': {"가평군","고양시","광명시","광주시","구리시","군포시","김포시","남양주시","동두천시","부천시","성남시","수원시","시흥시","안산시","안성시","안양시","양주시","양평군","여주시","연천군","오산시","용인시","의왕시","의정부시","이천시","파주시","평택시","포천시","하남시","화성시"},
    '강원도': {"강릉시","고성군","동해시","삼척시","속초시","양구군","양양군","영월군","원주시","인제군","정선군","철원군","춘천시","태백시","평창군","홍천군","화천군","횡성군"},
    '경상남도': {"거제시","거창군","고성군","김해시","남해군","밀양시","사천시","산청군","양산시","의령군","진주시","창녕군","창원시","통영시","하동군","함안군","함양군","합천군"},
    '경상북도': {"경산시","경주시","고령군","구미시","군위군","김천시","문경시","봉화군","상주시","성주군","안동시","영덕군","영주시","영천시","예천군","울릉군","울진군","의성군","청도군","청송군","칠곡군","포항시"},
    '전라남도': {'목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완도군','진도군','신안군'},
    '전라북도': {'전주시','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군'},
    '충청남도': {'천안시','공주시','보령시','아산시','서산시','논산시','계룡시','금산군','연기군','부여군','서천군','청양군','홍성군','예산군','태안군','당진시'},
    '충청북도': {'청주시','충주시','제천시','청원군','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군'},
    '충북': {'영동군'},
    '제주': {'제주시','서귀포시'},
    '세종': {"금남구즉로","금남면","부강면","소정면","연기면","연동면","장군면","전동면","전의면","조치원읍"}
}

lines_seen = set()  # holds lines already seen
outfile = codecs.open('75_육쌈냉면.txt', 'w', 'utf-8')
for line in codecs.open('75_육쌈냉면2.txt', 'r', 'utf-8'):
    if line not in lines_seen:  # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

os.remove(r'C:\00_업무\00_개발업무\03_매경100프랜_3.x\00_수집툴\75_육쌈냉면2.txt')

for sidoname in sorted(sidolist):
    gugunlist = sidolist[sidoname]
    for gugunname in sorted(gugunlist):
        storeList = getStores(sidoname, gugunname)
        if storeList == None:
            time.sleep(random.uniform(1, 2))
            storeList = getStores(sidoname, gugunname)

for store in range(0, 300, 15):
-------------------------------------------중복제거----------------------------------------------------------------------
    data1 = list(map(dict, set(tuple(sorted(d.items())) for d in data)))  ---순서 무관
    data2 = list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(d.items())) for d in data)))---순서 유지
result = []
def remove_dupe_dicts(l):
  return [dict(t) for t in {tuple(d.items()) for d in l}]

results = [dict(t) for t in {tuple(d.items()) for d in result}] # dict 중복제거

results = list(set(result)) #단일 리스트 중복 제거

results = set()
new_results = []
for list in result:
    lists = tuple(list.items())
    if lists not in results:
        results.add(lists)
        new_results.append(list)
df = 'nmae'
df['email_pad']    = df['email'].str.pad(width=20, side='left', fillchar='_') # 지정길이 패딩
df['email_center'] = df['email'].str.center(width=20, fillchar='_') # 중앙놓고 지정길이 패딩
df['email_ljust']  = df['email'].str.ljust(width=20, fillchar='_')  # 왼쪽놓고 지정길이 패딩
df['email_rjust']  = df['email'].str.rjust(width=20, fillchar='_')  # 오른쪽놓고 지정길이 패딩
df['email_zfill']  = df['email'].str.zfill(width=20)                # 지정길이 0패딩

# split(): 구분자를 기준으로 n개로 나눈다, expand=True이면 여러 컬럼, False이면 1개 컬럼에 리스트
df[['email_split_1', 'email_split_2']] = df['email'].str.split('@', n=1, expand=True)

# partition(): 좌측에 먼저 출현한 구분자포함 3개로 나눈다
df[['email_partition_1', 'email_partition_2', 'email_partition_3']] = df['email'].str.partition(sep='@')

# rpartition(): 우측에 먼저 출현한 구분자포함 3개로 나눈다
df[['email_rpartition_1','email_rpartition_2', 'email_rpartition_3']] = df['email'].str.rpartition(sep='@')

# rsplit(): split와 동일하며 우측부터 탐색하며 n개로 나눈다
df['email_rsplit_1']     = df['email'].str.rsplit(pat='@')

df['email_lower']      = df['email'].str.lower()      # 모두 소문자로 변경
df['email_upper']      = df['email'].str.upper()      # 모두 대문자로 변경
df['email_capitalize'] = df['email'].str.capitalize() # 앞문자 대문자로 변경
df['email_title']      = df['email'].str.title()      # 단위별 앞문자 대문자로 변경
df['email_swapcase']   = df['email'].str.swapcase()   # 소문자는 대문자, 대문자는 소문자로 변경

# 입력 패턴 또는 글자를 대체, 예제에서는 .을 _로 변경
df['email_replace']    = df['email'].str.replace(pat='.', repl='_', regex=False)

df['email_find']    = df['email'].str.find(sub='.')           # 왼쪽부터 sub값 검색후 위치반환
df['email_findall'] = df['email'].str.findall(pat='[a-zA-Z]') # 찾은 모든 값 반환
df['email_rfind']   = df['email'].str.rfind(sub='.')          # 오른쪽부터 sub값 검색후 위치반환
df['email_index']   = df['email'].str.index(sub='.')          # 왼쪽부터 sub값 검색후 위치반환
df['email_rindex']  = df['email'].str.rindex(sub='.')         # 오른쪽부터 sub값 검색후 위치반환

df['email_get']           = df['email'].str.get(i=0)    # 지정 위치값 반환
df['email_slice']         = df['email'].str.slice(start=0, stop=5) # 인덱스 사이 값 반환

# 인덱스 사이 값을 다른 값으로 바꾼 후 값 반환
df['email_slice_replace'] = df['email'].str.slice_replace(start=0, stop=5, repl='?')

df['email_len']   = df['email'].str.len()              # 길이 반환
df['email_count'] = df['email'].str.count(pat='[0-9]') # 문자열 중 패턴에 일치한 수 반환

df['email_isalnum']   = df['email'].str.isalnum()   # 알파벳 또는 숫자로만 구성 여부
df['email_isalpha']   = df['email'].str.isalpha()   # 알파벳으로만 구성 여부
df['email_isdecimal'] = df['email'].str.isdecimal() # 숫자문자로만 구성 여부
df['email_isdigit']   = df['email'].str.isdigit()   # 숫자문자로만 구성 여부
df['email_islower']   = df['email'].str.islower()   # 소문자로만 구성 여부
df['email_isnumeric'] = df['email'].str.isnumeric() # 숫자문자로만 구성 여부
df['email_isspace']   = df['email'].str.isspace()   # 공백(Whitespace)으로만 구성 여부
df['email_istitle']   = df['email'].str.istitle()   # TitleCase형태로 구성 여부
df['email_isupper']   = df['email'].str.isupper()   # 대문자로만 구성 여부

df['email_startswith'] = df['email'].str.startswith(pat='h')     # 좌측값이 입력패턴과 일치 여부
df['email_endswith']   = df['email'].str.endswith(pat='com')     # 우측값이 입력패턴과 일치 여부
df['email_contains']   = df['email'].str.contains(pat='kr', regex=False) # 값 중 패턴포함 여부
df['email_match']      = df['email'].str.match(pat='[a-zA-Z@.]') # 입력패턴과 일치 여부
------------------------------------------------------------------------------------------------------------------------
import sys
import time
import codecs
import requests
import random
import json
import bs4
from selenium import webdriver


def main():
    outfile = codecs.open('30_KDB생명.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo_Basic()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    store_list = dupRemove()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])

    outfile.close()


def getStoreInfo_Basic():
    driver = webdriver.Chrome(r'C:\chromedriver.exe')
    driver.get('https://www.kdblife.co.kr/ajax.do?scrId=HCSCT003M01P')
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    tbody = soup.find('tbody', {"id": "table_grid01"})
    tr = tbody.find_all('tr')
    result = []
    for info in tr:
        try:
            name = "KDB생명 금융프라자"
            branch = info.select('td')[0]
            branch = str(branch).replace('<td class="ta-c" style="border-bottom: 1px solid #e5e5e5;">', '').replace(
                '<td class="ta-c rows" rowspan="5">', '').replace('</td>', '').lstrip().rstrip()
            if branch == '금융프라자':
                branch = '본사'
            addr = info.find('a').text
            tell = info.select('td')[2]
            tell = str(tell).replace('<td class="ta-c" style="border-bottom: 1px solid #e5e5e5;">', '').replace('</td>',
                                                                                                                '').lstrip().rstrip()
            if branch == '본사':
                tell = info.select('td')[3]
                tell = str(tell).replace('<td class="ta-c" style="border-bottom: 1px solid #e5e5e5;">', '').replace(
                    '</td>', '').lstrip().rstrip()
        except:
            pass
        else:
            result.append({"name": name, "branch": branch, "addr": addr, "tell": tell})

    tbody1 = soup.find('tbody', {"id": "table_grid01_01"})
    tr1 = tbody1.find_all('tr')
    for info1 in tr1:
        try:
            name = 'KDB생명 CS BRNACH'
            branch = info1.select('td')[0]
            branch = str(branch).replace('<td class="ta-c">', '').replace('<td class="ta-c rows" rowspan="4">',
                                                                          '').replace('</td>', '').lstrip().rstrip()
            if branch == 'CS Branch':
                branch = '경인'
            addr = info1.find('a').text
            tell = info1.select('td')[2]
            tell = str(tell).replace('<td class="ta-c">', '').replace('</td>', '').lstrip().rstrip()
            if branch == '경인':
                tell = info1.select('td')[3]
                tell = str(tell).replace('<td class="ta-c">', '').replace('</td>', '').lstrip().rstrip()
        except:
            pass
        else:
            result.append({"name": name, "brnach": branch, "addr": addr, "tell": tell})
    return result


def getStoreInfo():
    driver = webdriver.Chrome(r'C:\chromedriver.exe')
    driver.get('https://www.kdblife.co.kr/ajax.do?scrId=HCSCT003M01P')
    time.sleep(3)
    result = []
    for ss in range(10):
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tbody = soup.find('tbody', {"id": "table_grid02"})
        tr = tbody.find_all('tr')
        driver.find_element_by_css_selector('#table_grid_paging > ul > li.next > a').click()
        driver.switch_to.window(driver.window_handles[-1])
        for info in tr:
            name = 'KDB생명'
            branch = info.select('td')[0]
            branch = str(branch).replace('<td class="ta-c">', '').replace('</td>', '').lstrip().rstrip()
            addr = info.find('a').text
            tell = info.select('td')[2]
            tell = str(tell).replace('<td class="ta-c">', '').replace('</td>', '').lstrip().rstrip()
            result.append({"name": name, "branch": branch, "addr": addr, "tell": tell})
        time.sleep(2)

    return result

def dupRemove():
    result = getStoreInfo()
    results = set()
    new_results = []
    for list in result:
        lists = tuple(list.items())
        if lists not in results:
            results.add(lists)
            new_results.append(list)
    return new_results


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
--------------------------------------------------------------------------------
jsonData = requests.post(url, data=data).text
    pageString = json.loads(jsonData)
    stringConvert4 = pageString['script']
    stringConvert3 = str(stringConvert4)
    stringConvert2 = stringConvert3.replace('"','').replace('</div>','').replace('</li>','').replace('</span>','')\
        .replace('\t','').replace('setMapPoint','').replace(";var locPosition = new daum.maps.LatLng(37.51625134859292, 127.10300624653243);map.setCenter(locPosition);","")\
    .replace("map.setCenter(locPosition);","").replace('\n','').replace(',','|').replace('(','').replace(')','')
    stringConvert = stringConvert2.split(';')

for sido_name in sorted(sidolist):
    gugunlist = sidolist[sido_name]
    for gugun_name in sorted(gugunlist):

        page = 1
        retry_count = 0
        while True:
            store_list = getStores(gugun_name, page)
            if store_list == None:
                if retry_count >= 7:
                    print('critical error!')
                    break
                else:
                    time.sleep(random.uniform(1, 2))
                    retry_count += 1;
                    continue

            retry_count = 0

import requests
import bs4
import json


form = {
        'board_code': 'b2017041258ed25b8503c5',
        'search':'',
        'search_mod': 'all',
        # 'page': '3',
        'sort': 'TIME'
}
form['page']=  "1"
res = requests.post('http://dailybeer.co.kr/ajax/get_map_list.cm', form)
son_string = requests.get().text
data_list = json.loads()

import pyautogui
import time

# 모니터 사이즈 세로 크기 구하고 변수에 지정
backWidth, backHeight = pyautogui.size()
time.sleep((5))
# 마우스의 현재 위치 출력(While 문과 함께 쓰면 실시간으로 좌표 확인 가능)
mousePositionX, mousePositionY = pyautogui.position()
print(mousePositionX,mousePositionY)
time.sleep((5))
# # 마우스 이동
# pyautogui.moveTo(200,150)
# time.sleep((5))
# # 마우스 클릭
pyautogui.click(button='right')
time.sleep((5))
# # 마우스 현재 위치에서 이동
# pyautogui.moveRel(100, 100)
# time.sleep((5))
# # 마우스 더블 클릭
# pyautogui.doubleClick()
# time.sleep((5))
# # 마우스를 해당 지점까지 서서히 이동
# pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad)
# time.sleep((5))
# # 타자로 텍스트를 입력
# pyautogui.typewrite('Hello world! This is my world', interval=0.01)
# time.sleep((5))
# esc를 누른다.
# pyautogui.press('esc')
# time.sleep((5))
# # Shift를 누른다.
# pyautogui.keyDown('shift')
# time.sleep((5))
# Shift를 손에서 뗀다
# pyautogui.keyUp('shift')
# time.sleep((5))
# # Left를 누른다.
# pyautogui.press(['left', 'left'])
# time.sleep((5))
# ctrl, s 동시 입력
# pyautogui.hotkey('ctrl', 's')
# time.sleep((5))
# for ss in range(0,30):
#     # 스크롤 제일 마지막 아래 대상 선택
#     ELEMENT = driver.find_elements_by_css_selector('body > section > section > section > article > div:nth-child(2) > div.location-search > ul > li:nth-child(16)')[-1]
#     # ELEMENT 가 화면에 보이도록 스크롤 조정 --> 아래 부분 추가로 확장됨
#     driver.execute_script("arguments[0].scrollIntoView(true);", ELEMENT);

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd

root = tk.Tk()

canvas1 = tk.Canvas(root, width=300, height=300, bg='lightsteelblue2', relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='File Conversion Tool', bg='lightsteelblue2')
label1.config(font=('helvetica', 20))
canvas1.create_window(150, 60, window=label1)


def getTxt():
    global read_file

    import_file_path = filedialog.askopenfilename()
    read_file = pd.read_csv(import_file_path, encoding = 'EUC-KR')


browseButtonTxt = tk.Button(text="      Import Text File     ", command=getTxt, bg='green', fg='white',
                            font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 130, window=browseButtonTxt)


def convertToCsv():
    global read_file

    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    read_file.to_csv(export_file_path, index=None)


saveAsButtonCsv = tk.Button(text='Convert Text to CSV', command=convertToCsv, bg='green', fg='white',
                            font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 180, window=saveAsButtonCsv)


def exitApplication():
    MsgBox = tk.messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application',
                                       icon='warning')
    if MsgBox == 'yes':
        root.destroy()


exitButton = tk.Button(root, text='       Exit Application     ', command=exitApplication, bg='brown', fg='white',
                       font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 230, window=exitButton)

root.mainloop()

########################################################################################################################
import sys
import time
import codecs
import requests
import random
import bs4
from selenium import webdriver
import json
import csv

def getStoreList(intPageNo):
    url = 'https://www.car1023.com/board/list.php?page={}&bdId=position'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            a = str(info.find('a')['href']).split(',')[1].replace(' ','')
        except:pass
        else:
            result.append(a)
    return result

for ss in getStoreList(1):
    print(ss)

def getStorePageNo(intPageNo):
    url = 'https://www.car1023.com/board/list.php?page={}&bdId=position'.format(intPageNo)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all('tr')
    result = []
    for info in tr:
        try:
            a = str(info.find('a')['href']).split(',')[1].replace(' ','')
        except:pass
        else:
            result.append(a)
    return result

for ss in getStorePageNo(167):
    print(ss)

########################################################################################################################

import pandas as pd

read_file = pd.read_csv (r'C:\00_업무\00_개발업무\03_매경100프랜_3.x\00_수집툴\133_골프존마켓.txt')
read_file.to_csv (r'C:\00_업무\00_개발업무\03_매경100프랜_3.x\00_수집툴\133_골프존마켓.csv', index=None, encoding='EUC-KR')


########################################################################################################################

def compare_excel(old_xlsx, new_xlsx, column_name):
    import pandas as pd

    df_old = pd.read_excel(old_xlsx)
    df_new = pd.read_excel(new_xlsx)

    # 불러온 데이터의 버전 구분
    df_old['ver'] = 'old'
    df_new['ver'] = 'new'

    id_dropped = set(df_old[column_name]) - set(df_new[column_name])
    id_added = set(df_new[column_name]) - set(df_old[column_name])

    # 삭제된 데이터
    df_dropped = df_old[df_old[column_name].isin(id_dropped)].iloc[:, :-1]
    # 추가된 데이터
    df_added = df_new[df_new[column_name].isin(id_added)].iloc[:, :-1]

    df_concatted = pd.concat([df_old, df_new], ignore_index=True)
    changes = df_concatted.drop_duplicates(df_concatted.columns[:-1], keep='last')
    duplicated_list = changes[changes[column_name].duplicated()][column_name].to_list()
    df_changed = changes[changes[column_name].isin(duplicated_list)]

    df_changed_old = df_changed[df_changed['ver'] == 'old'].iloc[:, :-1]
    df_changed_old.sort_values(by=column_name, inplace=True)

    df_changed_new = df_changed[df_changed['ver'] == 'new'].iloc[:, :-1]
    df_changed_new.sort_values(by=column_name, inplace=True)

    # 정보가 변경된 데이터 정리
    df_info_changed = df_changed_old.copy()
    for i in range(len(df_changed_new.index)):
        for j in range(len(df_changed_new.columns)):
            if (df_changed_new.iloc[i, j] != df_changed_old.iloc[i, j]):
                df_info_changed.iloc[i, j] = str(df_changed_old.iloc[i, j]) + " ==> " + str(df_changed_new.iloc[i, j])

    # 엑셀 저장
    with pd.ExcelWriter('compared_result.xlsx') as writer:
        df_info_changed.to_excel(writer, sheet_name='info changed', index=False)
        df_added.to_excel(writer, sheet_name='added', index=False)
        df_dropped.to_excel(writer, sheet_name='dropped', index=False)

#######################################################################################################
#CSV로 변환
import csv
txt_file = r"133_골프존마켓.txt"
csv_file = r"133_골프존마켓.csv"
in_txt = csv.reader(open(txt_file, "r", encoding='UTF-8'), delimiter = '|')
out_csv = csv.writer(open(csv_file, 'w'))
out_csv.writerows(in_txt)

#엑셀로 변환
import pandas as pd

df = pd.DataFrame(pd.read_csv('133_골프존마켓.txt',sep='|'))
print(df)
df.to_excel('133_골프존마켓.xlsx',index=False)


# url 코드 디코딩
import urllib.parse
pageString = requests.post(url, data=data).text
pageString = urllib.parse.unquote(pageString)
jsonString = json.loads(pageString)
entityList = jsonString['_msg_']['_body_']['GRID00']

for url in url_list:
    store_list = getStoreInfo(url['col1'], url['no'])
    print(url['col1'], url['no'])

#requests 의 data 셋이 리스트 안의 리스트 인경우
    data={}
    data['mbw_json'] = '{"areanum":"'+str(intPageNo)+'","gubun":"1","flag":"card"}'


requests.post(url, data=json.dumps(data))

#20개씩 끊어서 저장하기.

def getStore_list():
    n = 20
    alllist = getStore_id_all()
    alllist2 = [alllist[i * n:(i + 1) * n] for i in range((len(alllist) + n - 1) // n )]
    for num in range(len(alllist2)):
        tv_list = alllist2[num]
        filename = str(num)+'_'+'daum_tv_list.text'
        outfile = codecs.open(filename,'a')
        for list in tv_list:
            list_id = str(list)+'\n'
            outfile.write(list_id)
        outfile.close()


import requests
from scrapy import Selector
from random import choice
from requests.exceptions import ProxyError, SSLError, ConnectTimeout
from random import choice

def get_proxy_list():
    proxy_url = "https://free-proxy-list.net/"

    resp = requests.get(proxy_url)
    sel = Selector(resp)
    tr_list = sel.xpath('//*[@id="proxylisttable"]/tbody/tr')

    proxy_server_list = []

    for tr in tr_list:
        ip = tr.xpath("td[1]/text()").extract_first()
        port = tr.xpath("td[2]/text()").extract_first()
        https = tr.xpath("td[7]/text()").extract_first()

        if https == "yes":
            server = f"{ip}:{port}"
            proxy_server_list.append(server)


    return proxy_server_list


def getStoreInfo(ID, proxy):
    result = []
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    url = 'https://place.map.kakao.com/main/v/{}?_=1620092986015'.format(ID)
    pageString = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}).text
    jsonData = json.loads(pageString)
    basicinfo = jsonData['basicInfo']
    name = basicinfo["placenamefull"]


def dup_remove():
    w = open('심평원_약국_중복제거.txt', 'w')
    r = open('심평원_약국.txt', 'r',encoding='UTF8')
    # 파일에서 읽은 라인들을 리스트로 읽어들임
    lines = r.readlines()
    # Set에 넣어서 중복 제거 후 다시 리스트 변환
    lines = list(set(lines))
    # 리스트 정렬
    # 정렬,중복제거한 리스트 파일 쓰기
    w.write("YADNM|ADDR|CLCD|EMDONGNM|ESTBDD|GDRCNT|INTNCNT|POSTNO|RESDNTNCT|SDRCNT|SGGUCD|SGGUCDNM|SIDOCD|SIDOCDNM|TELNO|XPOS|YPOS|YKIHO\n")
    for line in lines:
        w.write(line)
    # 파일 닫기
    w.close()
    r.close()
    # os.remove('DAUM_TV맛집_간편수집결과.txt')