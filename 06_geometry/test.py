from shapely import wkt
import requests
from pyproj import Proj, transform
import json


proj_UTMK = Proj(init='epsg:5178') # UTM-K(Bassel) 도로명주소 지도 사용 중
proj_WGS84 = Proj(init='epsg:4326') # Wgs84 경도/위도, GPS사용 전지구 좌표
a = 'POINT (924252.7535505547 1931374.344574431)'
a = a.replace('POINT (','').replace(')','').split(' ')
x = a[0]
y = a[1]
x2, y2 = transform(proj_UTMK,proj_WGS84,x,y)
print(x2,y2)
url = 'http://api.vworld.kr/req/address?service=address&request=getAddress&version=2.0&crs=epsg:4326&point={},{}&format=json&type=both&zipcode=true&simple=false&key=3EAB6562-19D4-33E5-920A-66E483DBC133'.format(x2,y2)
response = requests.get(url).text
jsonString = json.loads(response)
result = jsonString['response']['result'][0]['structure']
addr = str(result['level1'] + ' ' + result['level2'] + ' ' + result['level3'] + ' ' + result['level4L']).replace('  ',' ').strip()
print(addr)





# 'result': [{'zipcode': '22013', 'type': 'parcel', 'text': '인천광역시 연수구 송도동 11-104', 'structure': {'level0': '대한민국', 'level1': '인천광역시', 'level2': '연수구', 'level3': '', 'level4L': '송도동', 'level4LC': '2818510600', 'level4A': '송도1동', 'level4AC': '2818582000', 'level5': '11-104', 'detail': ''}}]}}