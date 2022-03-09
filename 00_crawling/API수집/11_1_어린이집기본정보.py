import time
import requests
import random
import bs4
import codecs
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\11_1_어린이집기본정보\\') == False : os.makedirs('수집결과\\11_1_어린이집기본정보\\')
outfilename = '수집결과\\11_1_어린이집기본정보\\어린이집기본정보_{}.txt'.format(today)
outfilename_true = '수집결과\\11_1_어린이집기본정보\\어린이집기본정보_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\11_1_어린이집기본정보\\어린이집기본정보_{}.log_실패.txt'.format(today)

def main():
    try:
        Crawl_run()
        dup_remove()
        outfile = codecs.open(outfilename_true, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '정상 수집 완료'
        outfile.write(write_text)
        outfile.close()
    except:
        if os.path.isfile(outfilename_true):
            os.remove(outfilename_true)
        outfile = codecs.open(outfilename_false, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '수집 실패' + '|' + str(traceback.format_exc())
        outfile.write(write_text)
        outfile.close()

def Crawl_run():
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    page = getSidoCode_list()
    for code in page:
        store_list = getStoreInfo(code)
        print(code, store_list)
        if store_list == [] :
            print(code, "호출결과가 없는 리스트로 반환.")
            outfile_fail = codecs.open('수집결과\\11_1_어린이집기본정보\\전국어린이집정보_수집실패.txt', 'w')
            fail_url = str(code) + '\n'
            outfile_fail.write(fail_url)
            outfile_fail.close()
        for store in store_list:
            outfile.write(u'%s|' % store['stcode'])
            outfile.write(u'%s|' % store['crname'])
            outfile.write(u'%s|' % store['crtel'])
            outfile.write(u'%s|' % store['crfax'])
            outfile.write(u'%s|' % store['craddr'])
            outfile.write(u'%s|' % store['crhome'])
            outfile.write(u'%s\n' % store['crcapat'])
        time.sleep(random.uniform(2, 3))
    outfile.close()

    outfile = codecs.open(outfilename, 'a', 'utf-8')
    page = getcode()
    for code in page:
        store_list = getStoreInfo(code)
        print(code, store_list)
        if store_list == [] :
            print(code, "호출결과가 없는 리스트로 반환.")
            outfile_fail = codecs.open('수집결과\\11_1_어린이집기본정보\\전국어린이집정보_수집실패2.txt', 'w')
            fail_url = str(code) + '\n'
            outfile_fail.write(fail_url)
            outfile_fail.close()
        for store in store_list:
            outfile.write(u'%s|' % store['stcode'])
            outfile.write(u'%s|' % store['crname'])
            outfile.write(u'%s|' % store['crtel'])
            outfile.write(u'%s|' % store['crfax'])
            outfile.write(u'%s|' % store['craddr'])
            outfile.write(u'%s|' % store['crhome'])
            outfile.write(u'%s\n' % store['crcapat'])
        time.sleep(random.uniform(2, 3))
    outfile.close()

    outfile = codecs.open(outfilename, 'a', 'utf-8')
    page = getcode2()
    for code in page:
        store_list = getStoreInfo(code)
        print(store_list)
        if store_list == [] :
            print(code, "호출결과가 없는 리스트로 반환.")
            outfile_fail = codecs.open('수집결과\\11_1_어린이집기본정보\\전국어린이집정보_수집실패3.txt', 'w')
            fail_url = str(code) + '\n'
            outfile_fail.write(fail_url)
            outfile_fail.close()
        for store in store_list:
            outfile.write(u'%s|' % store['stcode'])
            outfile.write(u'%s|' % store['crname'])
            outfile.write(u'%s|' % store['crtel'])
            outfile.write(u'%s|' % store['crfax'])
            outfile.write(u'%s|' % store['craddr'])
            outfile.write(u'%s|' % store['crhome'])
            outfile.write(u'%s\n' % store['crcapat'])
        time.sleep(random.uniform(2, 3))
    outfile.close()

def getStoreInfo(sidoCode):
    url = "http://api.childcare.go.kr/mediate/rest/cpmsapi021/cpmsapi021/request"
    querystring = {"key":"ff74048210694a708f0c8871d0644ac8"}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    querystring['arcode'] = sidoCode
    data = []
    try:
        pageinfo = requests.get(url, params=querystring, headers=headers, timeout = 10).text
        print(url,querystring)
    except requests.exceptions.ConnectionError:
        print(sidoCode, "해당 코드의 페이지 호출을 실패하여 실패 리스트로 반환합니다.")
    except requests.exceptions.ReadTimeout:
        print(sidoCode, "해당 코드의 페이지 호출을 실패하여 실패 리스트로 반환합니다.")
    else:
        soup = bs4.BeautifulSoup(pageinfo,'lxml')
        list = soup.find_all('item')
        for info in range(len(list)):
            try:
                stcode = list[info].find('stcode').text
            except AttributeError:
                stcode = ''
            try:
                crname = list[info].find('crname').text
            except AttributeError:
                crname =''
            try:
                crtel = list[info].find('crtel').text
            except AttributeError:
                crtel = ''
            try:
                crfax = list[info].find('crfax').text
            except AttributeError:
                crfax =''
            try:
                craddr = list[info].find('craddr').text
            except AttributeError:
                craddr = ''
            try:
                crhome = list[info].find('crhome').text
            except AttributeError:
                crhome = ''
            try:
                crcapat = list[info].find('crcapat').text
            except AttributeError:
                crcapat = 'tr'
            data.append({"stcode":stcode,"crname":crname,"crtel":crtel,"crfax":crfax,"craddr":craddr,"crhome":crhome,"crcapat":crcapat})
    return data

def getSidoCode(sidoName):
    url = "http://api.childcare.go.kr/mediate/rest/cpmsapi020/cpmsapi020/request"
    querystring = {"key":"71c59f0ccc3b4b8da812e2db18ca9b56"}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    querystring['arname'] = sidoName
    pageinfo = requests.get(url, params=querystring, headers=headers, timeout = 10).text
    soup = bs4.BeautifulSoup(pageinfo,'lxml')
    list = soup.find_all('item')
    data = []
    for info in range(len(list)):
        sidoname = list[info].find('sidoname').text
        sigunname = list[info].find('sigunname').text
        arcode = list[info].find('arcode').text
        # data.append({"sidoname":sidoname,"sigunname":sigunname,"arcode":arcode})
        data.append(arcode)
    return data

def getSidoCode_list():
    sido_list = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시', '광주광역시', '대구광역시', '부산광역시', '세종특별자치시', '제주도']
    result = []
    for sido in sido_list:
        result = result + getSidoCode(sido)
        print(sido, getSidoCode(sido))
    return result

def getcode():
    with open('수집결과\\11_1_어린이집기본정보\\전국어린이집정보_수집실패.txt') as data:
        lines = data.read().splitlines()
    code_list = lines
    return  code_list

def getcode2():
    with open('수집결과\\11_1_어린이집기본정보\\전국어린이집정보_수집실패2.txt') as data:
        lines = data.read().splitlines()
    code_list = lines
    return  code_list

def dup_remove():
    outfilename_dupRemove = '수집결과\\11_1_어린이집기본정보\\어린이집기본정보_중복제거.txt'
    w = open(outfilename_dupRemove, 'w')
    r = open(outfilename, 'r',encoding='UTF8')
    # 파일에서 읽은 라인들을 리스트로 읽어들임
    lines = r.readlines()
    # Set에 넣어서 중복 제거 후 다시 리스트 변환
    lines = list(set(lines))
    # 리스트 정렬
    # 정렬,중복제거한 리스트 파일 쓰기
    w.write("STCODE|CRNAME|CRTEL|CRFAX|CRADDR|CRHOME|CRCAPAT\n")
    for line in lines:
        w.write(line)
    # 파일 닫기
    w.close()
    r.close()
    os.remove('수집결과\\11_1_어린이집기본정보\\전국어린이집정보_수집실패.txt')
    os.remove('수집결과\\11_1_어린이집기본정보\\전국어린이집정보_수집실패2.txt')
    os.remove('수집결과\\11_1_어린이집기본정보\\전국어린이집정보_수집실패3.txt')
    os.remove(outfilename)
    os.rename(outfilename_dupRemove, outfilename)

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()