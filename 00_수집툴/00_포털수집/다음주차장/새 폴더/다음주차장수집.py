import time
import requests
import random
import json
import codecs

def getStore_id(intpageNo, sido, searchName):
    url = 'https://search.map.kakao.com/mapsearch/map.daum'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'kuid=388435622479527939; webid=8ae47d432fab4843a239ac151cb09122; TIARA=7l--Mxafxr1qZZDRCrsYov66a6iKwhXVp2gnGlEfWaecua4zlmNfiuBn3Bi8oczn6-8Iyv5JhGTlP8MTfo5Yud_TSrFz--qg8VNeJBAR3jM0; webid_ts=1579228279841; _kadu=-LU_BtUeFmy-jlqA_1616466578120; _ga=GA1.2.1523905731.1622520787; _gcl_au=1.1.206440758.1632369937; __T_=1; _T_ANO=a+Huprfu7a8gpnTaGUxJPHROX4cB9GJrQrXi7Uag8D/V2Q4WDWJhdtbKzWcCKamUFy+nxVlzL3r7azueNxInahrZFqDa3jVAGOxwgVOoNzBHEsKNs7H1wsT16Sh/djlzgCsAQ+5EXSwPVfndbrdSKE/5vOm2TTDcJROumuA1HyUJEeGZ9+1DAPNIjdLQX6TVq6aAIRzLPujFv/4ekaZL0q0ltijLteCMnQ98WsPfrbBwOW6JD/MZMcpF2aMLjg5gK0E1qLe3hEPTBPsrgsD/5+amU0N6APP8K5mY9ciz2ynHRPHJpeXX4ZAuieOWFpRYKJch9YiJALfdCnHuio2BEw==',
        'Referer': 'https://map.kakao.com/',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }
    data = {
        'callback': 'jQuery181018657064011065705_1634690332690',
        'msFlag': 'A',
        'sort': '0'
    }
    data['page'] = intpageNo
    data['q'] = sido + searchName
    try:
        urlopen = requests.get(url ,params = data, headers = headers).text
    except:
        print('Error calling the API')
    ss = urlopen.replace('/**/jQuery181018657064011065705_1634690332690(','').replace(');','')
    response = json.loads(ss)
    place = response['place']
    data =[]
    for list in place:
        id = str(list['confirmid'])
        try: cordx = str(list['lon'])
        except : cordx = ''
        try : cordy = str(list['lat'])
        except : cordy = ''
        text_all = str(id+'|'+cordx+'|'+cordy)

        data.append(text_all)
    return data

def getSidoName():
    with open('sidolist_dong33.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    return SearchList

def getStore_id_all():
    result = []
    sidolist = getSidoName()
    for sido in sidolist:
        page = 1
        while True:
            result  = result + getStore_id(page, sido, '공영주차장')
            print(sido, page)
            page+=1
            if len(getStore_id(page, sido, '공영주차장')) < 15 :
                result = result + getStore_id(page, sido, '공영주차장')
                break
            time.sleep(random.uniform(0.9, 1.2))
    return result

def getStore_list():
    alllist = getStore_id_all()
    outfile_tv = codecs.open('ID_list.txt', 'w')
    for lists in alllist:
        tv_list = str(lists) + '\n'
        outfile_tv.write(tv_list)
    outfile_tv.close()

def list_dup_remove():
    w = open('ID_list_중복제거.txt', 'w')
    r = open('ID_list.txt', 'r',encoding='UTF8')
    # 파일에서 읽은 라인들을 리스트로 읽어들임
    lines = r.readlines()
    # Set에 넣어서 중복 제거 후 다시 리스트 변환
    lines = list(set(lines))
    # 리스트 정렬
    # 정렬,중복제거한 리스트 파일 쓰기
    for line in lines:
        w.write(line)
    # 파일 닫기
    w.close()
    r.close()
#####################################################################################
def daum_save():
    outfile = codecs.open('parkingLot.txt', 'a', 'utf-8')
    outfile.write("ID|NAME|CAT|NEWADDR|OLDADDR|XX|YY|TELL|업데이트날짜|모두_운영시간|모두_현장요금|모두_URL|카카오_주차면수|카카오_결제방법|카카오_운영시간|카카오_현장요금\n")
    with open('ID_list_중복제거.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    id_list = SearchList
    count = 1
    for id in id_list:
        store_list_id = id.split('|')[0]
        store_list_cordx = id.split('|')[1]
        store_list_cordy =  id.split('|')[2]
        count_num = count / 21
        store_list = getStoreInfo(store_list_id, store_list_cordx, store_list_cordy)
        if str(count_num).endswith('.0') == True:
            print('대기중'), time.sleep(900)
        print(id, count)
        count += 1
        for store in store_list:
            outfile.write(u'%s|' % store['ID'])
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['cat'])
            outfile.write(u'%s|' % store['newaddr'])
            outfile.write(u'%s|' % store['oldaddr'])
            outfile.write(u'%s|' % store['cordx'])
            outfile.write(u'%s|' % store['cordy'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['sourceDate'])
            outfile.write(u'%s|' % store['modu_time_list'])
            outfile.write(u'%s|' % store['modu_price_list'])
            outfile.write(u'%s|' % store['modu_url'])
            outfile.write(u'%s|' % store['kakaot_countSpot'])
            outfile.write(u'%s|' % store['kakaot_payTypeDisps'])
            outfile.write(u'%s|' % store['kakaot_openHours'])
            outfile.write(u'%s|\n' % store['kakaot_offlinePrice'])
        time.sleep(random.uniform(1,1.1))
    outfile.close()

def getStoreInfo(ID,cordx,cordy):
    result = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    try:
        url = 'https://place.map.kakao.com/main/v/{}?_=1620092986015'.format(ID)
        pageString = requests.get(url, headers=headers).text
        jsonData = json.loads(pageString)
        basicinfo = jsonData['basicInfo']
        parkinginfo = jsonData['parkingInfo']
    except:pass
    else:
        try:name = basicinfo["placenamefull"]
        except:name = ''
        try:cat = basicinfo['catename']
        except:cat = ''
        try:newaddr = str(basicinfo['address']['region']['newaddrfullname']) + ' ' + str(basicinfo['address']['newaddr']['newaddrfull'])
        except : newaddr = ''
        try: oldaddr = str(basicinfo['address']['region']['fullname']) + ' ' + str(basicinfo['address']['addrbunho'])
        except:oldaddr = ''
        try:sourceDate = basicinfo['source']['date']
        except:sourceDate = ''
        try : tell = basicinfo['phonenum']
        except : tell = ''

        try : modu_time_list = parkinginfo['modu']['hourList']
        except: modu_time_list = ''
        try : modu_price_list = parkinginfo['modu']['offlinePriceList']
        except : modu_price_list = ''
        try: modu_url = parkinginfo['modu']['outlinkPc']
        except: modu_url = ''

        try : kakaot_countSpot = parkinginfo['kakaot']['countSpot']
        except: kakaot_countSpot = ''
        try : kakaot_payTypeDisps = parkinginfo['kakaot']['payTypeDisps']
        except : kakaot_payTypeDisps = ''
        try : kakaot_openHours = parkinginfo['kakaot']['openHours']
        except : kakaot_openHours = ''
        try : kakaot_offlinePrice = parkinginfo['kakaot']['offlinePrice']
        except : kakaot_offlinePrice = ''

        result.append({'ID': ID, 'name': name, 'cat': cat, 'newaddr': newaddr, 'oldaddr': oldaddr,'cordx':cordx,'cordy':cordy,'tell':tell,'sourceDate': sourceDate,
                       'modu_time_list':modu_time_list,'modu_price_list':modu_price_list,'modu_url':modu_url,'kakaot_countSpot':kakaot_countSpot,
                       'kakaot_payTypeDisps':kakaot_payTypeDisps,'kakaot_openHours':kakaot_openHours,'kakaot_offlinePrice':kakaot_offlinePrice})
    return result

getStore_list()
print('------------------리스트 수집완료------------------')
list_dup_remove()
print('------------------리스트 중복 제거------------------')
time.sleep(300)
daum_save()
print('------------------모든 수집완료------------------')