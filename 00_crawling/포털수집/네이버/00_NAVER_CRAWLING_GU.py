import codecs
import requests
import json
import time
import os
import random

start = time.time()

def main():
    outfile = codecs.open('Crawl_result_gu.txt', 'w', 'utf-8')
    inputNames = getInputName()
    sidoList = getSidoName()
    page = 1
    for input in inputNames:
        for sido in sidoList:
            if page == 500: time.sleep(120)
            if page == 1000: time.sleep(120)
            if page == 1500: time.sleep(120)
            if page == 2000: time.sleep(120)
            if page == 2500: time.sleep(120)
            if page == 3000: time.sleep(120)
            if page == 3500: time.sleep(120)
            if page == 4000: time.sleep(120)
            if page == 4500: time.sleep(120)
            result = getStoreInfo(input, sido)
            print(input,sido,page)
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
        lines2 = data.read().splitlines()
    inputName = lines2
    return inputName

def getSidoName():
    with open('sidolist_gu.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    return SearchList
def getStoreInfo(inputName,searchName):
    url ="https://map.naver.com/v5/api/search?caller=pcweb&query={} {}&type=all&searchCoord=127.10515475393677;37.50626&page=1&displayCount=300&isPlaceRecommendationReplace=true&lang=ko".format(inputName,searchName)
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
    except TypeError : pass
    except json.decoder.JSONDecodeError : pass
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
            list.append({"input":inputName,"id":id,"name":name,"oldaddr":oldaddr,"newaddr":newaddr,"tell":tell,"cat":cat,"xcord":xcord,"ycord":ycord,"url":url,"car_ent":car_ent,"walk_ent":walk_ent,"menu":menu,"time":time,'count':listcount,'inputname':inputname})
    return list
#
# def dup_remove():
#     w = open('Crawl_result_gu_중복제거.txt', 'w')
#     r = open('Crawl_result_gu.txt', 'r',encoding='UTF8')
#     # 파일에서 읽은 라인들을 리스트로 읽어들임
#     lines = r.readlines()
#     # Set에 넣어서 중복 제거 후 다시 리스트 변환
#     lines = list(set(lines))
#     # 리스트 정렬
#     # 정렬,중복제거한 리스트 파일 쓰기
#     w.write("INPUT|ID|NAME|OLDADDR|NEWADDR|TELL|CAT|XCORD|YCORD|URL|CAR_ENT|WALK_ENT|MENU|TIME\n")
#     for line in lines:
#         w.write(line)
#     # 파일 닫기
#     w.close()
#     r.close()
#     os.remove('Crawl_result_gu.txt')

print("time :", time.time() - start)

main()
# dup_remove()