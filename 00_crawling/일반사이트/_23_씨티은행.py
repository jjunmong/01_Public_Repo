import bs4
import codecs
import time
import requests
import sys
import json
import random

# 2021-01-27 : 헤더 쿠키 추가

def main():

    outfile = codecs.open('23_citibank.txt', 'w', 'utf-8')
    outfile.write("##NAME|BRANCH|ID|ADDR|TELL|FAX|XCOORD|YCOORD\n")

    sido_list = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시',
                 '광주광역시', '대구광역시', '부산광역시', '세종특별자치시', '제주특별자치도']

    for sido_name in sido_list:
        page = 1
        while True:
            store_list = getStoreInfo(sido_name, page)
            print(sido_name,page)
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['tell'])
                outfile.write(u'%s|' % store['xcoord'])
                outfile.write(u'%s\n' % store['ycoord'])
            page +=1
            if len(getStoreInfo(sido_name, page)) < 3 :
                store_list = getStoreInfo(sido_name, page)
                for store in store_list:
                    outfile.write(u'%s|' % store['name'])
                    outfile.write(u'%s|' % store['branch'])
                    outfile.write(u'%s|' % store['addr'])
                    outfile.write(u'%s|' % store['id'])
                    outfile.write(u'%s|' % store['tell'])
                    outfile.write(u'%s|' % store['xcoord'])
                    outfile.write(u'%s\n' % store['ycoord'])
                break
            time.sleep(random.uniform(0.3, 0.9))
    outfile.close()

def getStoreInfo(sido_name,intPageNo):
    url = 'https://www.citibank.co.kr/AtmSrch10.act'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'cache-control': 'no-cache',
        'content-length': '121',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'JSESSIONID=0001nYcL93g4j36j0FDRMjVWHdZ:-80PUHF; WMONID=MbSEmNl_1Bs; bm_sz=5FA4017B6E86D88F7944C2FEA2B1F771~YAAQNZc7FxPzrT13AQAAKGJWQQrK+qiKxbheMak2vU5eEeif4GsZSoIYvGqcYbJsSF+7gq/9JAbaoEL4vcFMWnaJZoQmmW0vQRe7V1RSYcuc5Kc0q92dIHx5nwWDsvandw+iXD+52b1bXUIx8HNp5O6HfwnQr/BTzBlNG8B/c+rfaAFNojmixZRp3R0W7uoHp+XEvw==; JEX_LANG=KO; JEX_LOCAL_LANG=KO; _abck=B05FA233BAC681DEDCF0C9E72FDC8274~0~YAAQNZc7FybzrT13AQAAsGVWQQWqCtmjON7yWhcFqDrCUaWMcYcjlM2ouQBvRFFbECGn4Bw+ji+KSdI+nJVUhsCpPqkc1aZpzcY2e5VtZv/jSVhsBP/DuVTw+/QFshtIxhRUbyYXCT+xTMS6MKi8lhG411D+r4UgPBPtEW10HjGK4kKUif7CX5pF3DTrZdu2Xm2KXhYcf/9iNwYcT5ihD0IJ9+zf6mk2x6vBEGK/OafhNY7pZyVVq0YlJVWsdmXsR2QcDpfcZaZ7Rj7x8NqLulZCEgxG+PwzLb9jNiEZJOQmLUquKj8LuwWqbuercfzUE5e8mCIVNYCkENV43Q94VFKSdQb7muwesYY=~-1~||-1||~-1; ak_bmsc=0E9E19FFE60F251DC3B93D9E924A9A02173B97354E010000F4B9106088460B64~pl0FGm7kvBDb0OeMp9D/lLSliOOmpLNMMuMpColM2uPr4U3j8dPiWo+znyledDcJ04daEZpakZSsL7OqoxnHZKde+yZYV8LeL/Lh6RBew/j2xsEHObOaHJ7VtbKwQ2AFd4o9i69zkTqlMdYTTz9ZFCnWjoK5Zd+wHAZtuLrFSmJYtnkGEm9gZIIvINYkVa8Ivza7wU07Oib97yo/0qvwrYH1/hLXIgCNsC+nAoBq2LtWsLe1MtWaNIH2G8grAcig/m; delfino.recentModule=G3; s_pers=%20s_vnum%3D1612105200645%2526vn%253D1%7C1612105200645%3B%20s_fid%3D22FD6E4F1C283DD3-1B8AD056C4D0FCC2%7C1769475634520%3B%20s_pp39%3DPre-login%7C1611711034522%3B%20s_pp5%3DAnonymous%7C1611711034523%3B%20s_gpv_pageName%3DKR%257C%25EC%259D%2580%25ED%2596%2589%25EC%2586%258C%25EA%25B0%259C%252F%25EC%25B1%2584%25EC%259A%25A9%257C%25ED%2595%259C%25EA%25B5%25AD%25EC%2594%25A8%25ED%258B%25B0%25EC%259D%2580%25ED%2596%2589%25EC%2586%258C%25EA%25B0%259C%257C%25EC%25A7%2580%25EC%25A0%2590%25ED%2598%2584%25ED%2599%25A9%7C1611711034525%3B%20s_nr%3D1611709234526-New%7C1614301234526%3B%20s_invisit%3Dtrue%7C1611711034528%3B%20s_gpv_products%3Dno%2520value%7C1611711034529%3B; s_sess=%20s_pgb_product%3D%3B%20s_cc%3Dtrue%3B%20s_sq%3Dcitiintlkoreaprod%253D%252526c.%252526a.%252526activitymap.%252526page%25253DKR%2525257C%252525EC%2525259D%25252580%252525ED%25252596%25252589%252525EC%25252586%2525258C%252525EA%252525B0%2525259C%2525252F%252525EC%252525B1%25252584%252525EC%2525259A%252525A9%2525257C%252525ED%25252595%2525259C%252525EA%252525B5%252525AD%252525EC%25252594%252525A8%252525ED%2525258B%252525B0%252525EC%2525259D%25252580%252525ED%25252596%25252589%252525EC%25252586%2525258C%252525EA%252525B0%2525259C%2525257C%252525EC%252525A7%25252580%252525EC%252525A0%25252590%252525ED%25252598%25252584%252525ED%25252599%252525A9%252526link%25253D%252525EC%252525A7%25252580%252525EC%252525A0%25252590%252525EC%252525B0%252525BE%252525EA%252525B8%252525B0%252526region%25253Dcontent2%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%252526pid%25253DKR%2525257C%252525EC%2525259D%25252580%252525ED%25252596%25252589%252525EC%25252586%2525258C%252525EA%252525B0%2525259C%2525252F%252525EC%252525B1%25252584%252525EC%2525259A%252525A9%2525257C%252525ED%25252595%2525259C%252525EA%252525B5%252525AD%252525EC%25252594%252525A8%252525ED%2525258B%252525B0%252525EC%2525259D%25252580%252525ED%25252596%25252589%252525EC%25252586%2525258C%252525EA%252525B0%2525259C%2525257C%252525EC%252525A7%25252580%252525EC%252525A0%25252590%252525ED%25252598%25252584%252525ED%25252599%252525A9%252526pidt%25253D1%252526oid%25253Dhttps%2525253A%2525252F%2525252Fwww.citibank.co.kr%2525252FHrdInrdCnts0109.act%25252523%252526ot%25253DA%3B; JEX_UI_UUID=f4d2fa6f-5443-45e8-902d-660f45ff099a; bm_sv=542AC283961807A3C842F30AF818DC93~y2cU/fihvSQoyBVb4BSbOEosU7xpzIN4OT6Ml0ZQPLpNoIMty1toUaDlTtm6HmOvcBNPXOhRx4Q6t8otRWk7J7mXittpMfjtSVT8mnzS7SdQQYMgx2rlezTh3Iwol8LcsX6VoD0e16rwSCRzNjIE2mVaYol3AC6PvGv+0nduSzg=; JEX_UI_UUID_SND=f4d2fa6f-5443-45e8-902d-660f45ff099a',
        'origin': 'https://www.citibank.co.kr',
        'pragma': 'no-cache',
        'referer': 'https://www.citibank.co.kr/AtmSrch10.act',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }
    data = {
        'tab': '1',
        'search_flag': 'search',
        'ps': '3',
        'type': '',
        'idx': '',
        'chk_branch': 'on',
        'search_type': '1',
    }
    data['pg'] = intPageNo
    data['search_word'] = sido_name
    try:
        urlopen = requests.post(url, data=data, headers = headers)
        print(urlopen, url)
    except:
        print('Error calling the API')
    urlopen.encoding = 'utf-8'
    html = urlopen.text
    bsObj = bs4.BeautifulSoup(html,"html.parser")
    list_all = bsObj.find_all('div',{"class":"wrap icoType"})
    store_list = []
    for infos in list_all:
        name = "씨티은행"
        branch = infos.find("strong",{"class":"titH4"}).text
        if branch != None:
            branch = branch.rstrip().lstrip().replace('\r', '').replace('\t', '').replace('\n', '')
            if branch.endswith('(출)'):
                branch = branch[:-3].rstrip() + '출장소'
            elif branch.endswith('센터'):
                pass
            elif branch.endswith('본점'):
                pass
            elif not branch.endswith('지점'):
                branch += '지점'
            branch = branch.replace(' ', '/')
        id = infos.find("a",{"class":"links arrowR"})['onclick'].replace("showInfo('BRANCH',",'').replace("); return false;",'').replace("'",'')
        addr = infos.find('textarea').text
        tell = infos.select('div')[0].text.replace('\n             Tel. ','').replace(' \n            상세보기\n','').replace(' ','').replace('Fax.','')
        xcoord = ''
        ycoord = ''
        temp_list = infos.find('a')['onclick'].replace("'); return false",'')
        subinfo_list = temp_list.split(',')
        if len(subinfo_list) >= 4:
            xcoord = subinfo_list[2][1:-1]
            ycoord = subinfo_list[3][1:-1]
            if len(xcoord) > 5:
                xcoord = xcoord[:3] + '.' + xcoord[3:]
            if len(ycoord) > 5:
                ycoord = ycoord[:2] + '.' + ycoord[2:]
        store_list.append({"name":name,"branch":branch,"id":id,"addr":addr,"tell":tell,"xcoord":xcoord,"ycoord":ycoord})
    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()