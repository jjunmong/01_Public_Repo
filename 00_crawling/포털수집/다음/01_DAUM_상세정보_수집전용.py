import time
import requests
import random
import json
import codecs

def getStore_id(searchName):
    url = 'https://search.map.daum.net/mapsearch/map.daum'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'HM_CU=5BeqkwBaldY; SLEVEL=1; webid=6452e45117e04f0e916f6cf1906b22ef; PROF=0603012032024064024192UiQPJk7X-6w0mlxoempuua9xJx.tnadvun2eF_6hqavgKuZP3z7wEl2bxriNh5SdkQ00LYYSA9A1_cGNLCyhCzrwOgyiAbNDcmXxh2w41oSjfO2GJnBHNMEzaCuyn1ZLzpPZfIauQlo8OTLcCscrxJX8Uw00cFQ7_86aN.l6LmAlEdKYTrNoXVAnUnIqjfmWiGn9LMSj__Chfu5NCxD-RP63Y8_4QeFwveJ.YJ-o23ZpZSEfwRRkij-5YpUmK.5nNr4F5h3BPoofgFROPsnmMheLHsjhK_QNysMOO5LC7gOE7gjwahEqlf86C9kHSiOjHiFBz3YHhFPgUmDWuuAxeTCDTaWa; ALCT=HH33WvWcJggxzQBo8emmuh-wSev7WY8LEJr1Twu9c_E; AGEN=7vEWAnOLmC89qzSrLrHaGAam8GIgivb5M_Z4_u-7R3Q; TIARA=Vlp9XTDCvTRwmyxWLS1W3-PX.QWSta5qN-w.x8gjPI_HLh8t6YGdgXb.eFybv.FGbwQVcRSMc5KkZ.HqR3MT-LP57pyMbZA1; webid_sync=1579047407478; TS=1579047670; HTS=niSZIMK5poWkKjGKhiofYw00; ALID=tGtJj7PfjX_-V0V3pCeOrWzsp9IJGZYSQxkSlD82kA8_gISEDEnIN5oszMeiixP2w999UI; LSID=9f9765d8-9e81-487e-827f-566e07bbfdc41579047670122; ssab=',
        'Host': 'search.map.daum.net',
        'Referer': 'https://map.kakao.com/',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }
    data = {
        'callback': 'jQuery18106614589704115768_1579047502403',
        'msFlag': 'A',
        'sort': '0',
    }
    data['q'] = searchName
    try:
        urlopen = requests.post(url, data=data, headers=headers).text
    except:
        print('Error calling the API')
    ss = urlopen.replace('jQuery18106614589704115768_1579047502403 (', '').replace('(', '').replace(')', '')
    response = json.loads(ss)
    result = []
    try:
        place = response['place']
        id = place[0]['confirmid']
        if response['place'][0]['cate_name_depth1'] != '음식점':
            place = response['place']
            id = place[1]['confirmid']
    except :
        id = '찾을 수 없음'
    name_id_sum = searchName + '|'+id
    result.append(name_id_sum)
    return result

def getStoreName():
    with open('daum_search_list.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    return SearchList

def getStore_id_all():
    result = []
    nameList = getStoreName()
    for name in nameList:
        print(name)
        result = result + getStore_id(name)
        # time.sleep(random.uniform(0.9, 1.2))
    # results = list(set(result))
    return result

def getStore_list():
    alllist = getStore_id_all()
    outfile_daum = codecs.open('daum_ID_list.txt', 'a')
    for lists in alllist:
        tv_list = str(lists) + '\n'
        outfile_daum.write(tv_list)
    outfile_daum.close()

#####################################################################################

def daum_save():
    outfile = codecs.open('다음_상세정보_수집결과.txt', 'a', 'utf-8')
    outfile.write(
        "SOURCENAME|ID|NAME|CAT|ADDR|TELL|FORDISABLED|PARKING|PET|SMOKINGROOM|WIFI|APPOINTMENT|PACKAGE|SOURCEDATE|MENU|TVINFO1|TVINFO2|TVINFO3|TVINFO4|TVINFO5|DAYOFF|24HR|MONTIME|THUTIME|WEDTIME|TURRIME|FRITIME|SATTIME|SUNTIME|HOLTIME\n")

    with open('daum_ID_list.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    id_list = SearchList
    count = 1
    for id in id_list:
        id1 = id.split('|')[0]
        id2 = id.split('|')[1]
        if id2 == '찾을 수 없음' : count = count -1
        store_list = getStoreInfo(id1,id2)
        count_num = count / 20
        if str(count_num).endswith('.0') == True:
            print('대기중'), time.sleep(900)
        print(id, count)
        count += 1
        for store in store_list:
            outfile.write(u'%s|' % store['SourceName'])
            outfile.write(u'%s|' % store['ID'])
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['cat'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['fordisabled'])
            outfile.write(u'%s|' % store['parking'])
            outfile.write(u'%s|' % store['pet'])
            outfile.write(u'%s|' % store['smokimgroom'])
            outfile.write(u'%s|' % store['wifi'])
            outfile.write(u'%s|' % store['appointment'])
            outfile.write(u'%s|' % store['package'])
            outfile.write(u'%s|' % store['sourceDate'])
            outfile.write(u'%s|' % store['menu'])
            outfile.write(u'%s|' % store['tvinfo1'])
            outfile.write(u'%s|' % store['tvinfo2'])
            outfile.write(u'%s|' % store['tvinfo3'])
            outfile.write(u'%s|' % store['tvinfo4'])
            outfile.write(u'%s|' % store['tvinfo5'])
            outfile.write(u'%s|' % store['dayoff'])
            outfile.write(u'%s|' % store['mon_time'])
            outfile.write(u'%s|' % store['tue_time'])
            outfile.write(u'%s|' % store['wed_time'])
            outfile.write(u'%s|' % store['thu_time'])
            outfile.write(u'%s|' % store['fri_time'])
            outfile.write(u'%s|' % store['sat_time'])
            outfile.write(u'%s|' % store['sun_time'])
            outfile.write(u'%s|\n' % store['hol_time'])
        time.sleep(random.uniform(1, 1.5))

    outfile.close()

def getStoreInfo(Name,ID):
    result = []
    if ID == '찾을 수 없음' : result.append({'SourceName':Name,'ID': ID, 'name': '', 'cat': '', 'addr': '', 'tell': '', 'fordisabled': '',
                       'parking': '', 'pet': '', 'smokimgroom': '', 'wifi': '',
                       'appointment': '', 'package': '', 'sourceDate': '', 'menu': '','tvinfo1': '',
                       'tvinfo2': '', 'tvinfo3': '', 'tvinfo4': '', 'tvinfo5': '',
                       'dayoff': '', '24hr': '', 'mon_time': '', 'tue_time': '', 'wed_time': '',
                       'thu_time': '', 'fri_time': '', 'sat_time': '', 'sun_time': '',
                       'hol_time': ''})
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }
        try:
            url = 'https://place.map.kakao.com/main/v/{}?_=1620092986015'.format(ID)
            pageString = requests.get(url, headers=headers).text
            jsonData = json.loads(pageString)
            basicinfo = jsonData['basicInfo']
            try:
                menuinfo = jsonData['menuInfo']
            except :
                menuinfo = ''
        except:
            result.append({'SourceName':Name,'ID': ID, 'name': '', 'cat': '', 'addr': '', 'tell': '', 'fordisabled': '',
                           'parking': '', 'pet': '', 'smokimgroom': '', 'wifi': '',
                           'appointment': '', 'package': '', 'sourceDate': '', 'menu': '','tvinfo1': '',
                           'tvinfo2': '', 'tvinfo3': '', 'tvinfo4': '', 'tvinfo5': '',
                           'dayoff': '', '24hr': '', 'mon_time': '', 'tue_time': '', 'wed_time': '',
                           'thu_time': '', 'fri_time': '', 'sat_time': '', 'sun_time': '',
                           'hol_time': ''})
        else:
            try:
                name = basicinfo["placenamefull"]
            except:
                name = ''
            try:
                cat = basicinfo['catename']
            except:
                cat = ''
            try:
                addr = str(basicinfo['address']['region']['newaddrfullname']) + ' ' + str(
                    basicinfo['address']['newaddr']['newaddrfull'])
            except:
                try:
                    addr = str(basicinfo['address']['region']['fullname']) + ' ' + str(basicinfo['address']['addrbunho'])
                except : addr = ''
            try:
                tell = basicinfo['phonenum']
            except:
                tell = ''
            try:
                fordisabled = basicinfo['facilityInfo']['fordisabled']
            except:
                fordisabled = ''
            try:
                parking = basicinfo['facilityInfo']['parking']
            except:
                parking = ''
            try:
                pet = basicinfo['facilityInfo']['pet']
            except:
                pet = ''
            try:
                smokimgroom = basicinfo['facilityInfo']['smokingroom']
            except:
                smokimgroom = ''
            try:
                wifi = basicinfo['facilityInfo']['wifi']
            except:
                wifi = ''
            try:
                appointment = basicinfo['operationInfo']['appointment']
            except:
                appointment = ''
            try:
                package = basicinfo['operationInfo']['pagekage']
            except:
                package = ''
            try:
                sourceDate = basicinfo['source']['date']
            except:
                sourceDate = ''
            try:
                menu = []
                for info in menuinfo['menuList']:
                    M = info['menu']
                    P = str(info['price']).replace(',','')
                    Sum = M+':'+P+'/'
                    menu.append(Sum)
                menu = str(menu).replace("', '", "/").replace("'", "").replace('[', '').replace('/]', '').replace('//','@')
            except: menu = ''
            try:
                tvInfoList1 = basicinfo['tvInfoList'][0]
            except:
                tvInfoList1 = ''
            if tvInfoList1 == '':
                pass
            else:
                chtitle = tvInfoList1['chtitle']
                episodeseq = tvInfoList1['episodeseq']
                prtitle = tvInfoList1['prtitle']
                telecastdt = tvInfoList1['telecastdt']
                tvInfoList1 = episodeseq + '회/' + chtitle + '/' + prtitle + '/' + telecastdt
            try:
                tvInfoList2 = basicinfo['tvInfoList'][1]
            except:
                tvInfoList2 = ''
            if tvInfoList2 == '':
                pass
            else:
                chtitle = tvInfoList2['chtitle']
                episodeseq = tvInfoList2['episodeseq']
                prtitle = tvInfoList2['prtitle']
                telecastdt = tvInfoList2['telecastdt']
                tvInfoList2 = episodeseq + '회/' + chtitle + '/' + prtitle + '/' + telecastdt
            try:
                tvInfoList3 = basicinfo['tvInfoList'][2]
            except:
                tvInfoList3 = ''
            if tvInfoList3 == '':
                pass
            else:
                chtitle = tvInfoList3['chtitle']
                episodeseq = tvInfoList3['episodeseq']
                prtitle = tvInfoList3['prtitle']
                telecastdt = tvInfoList3['telecastdt']
                tvInfoList3 = episodeseq + '회/' + chtitle + '/' + prtitle + '/' + telecastdt
            try:
                tvInfoList4 = basicinfo['tvInfoList'][3]
            except:
                tvInfoList4 = ''
            if tvInfoList4 == '':
                pass
            else:
                chtitle = tvInfoList4['chtitle']
                episodeseq = tvInfoList4['episodeseq']
                prtitle = tvInfoList4['prtitle']
                telecastdt = tvInfoList4['telecastdt']
                tvInfoList4 = episodeseq + '회/' + chtitle + '/' + prtitle + '/' + telecastdt
            try:
                tvInfoList5 = basicinfo['tvInfoList'][4]
            except:
                tvInfoList5 = ''
            if tvInfoList5 == '':
                pass
            else:
                chtitle = tvInfoList5['chtitle']
                episodeseq = tvInfoList5['episodeseq']
                prtitle = tvInfoList5['prtitle']
                telecastdt = tvInfoList5['telecastdt']
                tvInfoList5 = episodeseq + '회/' + chtitle + '/' + prtitle + '/' + telecastdt

            try:
                dayoff_info = basicinfo['openHour']['offdayList'][0]['weekAndDay']
            except:
                dayoff_info = ''

            dayoff = ''

            if dayoff_info == '월요일': dayoff = 'W1D1' + ',' + 'W2D1' + ',' + 'W3D1' + ',' + 'W4D1' + ',' + 'W5D1'
            if dayoff_info == '화요일': dayoff = 'W1D2' + ',' + 'W2D2' + ',' + 'W3D2' + ',' + 'W4D2' + ',' + 'W5D2'
            if dayoff_info == '수요일': dayoff = 'W1D3' + ',' + 'W2D3' + ',' + 'W3D3' + ',' + 'W4D3' + ',' + 'W5D3'
            if dayoff_info == '목요일': dayoff = 'W1D4' + ',' + 'W2D4' + ',' + 'W3D4' + ',' + 'W4D4' + ',' + 'W5D4'
            if dayoff_info == '금요일': dayoff = 'W1D5' + ',' + 'W2D5' + ',' + 'W3D5' + ',' + 'W4D5' + ',' + 'W5D5'
            if dayoff_info == '토요일': dayoff = 'W1D6' + ',' + 'W2D6' + ',' + 'W3D6' + ',' + 'W4D6' + ',' + 'W5D6'
            if dayoff_info == '일요일': dayoff = 'W1D7' + ',' + 'W2D7' + ',' + 'W3D7' + ',' + 'W4D7' + ',' + 'W5D7'

            try:
                hr_info = basicinfo['openHour']['realtime']['currentPeriod']['timeList'][0]['dayOfWeek']
                if hr_info == '매일':
                    hr = '1'
                else:
                    hr = '0'
            except:
                hr = '0'
                hr_info = ''

            try:
                time_info = basicinfo['openHour']['realtime']['currentPeriod']['timeList'][0]['timeSE']
                time_info = str(time_info).replace(' ', '').replace('~', '-')
            except:
                time_info = ''
            mon_time = time_info
            tue_time = time_info
            wed_time = time_info
            thu_time = time_info
            fri_time = time_info
            sat_time = time_info
            sun_time = time_info
            hol_time = ''

            if dayoff_info == '월요일': mon_time = ''
            if dayoff_info == '화요일': tue_time = ''
            if dayoff_info == '수요일': wed_time = ''
            if dayoff_info == '목요일': thu_time = ''
            if dayoff_info == '금요일': fri_time = ''
            if dayoff_info == '토요일': sat_time = ''
            if dayoff_info == '일요일': sun_time = ''
            if hr_info == '매일': hol_time = time_info

            result.append({'SourceName':Name,'ID': ID, 'name': name, 'cat': cat, 'addr': addr, 'tell': tell, 'fordisabled': fordisabled,
                           'parking': parking, 'pet': pet, 'smokimgroom': smokimgroom, 'wifi': wifi,
                           'appointment': appointment, 'package': package, 'sourceDate': sourceDate, 'menu': menu, 'tvinfo1': tvInfoList1,
                           'tvinfo2': tvInfoList2, 'tvinfo3': tvInfoList3, 'tvinfo4': tvInfoList4, 'tvinfo5': tvInfoList5,
                           'dayoff': dayoff, '24hr': hr, 'mon_time': mon_time, 'tue_time': tue_time, 'wed_time': wed_time,
                           'thu_time': thu_time, 'fri_time': fri_time, 'sat_time': sat_time, 'sun_time': sun_time,
                           'hol_time': hol_time})
    return result


getStore_list()
print('------------------리스트 수집완료------------------')
daum_save()
print('------------------모든 수집완료------------------')