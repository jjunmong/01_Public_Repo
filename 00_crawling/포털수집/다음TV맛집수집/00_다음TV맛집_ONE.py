import time
import requests
import random
import json
import codecs
import os

def main():
    outfile = codecs.open('다음TV맛집_1회_수집결과.txt', 'w', 'utf-8')

    sidolist = getSidoName()

    for sido in sidolist:
        page = 1
        while True:
            store_list = getStoreInfo(page, sido, 'TV맛집')
            print(page, sido)
            if len(store_list) <15 :
                for store in store_list:
                    outfile.write(u'%s|' % store['id'])
                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['cat'])
                    outfile.write(u'%s|' % store['old_addr'])
                    outfile.write(u'%s|' % store['new_addr'])
                    outfile.write(u'%s|' % store['tell'])
                    outfile.write(u'%s|' % store['tvinfo'])
                    outfile.write(u'%s\n' % store['cate'])
                break
            for store in store_list:
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['cat'])
                outfile.write(u'%s|' % store['old_addr'])
                outfile.write(u'%s|' % store['new_addr'])
                outfile.write(u'%s|' % store['tell'])
                outfile.write(u'%s|' % store['tvinfo'])
                outfile.write(u'%s\n' % store['cate'])
            page+=1
            time.sleep(random.uniform(1,1.5))
    outfile.close()

def getStoreInfo(intpageNo, sido, searchName):
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
        urlopen = requests.get(url, params=data, headers=headers).text
    except:
        print('Error calling the API')
    ss = urlopen.replace('/**/jQuery181018657064011065705_1634690332690(', '').replace(');', '')
    response = json.loads(ss)
    place = response['place']
    data =[]
    for list in place:
        id = list['confirmid']
        name = list['name']
        cat = list['brandName']
        old_addr = list['address']
        new_addr = list['new_address']
        tell = list['tel']
        tvinfo1 = str(list['tvshow_info']).replace('|','/')
        tvinfo2 = list['tvshow_name']
        tvinfo = tvinfo2+'/'+tvinfo1
        tv_show = list['tvshow_info']
        cate = list['brandName']
        if tv_show == '' : pass
        else:
            data.append({'id':id,'name':name,'cat':cat,'old_addr':old_addr,'new_addr':new_addr,'tell':tell,'tvinfo':tvinfo,'cate':cate})
    return data

def getSidoName():
    with open('daum_tv_sidolist.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    return SearchList

def dup_remove():
    w = open('다음TV맛집_1회_수집결과_중복제거.txt', 'w')
    r = open('다음TV맛집_1회_수집결과.txt', 'r',encoding='UTF8')
    # 파일에서 읽은 라인들을 리스트로 읽어들임
    lines = r.readlines()
    # Set에 넣어서 중복 제거 후 다시 리스트 변환
    lines = list(set(lines))
    # 리스트 정렬
    # 정렬,중복제거한 리스트 파일 쓰기
    w.write("ID|NAME|CAT|OLD_ADDR|NEW_ADDR|TELL|TV_INFO|CATE\n")
    for line in lines:
        w.write(line)
    # 파일 닫기
    w.close()
    r.close()
    # os.remove('DAUM_TV맛집_간편수집결과.txt')

main()
dup_remove()
print('------------------수집완료------------------')