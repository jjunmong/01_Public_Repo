import sys
import time
import codecs
import requests
import random
import json
import bs4

sidolist = {
    '서울': {'강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'},
    '경기': {'고양시 덕양구', '고양시 일산동구', '고양시 일산서구', '과천시', '광명시', '구리시', '군포시', '김포시',
           '남양주시', '동두천시', '부천시 소사구', '부천시 오정구', '부천시 원미구', '성남시 분당구', '성남시 수정구',
           '성남시 중원구', '수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구', '시흥시', '안산시', '안성시',
           '안양시 동안구', '안양시 만안구', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시', '평택시', '하남시', '가평군', '광주시', '양주시', '양평군', '여주군', '연천군', '안포천군', '화성시', '포천시'},
    '인천': {'계양구', '남구', '남동구', '동구', '부평구', '서구', '연수구', '중구', '강화군', '옹진군'},
    '강원': {'동해시', '삼척시', '속초시', '원주시', '춘천시', '태백시', '고성군', '양구군', '양양군', '영월군', '인제군', '정선군', '철원군', '평창군', '홍천군', '화천군', '횡성군'},
    '충북': {'제천시', '청주시 상당구', '청주시 흥덕구', '청주시 청원구', '충주시', '괴산군', '단양군', '보은군', '영동군', '옥천군', '음성군', '진천군', '증평군', '청원군'},
    '충남': {'공주시', '논산시', '보령시', '서산시', '아산시', '천안시', '계룡시', '금산군', '당진시', '부여군', '서천군', '연기군', '예산군', '청양군', '태안군', '홍성군'},
    '대전': {'대덕구', '동구', '서구', '유성구', '중구'},
    '경북': {'경산시', '경주시', '구미시', '김천시', '문경시', '상주시', '안동시', '영주시', '영천시', '포항시 남구', '포항시 북구', '고령군', '군위군', '봉화군', '성주군', '영덕군', '영양군', '예천군', '울릉군', '울진군', '의성군', '청도군', '양청송군', '칠곡군'},
    '경남': {'거제시', '김해시', '밀양시', '사천시', '양산시', '진주시', '창원시 의창구', '창원시 성산구', '창원시 마산합포구', '창원시 마산회원구', '창원시 진해구', '통영시', '거창군', '고성군', '남해군', '산청군', '의령군', '창녕군', '하동군', '함안군', '함양군', '합천군'},
    '대구': {'남구', '달서구', '동구', '북구', '서구', '수성구', '중구', '달성군'},
    '울산': {'남구', '동구', '북구', '중구', '울주군'},
    '전북': {'군산시', '김제시', '남원시', '익산시', '전주시 덕진구', '전주시 완산구', '정읍시', '고창군', '무주군', '부안군', '순창군', '완주군', '임실군', '장수군', '진안군'},
    '전남': {'광양시', '나주시', '목포시', '순천시', '여수시', '강진군', '고흥군', '곡성군', '구례군', '담양군', '무안군', '보성군', '신안군', '영광군', '영암군', '완도군', '장성군', '장흥군', '진도군', '함평군', '해남군', '화순군'},
    '광주': {'광산구', '남구', '동구', '북구', '서구'},
    '부산': {'강서구', '금정구', '남구', '동구', '동래구', '진구', '북구', '사상구', '사하구', '서구', '수영구', '연제구', '영도구', '중구', '해운대구', '기장군'},
    '세종': {'세종시'},
    '제주': {'서귀포시', '제주시', '남제주군', '북제주군' }
}

def main():

    outfile = codecs.open('52_커브스.txt', 'w', 'utf-8')
    outfile.write("BRANCH|ADDR||TELL\n")

    for sidoname in sidolist:

        gugunlist = sidolist[sidoname]

        for gugunname in gugunlist:

            storeList = getStorelInfo(sidoname, gugunname)

            for store in storeList:
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s\n' % store['tell'])

            time.sleep(random.uniform(0.7, 0.9))

    outfile.close()

def getStorelInfo(sidoname, gugunname):
    url = 'http://www.curveskorea.co.kr/club-locator/_php/si_do_ajax.php'
    params = {}
    params['sido_name'] = sidoname
    params['gungu_name']=gugunname
    pageString = requests.get(url, params = params).text
    print(url, sidoname, gugunname)
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('a')
    result = []
    for info in li:
        branch = info.find('span',{"class":"result_title"}).text
        infos = info.find('span',{"class":"addr"})
        infos = str(infos).split('<br/>')
        addr = sidoname + ' ' + gugunname + ' ' + infos[0].replace('<span class="addr">','')
        tell = infos[1].replace('</span>','')
        result.append({"branch": branch, "addr": addr, "tell": tell})

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
