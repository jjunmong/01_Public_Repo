import time
import codecs
import requests
import random
import bs4
import os
from datetime import datetime

def main():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\어린이집상세정보_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'w', 'utf-8')

    page = getSidoCode_list()

    # page = [11560,11620]
    for code in page:
        store_list = getStoreInfo(code)
        print(code, store_list)
        if store_list == [] :
            print(code, "호출결과가 없는 리스트로 반환.")
            outfile_fail = codecs.open('어린이집별기본정보_수집실패.txt', 'a')
            fail_url = str(code)
            outfile_fail.write(fail_url+'\n')
            outfile_fail.close()
        for store in store_list:
            outfile.write(u'%s|' % store['sidoname'])
            outfile.write(u'%s|' % store['sigunname'])
            outfile.write(u'%s|' % store['stcode'])
            outfile.write(u'%s|' % store['crname'])
            outfile.write(u'%s|' % store['crtypename'])
            outfile.write(u'%s|' % store['crstatusname'])
            outfile.write(u'%s|' % store['zipcode'])
            outfile.write(u'%s|' % store['craddr'])
            outfile.write(u'%s|' % store['crtelno'])
            outfile.write(u'%s|' % store['nrtrroomcnt'])
            outfile.write(u'%s|' % store['nrtrroomsize'])
            outfile.write(u'%s|' % store['plgrdco'])
            outfile.write(u'%s|' % store['cctvinstlcnt'])
            outfile.write(u'%s|' % store['chcrtescnt'])
            outfile.write(u'%s|' % store['crcapat'])
            outfile.write(u'%s|' % store['crchcnt'])
            outfile.write(u'%s|' % store['la'])
            outfile.write(u'%s|' % store['lo'])
            outfile.write(u'%s|' % store['crcargbname'])
            outfile.write(u'%s|' % store['crcnfmdt'])
            outfile.write(u'%s|' % store['crpausebegindt'])
            outfile.write(u'%s|' % store['crpauseenddt'])
            outfile.write(u'%s|' % store['crabldt'])
            outfile.write(u'%s|' % store['datastdrdt'])
            outfile.write(u'%s\n' % store['crspec'])

        time.sleep(random.uniform(0.9, 0.8))

    outfile.close()


def main2():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\어린이집상세정보_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'a', 'utf-8')

    list = getcode2()

    for code in list:
        store_list = getStoreInfo(code)
        print(store_list)
        if store_list == [] :
            print(code, "호출결과가 없는 리스트로 반환.")
            outfile_fail = codecs.open('어린이집별기본정보_수집실패2.txt', 'a')
            fail_url = str(code) + '\n'
            outfile_fail.write(fail_url)
            outfile_fail.close()
        for store in store_list:
            outfile.write(u'%s|' % store['sidoname'])
            outfile.write(u'%s|' % store['sigunname'])
            outfile.write(u'%s|' % store['stcode'])
            outfile.write(u'%s|' % store['crname'])
            outfile.write(u'%s|' % store['crtypename'])
            outfile.write(u'%s|' % store['crstatusname'])
            outfile.write(u'%s|' % store['zipcode'])
            outfile.write(u'%s|' % store['craddr'])
            outfile.write(u'%s|' % store['crtelno'])
            outfile.write(u'%s|' % store['nrtrroomcnt'])
            outfile.write(u'%s|' % store['nrtrroomsize'])
            outfile.write(u'%s|' % store['plgrdco'])
            outfile.write(u'%s|' % store['cctvinstlcnt'])
            outfile.write(u'%s|' % store['chcrtescnt'])
            outfile.write(u'%s|' % store['crcapat'])
            outfile.write(u'%s|' % store['crchcnt'])
            outfile.write(u'%s|' % store['la'])
            outfile.write(u'%s|' % store['lo'])
            outfile.write(u'%s|' % store['crcargbname'])
            outfile.write(u'%s|' % store['crcnfmdt'])
            outfile.write(u'%s|' % store['crpausebegindt'])
            outfile.write(u'%s|' % store['crpauseenddt'])
            outfile.write(u'%s|' % store['crabldt'])
            outfile.write(u'%s|' % store['datastdrdt'])
            outfile.write(u'%s\n' % store['crspec'])

        time.sleep(random.uniform(0.9, 0.8))

    outfile.close()

def getcode2():
    with open('어린이집별기본정보_수집실패.txt') as data:
        lines = data.read().splitlines()
    code_list = lines
    return  code_list

def main3():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\어린이집상세정보_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'a', 'utf-8')

    list = getcode3()

    for code in list:
        store_list = getStoreInfo(code)
        print(store_list)
        if store_list == [] :
            print(code, "호출결과가 없는 리스트로 반환.")
            outfile_fail = codecs.open('어린이집별기본정보_수집실패3.txt', 'a')
            fail_url = str(code) + '\n'
            outfile_fail.write(fail_url)
            outfile_fail.close()
        for store in store_list:
            outfile.write(u'%s|' % store['sidoname'])
            outfile.write(u'%s|' % store['sigunname'])
            outfile.write(u'%s|' % store['stcode'])
            outfile.write(u'%s|' % store['crname'])
            outfile.write(u'%s|' % store['crtypename'])
            outfile.write(u'%s|' % store['crstatusname'])
            outfile.write(u'%s|' % store['zipcode'])
            outfile.write(u'%s|' % store['craddr'])
            outfile.write(u'%s|' % store['crtelno'])
            outfile.write(u'%s|' % store['nrtrroomcnt'])
            outfile.write(u'%s|' % store['nrtrroomsize'])
            outfile.write(u'%s|' % store['plgrdco'])
            outfile.write(u'%s|' % store['cctvinstlcnt'])
            outfile.write(u'%s|' % store['chcrtescnt'])
            outfile.write(u'%s|' % store['crcapat'])
            outfile.write(u'%s|' % store['crchcnt'])
            outfile.write(u'%s|' % store['la'])
            outfile.write(u'%s|' % store['lo'])
            outfile.write(u'%s|' % store['crcargbname'])
            outfile.write(u'%s|' % store['crcnfmdt'])
            outfile.write(u'%s|' % store['crpausebegindt'])
            outfile.write(u'%s|' % store['crpauseenddt'])
            outfile.write(u'%s|' % store['crabldt'])
            outfile.write(u'%s|' % store['datastdrdt'])
            outfile.write(u'%s\n' % store['crspec'])

        time.sleep(random.uniform(0.9, 0.8))

    outfile.close()

def getcode3():
    with open('어린이집별기본정보_수집실패2.txt') as data:
        lines = data.read().splitlines()
    code_list = lines
    return  code_list

def main4():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\어린이집상세정보_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'a', 'utf-8')

    list = getcode4()

    for code in list:
        store_list = getStoreInfo(code)
        print(store_list)
        if store_list == [] :
            print(code, "호출결과가 없는 리스트로 반환.")
            outfile_fail = codecs.open('어린이집별기본정보_수집실패4.txt', 'a')
            fail_url = str(code) + '\n'
            outfile_fail.write(fail_url)
            outfile_fail.close()
        for store in store_list:
            outfile.write(u'%s|' % store['sidoname'])
            outfile.write(u'%s|' % store['sigunname'])
            outfile.write(u'%s|' % store['stcode'])
            outfile.write(u'%s|' % store['crname'])
            outfile.write(u'%s|' % store['crtypename'])
            outfile.write(u'%s|' % store['crstatusname'])
            outfile.write(u'%s|' % store['zipcode'])
            outfile.write(u'%s|' % store['craddr'])
            outfile.write(u'%s|' % store['crtelno'])
            outfile.write(u'%s|' % store['nrtrroomcnt'])
            outfile.write(u'%s|' % store['nrtrroomsize'])
            outfile.write(u'%s|' % store['plgrdco'])
            outfile.write(u'%s|' % store['cctvinstlcnt'])
            outfile.write(u'%s|' % store['chcrtescnt'])
            outfile.write(u'%s|' % store['crcapat'])
            outfile.write(u'%s|' % store['crchcnt'])
            outfile.write(u'%s|' % store['la'])
            outfile.write(u'%s|' % store['lo'])
            outfile.write(u'%s|' % store['crcargbname'])
            outfile.write(u'%s|' % store['crcnfmdt'])
            outfile.write(u'%s|' % store['crpausebegindt'])
            outfile.write(u'%s|' % store['crpauseenddt'])
            outfile.write(u'%s|' % store['crabldt'])
            outfile.write(u'%s|' % store['datastdrdt'])
            outfile.write(u'%s\n' % store['crspec'])

        time.sleep(random.uniform(0.9, 0.8))

    outfile.close()

def getcode4():
    with open('어린이집별기본정보_수집실패3.txt') as data:
        lines = data.read().splitlines()
    code_list = lines
    return  code_list

def main5():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\어린이집상세정보_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'a', 'utf-8')

    list = getcode5()

    for code in list:
        store_list = getStoreInfo(code)
        print(store_list)
        if store_list == [] :
            print(code, "호출결과가 없는 리스트로 반환.")
            outfile_fail = codecs.open('어린이집별기본정보_수집실패5.txt', 'a')
            fail_url = str(code) + '\n'
            outfile_fail.write(fail_url)
            outfile_fail.close()
        for store in store_list:
            outfile.write(u'%s|' % store['sidoname'])
            outfile.write(u'%s|' % store['sigunname'])
            outfile.write(u'%s|' % store['stcode'])
            outfile.write(u'%s|' % store['crname'])
            outfile.write(u'%s|' % store['crtypename'])
            outfile.write(u'%s|' % store['crstatusname'])
            outfile.write(u'%s|' % store['zipcode'])
            outfile.write(u'%s|' % store['craddr'])
            outfile.write(u'%s|' % store['crtelno'])
            outfile.write(u'%s|' % store['nrtrroomcnt'])
            outfile.write(u'%s|' % store['nrtrroomsize'])
            outfile.write(u'%s|' % store['plgrdco'])
            outfile.write(u'%s|' % store['cctvinstlcnt'])
            outfile.write(u'%s|' % store['chcrtescnt'])
            outfile.write(u'%s|' % store['crcapat'])
            outfile.write(u'%s|' % store['crchcnt'])
            outfile.write(u'%s|' % store['la'])
            outfile.write(u'%s|' % store['lo'])
            outfile.write(u'%s|' % store['crcargbname'])
            outfile.write(u'%s|' % store['crcnfmdt'])
            outfile.write(u'%s|' % store['crpausebegindt'])
            outfile.write(u'%s|' % store['crpauseenddt'])
            outfile.write(u'%s|' % store['crabldt'])
            outfile.write(u'%s|' % store['datastdrdt'])
            outfile.write(u'%s\n' % store['crspec'])

        time.sleep(random.uniform(0.9, 0.8))

    outfile.close()

def getcode5():
    with open('어린이집별기본정보_수집실패4.txt') as data:
        lines = data.read().splitlines()
    code_list = lines
    return  code_list

def main6():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\어린이집상세정보_{}.txt'.format(today)
    outfile = codecs.open(outfilename, 'a', 'utf-8')

    list = getcode6()

    for code in list:
        store_list = getStoreInfo(code)
        print(store_list)
        if store_list == [] :
            print(code, "호출결과가 없는 리스트로 반환.")
            outfile_fail = codecs.open('어린이집별기본정보_수집실패6.txt', 'a')
            fail_url = str(code) + '\n'
            outfile_fail.write(fail_url)
            outfile_fail.close()
        for store in store_list:
            outfile.write(u'%s|' % store['sidoname'])
            outfile.write(u'%s|' % store['sigunname'])
            outfile.write(u'%s|' % store['stcode'])
            outfile.write(u'%s|' % store['crname'])
            outfile.write(u'%s|' % store['crtypename'])
            outfile.write(u'%s|' % store['crstatusname'])
            outfile.write(u'%s|' % store['zipcode'])
            outfile.write(u'%s|' % store['craddr'])
            outfile.write(u'%s|' % store['crtelno'])
            outfile.write(u'%s|' % store['nrtrroomcnt'])
            outfile.write(u'%s|' % store['nrtrroomsize'])
            outfile.write(u'%s|' % store['plgrdco'])
            outfile.write(u'%s|' % store['cctvinstlcnt'])
            outfile.write(u'%s|' % store['chcrtescnt'])
            outfile.write(u'%s|' % store['crcapat'])
            outfile.write(u'%s|' % store['crchcnt'])
            outfile.write(u'%s|' % store['la'])
            outfile.write(u'%s|' % store['lo'])
            outfile.write(u'%s|' % store['crcargbname'])
            outfile.write(u'%s|' % store['crcnfmdt'])
            outfile.write(u'%s|' % store['crpausebegindt'])
            outfile.write(u'%s|' % store['crpauseenddt'])
            outfile.write(u'%s|' % store['crabldt'])
            outfile.write(u'%s|' % store['datastdrdt'])
            outfile.write(u'%s\n' % store['crspec'])

        time.sleep(random.uniform(0.9, 0.8))

    outfile.close()

def getcode6():
    with open('어린이집별기본정보_수집실패5.txt') as data:
        lines = data.read().splitlines()
    code_list = lines
    return  code_list

def getStoreInfo(sidoCode):
    data = []
    url = "http://api.childcare.go.kr/mediate/rest/cpmsapi030/cpmsapi030/request?key=09dd9ce664724e8697e51355e0dbeb07&arcode={}".format(sidoCode)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
    try:
        pageString = requests.get(url, headers = headers, timeout = 10).text
        time.sleep(1)
        print(url)
    except requests.exceptions.ConnectionError:
        print(sidoCode,"해당 코드의 페이지 호출을 실패하여 실패 리스트로 반환합니다.")
    except requests.exceptions.ReadTimeout:
        print(sidoCode, "해당 코드의 페이지 호출을 실패하여 실패 리스트로 반환합니다.")
    else :
        soup = bs4.BeautifulSoup(pageString,'lxml')
        list = soup.find_all('item')
        for info in range(len(list)):
            try:
                sidoname = list[info].find('sidoname').text
            except AttributeError:
                sidoname = ''
            try:
                sigunname = list[info].find('sigunname').text
            except AttributeError:
                sigunname =''
            try:
                stcode = list[info].find('stcode').text
            except AttributeError:
                stcode = ''
            try:
                crname = list[info].find('crname').text
            except AttributeError:
                crname =''
            try:
                crtypename = list[info].find('crtypename').text
            except AttributeError:
                crtypename = ''
            try:
                crstatusname = list[info].find('crstatusname').text
            except AttributeError:
                crstatusname = ''
            try:
                zipcode = list[info].find('zipcode').text
            except AttributeError:
                zipcode = ''
            try:
                craddr = list[info].find('craddr').text
            except AttributeError:
                craddr = ''
            try:
                crtelno = list[info].find('crtelno').text
            except AttributeError:
                crtelno = ''
            try:
                crfaxno = list[info].find('crfaxno').text
            except AttributeError:
                crfaxno = ''
            try:
                nrtrroomcnt = list[info].find('nrtrroomcnt').text
            except AttributeError:
                nrtrroomcnt = ''
            try:
                nrtrroomsize = list[info].find('nrtrroomsize').text
            except AttributeError:
                nrtrroomsize = ''
            try:
                plgrdco = list[info].find('plgrdco').text
            except AttributeError:
                plgrdco = ''
            try:
                cctvinstlcnt = list[info].find('cctvinstlcnt').text
            except AttributeError:
                cctvinstlcnt = ''
            try:
                crcapat = list[info].find('crcapat').text
            except AttributeError:
                crcapat = ''
            try:
                chcrtescnt = list[info].find('chcrtescnt').text
            except AttributeError:
                chcrtescnt = ''
            try:
                crchcnt = list[info].find('crchcnt').text
            except AttributeError:
                crchcnt = ''
            try:
                la = list[info].find('la').text
            except AttributeError:
                la = ''
            try:
                lo = list[info].find('lo').text
            except AttributeError:
                lo = ''
            try:
                crcargbname = list[info].find('crcargbname').text
            except AttributeError:
                crcargbname = ''
            try:
                crcnfmdt = list[info].find('crcnfmdt').text
            except AttributeError:
                crcnfmdt = ''
            try:
                crpausebegindt = list[info].find('crpausebegindt').text
            except AttributeError:
                crpausebegindt = ''
            try:
                crpauseenddt = list[info].find('crpauseenddt').text
            except AttributeError:
                crpauseenddt = ''
            try:
                crabldt = list[info].find('crabldt').text
            except AttributeError:
                crabldt = ''
            try:
                datastdrdt = list[info].find('datastdrdt').text
            except AttributeError:
                datastdrdt = ''
            try:
                crspec = list[info].find('crspec').text
            except AttributeError:
                crspec = ''
            data.append({"sidoname":sidoname,"sigunname":sigunname,"stcode":stcode,"crname":crname,"crtypename":crtypename,
                         "crstatusname":crstatusname,"zipcode":zipcode,"craddr":craddr,"crtelno":crtelno,"crfaxno":crfaxno,
                         "nrtrroomcnt":nrtrroomcnt,"nrtrroomsize":nrtrroomsize,
                         "plgrdco":plgrdco,"cctvinstlcnt":cctvinstlcnt,"chcrtescnt":chcrtescnt,"crcapat":crcapat,"crchcnt":crchcnt,
                         "la":la,"lo":lo,"crcargbname":crcargbname,"crcnfmdt":crcnfmdt,"crpausebegindt":crpausebegindt,"crpauseenddt":crpauseenddt,
                         "crabldt":crabldt,"datastdrdt":datastdrdt,"crspec":crspec})
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

def dup_remove():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\어린이집상세정보_{}.txt'.format(today)
    outfilename2 = '수집결과\\어린이집상세정보_{}_중복제거.txt'.format(today)

    w = open(outfilename2, 'w')
    r = open(outfilename, 'r',encoding='UTF8')
    # 파일에서 읽은 라인들을 리스트로 읽어들임
    lines = r.readlines()
    # Set에 넣어서 중복 제거 후 다시 리스트 변환
    lines = list(set(lines))
    # 리스트 정렬
    # 정렬,중복제거한 리스트 파일 쓰기
    w.write("SIDONAME|SIGUNNAME|STCODE|CRNAME|CRTYPENAME|ZIPCODE|CRADDR|CRTELNO|CRFAXNO|NRTRROOMSIZE|PLGRDCO"
                  "|CCTVINSTLCNT|CHCRTESCNT|LA|LO|CRCARGBNAME|CRCNFMDT|CRPAUSEBEGINDT|CRPAUSEENDDT|CRABLDT|DATASTDRDT|CRSPEC\n")
    for line in lines:
        w.write(line)
    # 파일 닫기
    w.close()
    r.close()
    os.remove(outfilename)
    os.remove('어린이집별기본정보_수집실패.txt')
    os.remove('어린이집별기본정보_수집실패2.txt')
    os.remove('어린이집별기본정보_수집실패3.txt')
    os.remove('어린이집별기본정보_수집실패4.txt')
    os.remove('어린이집별기본정보_수집실패5.txt')
    os.remove('어린이집별기본정보_수집실패6.txt')
    os.rename(outfilename2, outfilename)
main()
main2()
main3()
main4()
main5()
main6()
dup_remove()
