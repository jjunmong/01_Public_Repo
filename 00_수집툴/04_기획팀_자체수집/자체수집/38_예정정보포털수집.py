import codecs
import requests
import json
import time
import random

def main():

    outfile = codecs.open('수집결과\\38_네이버_예정정보.txt', 'w', 'utf-8')
    inputNames = getInputName()

    for input in inputNames:
        page = 1
        while True:
            if getStoreInfo(input, page) == [] : break
            result = getStoreInfo(input, page)
            print(input,page)
            for results in result:
                outfile.write(u'%s|' % results['input'])
                outfile.write(u'%s|' % results['id'])
                outfile.write(u'%s|' % results['name'])
                outfile.write(u'%s|' % results['oldaddr'])
                outfile.write(u'%s|' % results['newaddr'])
                outfile.write(u'%s|' % results['tell'])
                outfile.write(u'%s|' % results['cat'])
                outfile.write(u'%s|' % results['xcord'])
                outfile.write(u'%s|' % results['ycord'])
                outfile.write(u'%s|' % results['url'])
                outfile.write(u'%s|' % results['car_ent'])
                outfile.write(u'%s|' % results['walk_ent'])
                outfile.write(u'%s|' % results['menu'])
                outfile.write(u'%s\n' % results['time'])
            page +=1
        time.sleep(random.uniform(0.9, 1.2))
    outfile.close()

def getInputName():
    with open('inputlist.txt') as data:
        lines = data.read().splitlines()
    inputName = lines
    return inputName

def getStoreInfo(inputName, page):
    url ="https://map.naver.com/v5/api/search?caller=pcweb&query={}&type=all&searchCoord=127.10515475393677;37.50626&page={}&displayCount=100&isPlaceRecommendationReplace=true&lang=ko".format(inputName, page)
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'hide_intro_popup=true; NNB=VD5X4T5BDQQV4; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; _ga_4BKHBFKFK0=GS1.1.1580361926.2.1.1580361933.53; ASID=70a9214300000171a09755f300000052; NDARK=Y; NFS=2; _ga_7VKFYR6RV1=GS1.1.1606871504.2.1.1606871547.17; _ga_1BVHGNLQKG=GS1.1.1627620465.3.1.1627620482.0; _ga=GA1.2.596751893.1580201194; NID_AUT=n05PMvUm8N2X/Waf7uwOzmHbwCaKV7pCXiAhBczbNuB9uw1oyr+kz8Dc7yycCpCr; NID_JKL=jIOz5mIqkj70+e7soPy9PoNANf57VH+JC4oTsxQ3Knc=; nx_ssl=2; page_uid=hU4kTsp0YidssMupVxhssssstFh-333950; BMR=s=1634892771009&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dsabisung%26logNo%3D220461496301&r2=https%3A%2F%2Fwww.google.com%2F; NID_SES=AAABpxTw9/08YtTkjkFEYEcVggOhlYQH5ujpCZ3dtE/Eh1PONQr/ocQvc31uDhyaGhwCWZgBLA9XPbqcvglKFi0Mk+qAoyuEgmBY7ACPMUsbMvQUK3WsaOs6qDJ2A/Jk2ehhAVqWZVG9RYmg9hhq/uYINZ+rYp51T71FnySEdsifNHkZfO1ZqLNSBoCPPvjruVlZYFu8TuD2zSEpFNs1rMoc8DWxNU/beI0HY9TTRs20BEuk38YzRCU/PBxbjb4+oaVvgMdkA+GptCHYdCbg9FUuJyLxM0WcNHfq0IjrtaPwLyyJywqM5cRBTv63sQ+eBgDpX5g44NUvuJqL/PIiT3HdB0JpNSMoZ0KIQnFAK/wPy58GUwt89KG/D3pdHa/VRPIVh1L9vS2exP/IfdhgHwiKixCRfz/qVKFpHYL5UQQqzO0UcGS+k+uKdaa+eefyCMN5Eu/pcC83ahNYoRVTmXV/G3oOh1oYXNhOXGy27JKPoPuC1+x14LdqzmC6Ke9CXtJ9V+Lc+/0U+rxs+QV7JUjIsUF2IMV2Yd+y0GHCV0XoD2uUVv3havBnISeT8aMbsGtAmg==; page_uid=71db2c8b-da7c-404a-9d10-d66761e416c1; csrf_token=2d6fcb0cd063f5e31cfc8ba551bbab1457cde521474965aede72cd0290cb26e7d0e68910f21469b6f0b0fdb623a10bd29e39ebeec4bfc5e36876ac51f9cd2059',
        'expires': 'Sat, 01 Jan 2000 00:00:00 GMT',
        'pragma': 'no-cache',
        'referer': 'https://map.naver.com/',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    }
    req = requests.get(url, headers = headers).text
    list = []
    try:
        data = json.loads(req)
        data_all = data['result']['place']['list']
        try:
            listcount = data['result']['place']['totalCount']
        except:
            listcount = ''
        inputname = inputName
    except : pass
    else:
        if data_all == None : pass
        for ss in data_all:
            try: id = ss['id']
            except : id = ''
            try: name = ss['name']
            except : name = ''
            try: oldaddr = ss['address']
            except : oldaddr = ''
            try: newaddr = ss['roadAddress']
            except : newaddr = ''
            try : tell = ss['tel']
            except : tell = ''
            try: cat = ss['category']
            except : cat = ''
            try:xcord = ss['x']
            except:xcord = ''
            try: ycord = ss['y']
            except :ycord = ''
            try : url = ss['homePage']
            except : url = ''
            try : car_ent =  ss['entranceCoords']['car']
            except : car_ent = ''
            try: walk_ent = ss['entranceCoords']['walk']
            except : walk_ent = ''
            try: menu = ss['menuInfo']
            except: menu = ''
            try :time = ss['bizhourInfo']
            except : time = ''
            if name.endswith('예정)')==True :
                list.append({"input":inputName,"id":id,"name":name,"oldaddr":oldaddr,"newaddr":newaddr,"tell":tell,"cat":cat,"xcord":xcord,"ycord":ycord,"url":url,"car_ent":car_ent,"walk_ent":walk_ent,"menu":menu,"time":time,'count':listcount,'inputname':inputname})
            else : pass
    return list

def main2():
    outfile = codecs.open('수집결과\\38_다음_예정정보.txt', 'w', 'utf-8')
    outfile.write("NAME|CAT|OLDADDR|NEWADDR|TELL|URL\n")
    inputNames = getInputName()
    for input in inputNames:
        page = 1
        while True:
            store_list = getStoreInfo2(page, input)
            print(input, page)
            if len(store_list) <15 :
                for store in store_list:
                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['cat'])
                    outfile.write(u'%s|' % store['oldaddr'])
                    outfile.write(u'%s|' % store['newaddr'])
                    outfile.write(u'%s|' % store['tell'])
                    outfile.write(u'%s\n' % store['url'])
                break
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['cat'])
                outfile.write(u'%s|' % store['oldaddr'])
                outfile.write(u'%s|' % store['newaddr'])
                outfile.write(u'%s|' % store['tell'])
                outfile.write(u'%s\n' % store['url'])
            page+=1
            time.sleep(random.uniform(1,1.5))
    outfile.close()

def getStoreInfo2(intpageNo, searchName):
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
    data['q'] = searchName
    try:
        urlopen = requests.get(url ,params = data, headers = headers).text
    except:
        print('Error calling the API')
    ss = urlopen.replace('/**/jQuery181018657064011065705_1634690332690(','').replace(');','')
    response = json.loads(ss)
    place = response['place']
    result = []
    for info in place:
        name = info['name']
        oldaddr = info['address']
        newaddr = info['new_address']
        tell = info['tel']
        cat = info['cate_name_depth1'] + '/' + info['cate_name_depth2'] + '/' + info[
            'cate_name_depth3'] + '/' + info['cate_name_depth4']
        url = info['homepage']
        if name.endswith('예정)') == True:
            result.append({'name':name, 'oldaddr':oldaddr, 'newaddr':newaddr,'tell':tell,'cat':cat,'url':url})
        else: pass
    return result

main()
main2()
