import bs4
import time
import codecs
import requests
import random
from datetime import datetime
import traceback
import os,sys
import json

def getStoreInfo(searchName):
    url = 'https://search.map.kakao.com/mapsearch/map.daum'
    headers = {
        'Referer': 'https://map.kakao.com/', # Referer 헤더값 없으면 호출 요청 에러
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }
    data = {
        'callback': 'jQuery181018657064011065705_1634690332690',
        'msFlag': 'A',
        'sort': '0'
    }
    data['q'] =searchName
    result = []
    try:
        urlopen = requests.get(url ,params = data, headers = headers).text
    except:
        print('Error calling the API')
    try:
        ss = urlopen.replace('/**/jQuery181018657064011065705_1634690332690(','').replace(');','')
        response = json.loads(ss)
    except :
        result.append({'inputName': searchName, 'name': '찾을 수 없음', 'oldaddr': '', 'newaddr': '', 'tell': '', 'cat': '','url': ''})
    data_info = response['place'][0]
    name = data_info['name']
    oldaddr = data_info['address']
    newaddr = data_info['new_address']
    tell = data_info['tel']
    cat = data_info['cate_name_depth1']+'/'+data_info['cate_name_depth2']+'/'+data_info['cate_name_depth3']+'/'+data_info['cate_name_depth4']
    url = data_info['homepage']
    if url == 'https://search.map.daum.net/mapsearch/map.daum' : url = ''
    result.append({'inputName':searchName, 'name':name, 'oldaddr':oldaddr, 'newaddr':newaddr,'tell':tell,'cat':cat,'url':url})
    return result

print(getStoreInfo('서울특별시 금천구 독산로 215, 사아마'))