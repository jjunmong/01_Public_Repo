import requests
import json
import codecs
import random
import time

def main():
    outfile = codecs.open('daum_crawling_result.txt', 'w', 'utf-8')
    outfile.write("NAME|CAT|OLDADDR|NEWADDR|TELL|URL\n")

    inputNames = getInputName()
    sidolist = getSidoName()

    for input in inputNames:
        for sido in sidolist:
            page = 1
            while True:
                store_list = getStoreInfo(page, sido, input)
                print(page, sido, input)
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

def getInputName():
    with open('inputlist.txt') as data:
        lines2 = data.read().splitlines()
    inputName = lines2
    return inputName

def getSidoName():
    with open('sidolist_dong.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    return SearchList

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
        result.append({'inputName':searchName, 'name':name, 'oldaddr':oldaddr, 'newaddr':newaddr,'tell':tell,'cat':cat,'url':url})
    return result

main()

