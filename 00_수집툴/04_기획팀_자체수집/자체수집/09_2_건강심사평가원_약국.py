import time
import codecs
import requests
import random
import bs4
from datetime import datetime

def main():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\약국_{}.txt'.format(today)

    outfile = codecs.open(outfilename, 'w', 'utf-8')
    sido_code = ['110000','210000','220000','230000','240000','250000','260000','410000','310000','320000','330000','340000','350000','360000','370000','380000','390000']
    for sido in sido_code:
        page = 1
        while True :
            result = getStoreInfo(sido, page)
            if result == [] : break
            for store in result:
                outfile.write(u'%s|' % store['yadNm'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['clcd'])
                outfile.write(u'%s|' % store['emdongnm'])
                outfile.write(u'%s|' % store['estbdd'])
                outfile.write(u'%s|' % store['gdrCnt'])
                outfile.write(u'%s|' % store['intnCnt'])
                outfile.write(u'%s|' % store['postNo'])
                outfile.write(u'%s|' % store['resdntNct'])
                outfile.write(u'%s|' % store['sdrCnt'])
                outfile.write(u'%s|' % store['sgguCd'])
                outfile.write(u'%s|' % store['sgguCdNm'])
                outfile.write(u'%s|' % store['sidoCd'])
                outfile.write(u'%s|' % store['sidoCdNm'])
                outfile.write(u'%s|' % store['telno'])
                outfile.write(u'%s|' % store['XPos'])
                outfile.write(u'%s|' % store['YPos'])
                outfile.write(u'%s\n' % store['ykiho'])
            page += 1
            if page == 100 : break
            time.sleep(random.uniform(0.3, 0.9))
    outfile.close()

def getStoreInfo(sidoCode, intPageNo):
    url = "http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList"
    querystring = {"serviceKey":"fdBIIF1vASwjtUTGKzimsdOegcu7mQMFdyIba/JeymvRkGmib9WbfhD9X/hh3ruQLQWvqtD5l9p4KEihyi1Hrw=="}
    querystring['pageNo'] = intPageNo
    querystring['numOfRows']= '1000'
    querystring['sidoCd'] = sidoCode
    try:
        response = requests.request("GET", url, params=querystring).text
        print(url,querystring)
    except requests.exceptions.ConnectionError:
        print(intPageNo, "해당 코드의 페이지 호출을 실패하여 실패 리스트로 반환합니다.")
        outfile = codecs.open('건강심사평가원_약국_수집실패.txt', 'a')
        fail_url = str(intPageNo) + '\n'
        outfile.write(fail_url)
        outfile.close()
    soup = bs4.BeautifulSoup(response,'lxml')
    list = soup.find_all('item')
    data = []
    for info in range(len(list)):
        try:
            yadmnm = list[info].find('yadmnm').text
        except AttributeError:
            yadmnm = ''
        try:
            addr = list[info].find('addr').text
        except AttributeError:
            addr =''
        try:
            clcd = list[info].find('clcd').text
        except AttributeError:
            clcd = ''
        try:
            emdongnm = list[info].find('emdongnm').text
        except AttributeError:
            emdongnm =''
        try:
            estbdd = list[info].find('estbdd').text
        except AttributeError:
            estbdd = ''
        try:
            gdrcnt = list[info].find('gdrcnt').text
        except AttributeError:
            gdrcnt = ''
        try:
            intncnt = list[info].find('intncnt').text
        except AttributeError:
            intncnt = ''
        try:
            postno = list[info].find('postno').text
        except AttributeError:
            postno = ''
        try:
            resdntnct = list[info].find('resdntnct').text
        except AttributeError:
            resdntnct = ''
        try:
            sdrcnt = list[info].find('sdrcnt').text
        except AttributeError:
            sdrcnt = ''
        try:
            sggucd = list[info].find('sggucd').text
        except AttributeError :
            sggucd = ''
        try :
            sggucdnm = list[info].find('sggucdnm').text
        except AttributeError:
            sggucdnm = ''
        try:
            sidocd = list[info].find('sidocd').text
        except AttributeError:
            sidocd =''
        try:
            sidocdnm = list[info].find('sidocdnm').text
        except AttributeError:
            sidocdnm = ''
        try:
            telno = list[info].find('telno').text
        except AttributeError:
            telno = ''
        try:
            xpos = list[info].find('xpos').text
        except AttributeError:
            xpos = ''
        try:
            ypos = list[info].find('ypos').text
        except AttributeError:
            ypos =''
        try :
            ykiho = list[info].find('ykiho').text
        except AttributeError:
            ykiho : ''
        data.append({"yadNm":yadmnm,"addr":addr,"clcd":clcd,"emdongnm":emdongnm,"estbdd":estbdd,"gdrCnt":gdrcnt,"intnCnt":intncnt,"postNo":postno,"resdntNct":resdntnct
                     ,"sdrCnt":sdrcnt,"sgguCd":sggucd,"sgguCdNm":sggucdnm,"sidoCd":sidocd,"sidoCdNm":sidocdnm,"telno":telno,"XPos":xpos,"YPos":ypos,"ykiho":ykiho})
    return data

def dup_remove():
    w = open('심평원_약국_중복제거.txt', 'w')
    r = open('심평원_약국.txt', 'r',encoding='UTF8')
    # 파일에서 읽은 라인들을 리스트로 읽어들임
    lines = r.readlines()
    # Set에 넣어서 중복 제거 후 다시 리스트 변환
    lines = list(set(lines))
    # 리스트 정렬
    # 정렬,중복제거한 리스트 파일 쓰기
    w.write("YADNM|ADDR|CLCD|EMDONGNM|ESTBDD|GDRCNT|INTNCNT|POSTNO|RESDNTNCT|SDRCNT|SGGUCD|SGGUCDNM|SIDOCD|SIDOCDNM|TELNO|XPOS|YPOS|YKIHO\n")
    for line in lines:
        w.write(line)
    # 파일 닫기
    w.close()
    r.close()
    # os.remove('DAUM_TV맛집_간편수집결과.txt')

main()
dup_remove()

# 2020-03-19  : 구분자 오류로 툴 수정 후 배포
# 2020-04-08 : 중복 및 누락 분 발생으로 시도코드 삽입, 중복제거 프로세스 추가
# 2020-09-10 : 누락 발생으로 시도코드 정비, 재 수집 결과 이상 없음.