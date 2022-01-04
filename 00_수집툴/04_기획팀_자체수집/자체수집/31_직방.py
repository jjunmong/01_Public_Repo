import time
import codecs
import requests
import random
import bs4
import json

def main():
    outfile = codecs.open('31_직방.txt', 'w', 'utf-8')
    dict_keys1 = getStoreInfo()[1]
    dict_keys2 = str(dict_keys1).replace('dict_keys','').replace('[','').replace(']','').replace('(','').replace(')','').replace(',','|').replace("'","").replace(' ','')
    outfile.write("%s\n" % dict_keys2)

    key_list = []
    for key in dict_keys1:
        key_list.append(key)

    store_list = getStoreInfo()[0]
    for store in store_list:
        column_num = 0
        while True:
            if column_num == len(key_list) : break
            elif column_num == len(key_list)-1 :
                outfile.write(u'%s\n' % store[u'%s' % key_list[column_num]])
            else:
                outfile.write(u'%s|' % store[u'%s' % key_list[column_num]])
            column_num +=1
    outfile.close()

def getStoreInfo():
    url = 'https://apis.zigbang.com/v2/danjis?%EC%84%9C%EB%B9%84%EC%8A%A4%EA%B5%AC%EB%B6%84%5B0%5D=%EB%B6%84%EC%96%91%EC%98%88%EC%A0%95&%EC%84%9C%EB%B9%84%EC%8A%A4%EA%B5%AC%EB%B6%84%5B1%5D=%EB%B6%84%EC%96%91%EC%9E%84%EB%B0%95&%EC%84%9C%EB%B9%84%EC%8A%A4%EA%B5%AC%EB%B6%84%5B2%5D=%EC%B2%AD%EC%95%BD%EC%A4%91&%EC%84%9C%EB%B9%84%EC%8A%A4%EA%B5%AC%EB%B6%84%5B3%5D=%EC%B2%AD%EC%95%BD%EB%A7%88%EA%B0%90&%EC%84%9C%EB%B9%84%EC%8A%A4%EA%B5%AC%EB%B6%84%5B4%5D=%EC%9E%85%EC%A3%BC%EC%98%88%EC%A0%95&domain=zigbang&lat_north=39.79528885397302&lat_south=32.61096160838689&lng_east=131.13952988139303&lng_west=122.0636247046892'
    pageString = requests.get(url,stream=True)
    with open('zigbang_raw.txt', 'wb') as fd:
        for chunk in pageString.iter_content(chunk_size=128):
            fd.write(chunk)

    with open('zigbang_raw.txt', 'r', encoding='utf-8') as jsonfile:
        jsonString = json.load(jsonfile)
    data = jsonString['danjis']
    result = []
    dict_key = ''
    for info in data:
        active = str(info['active'])
        address2 = str(info['address2'])
        first_compet = str(info['first_경쟁률'])
        id = str(info['id'])
        lat = str(info['lat'])
        lng = str(info['lng'])
        local1 = str(info['local1'])
        local2 = str(info['local2'])
        local3 = str(info['local3'])
        name = str(info['name'])
        real_type = str(info['real_type'])
        info_text_1 = str(info['view_sources']['info_text_1'])
        info_text_2 = str(info['view_sources']['info_text_2'])
        sub_title_2 = str(info['view_sources']['sub_title_2'])
        try: marker = str(info['view_sources']['분양년월마커'])
        except : marker = ''
        average = str(info['당첨가점평균'])
        aa = str(info['분양년월'])
        bb = str(info['분양일정'])
        cc = str(info['사용승인일'])
        dd = str(info['서비스구분'])
        ee = str(info['아파트추천평균'])
        ff = str(info['총세대수'])
        result_dict = {'active':active,'address2':address2,'first_compet':first_compet,'id':id,'lat':lat,'lng':lng,'local1':local1,'local2':local2,'local3':local3
                       ,'name':name,'real_type':real_type,'info_text_1':info_text_1,'info_text_2':info_text_2,'sub_title_2':sub_title_2,'marker':marker,'average':average,'분양년월':aa
                       ,'분양일정':bb,'사용승인일':cc,'서비스구분':dd,'아파트추천평균':ee,'총세대수':ff}
        dict_key = result_dict.keys()
        result.append(result_dict)
    return result, dict_key

main()