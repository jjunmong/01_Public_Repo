import sys
import requests
import codecs
import bs4
import os

def main():
    outfile = codecs.open('84_영화진흥위원회.txt', 'w', 'utf-8')
    outfile.write("NAME|ADDR|TELL|STATE\n")

    code_list = getStoreInfoIdList()
    for code in code_list:
        store_list = getStoreInfo(code['code'], code['state'])
        print(code['code'],code['state'])
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s\n' % store['state'])
    outfile.close()

def getStoreInfoIdList():
    result = []
    maxPage = int(getStoreInfoId(1)[1] / 10 + 1)
    print('최대 수집 페이지 :',maxPage)
    page =1
    while True:
        if page == maxPage: break
        result = result + getStoreInfoId(page)[0]
        print(page)
        page+=1
    return result

def getStoreInfoId(intPageNo):
    url = 'https://www.kobis.or.kr/kobis/business/mast/thea/findTheaterInfoList.do'
    data ={
        'CSRFToken': '9WRCALUlRBb5yQKRj30Ejsg4BRXRBhqZzU8JVY2lLtw',
        # 'pageIndex': '1',
        'theaCd': '',
        'sTheaNm': '',
        'sTheaCd': '',
        'sPermYn': 'Y',
        'sJoinYn': 'Y',
        'sWideareaCd': '',
        'sBasareaCd': '',
        'sSaleStat': '',
        'sSenderCd': '',
        'CSRFToken': '9WRCALUlRBb5yQKRj30Ejsg4BRXRBhqZzU8JVY2lLtw',
    }
    data['pageIndex']=intPageNo
    try:
        pageString = requests.post(url,data =data).text
        bsObj = bs4.BeautifulSoup(pageString,"html.parser")
        tbody = bsObj.find('tbody').find_all('tr')
        totalcount = int(bsObj.find('em',{"class":"fwb"}).text.replace('총 ','').replace('건',''))
        state = bsObj.find('td',{"class":"last-child"}).text
    except:
        return []
    result = []
    for info in tbody:
        a = info.find('a')['onclick'].split(',')[2].strip().replace(');return false;','').replace("'","")
        result.append({'code':a,'state':state})
    return result, totalcount

def getStoreInfo(storeCode,state):
    url = 'https://www.kobis.or.kr/kobis/business/mast/thea/findTheaterCodeLayer.do?theaCd={}'.format(storeCode)
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    name = bsObj.find('strong',{"class":"tit"}).text
    tell = bsObj.select_one('#pop_content02 > table.tbl_99 > tbody > tr:nth-child(2) > td:nth-child(2)').text.replace('\r','').replace('\n','').replace('\t','').strip()
    addr = bsObj.select_one('#pop_content02 > table.tbl_99 > tbody > tr:nth-child(4) > td').text.replace('\r','').replace('\n','').replace('\t','').strip()
    result.append({'name': name, 'addr': addr, 'tell': tell,'state':state})
    return result

def dup_remove():
    outfilename_dupRemove = '84_영화진흥위원회_중복제거.txt'
    w = open(outfilename_dupRemove, 'w')
    r = open('84_영화진흥위원회.txt', 'r',encoding='UTF8')
    # 파일에서 읽은 라인들을 리스트로 읽어들임
    lines = r.readlines()
    # Set에 넣어서 중복 제거 후 다시 리스트 변환
    lines = list(set(lines))
    # 리스트 정렬
    # 정렬,중복제거한 리스트 파일 쓰기
    w.write("NAME|ADDR|TELL|STATE\n")
    for line in lines:
        w.write(line)
    # 파일 닫기
    w.close()
    r.close()
    os.remove('84_영화진흥위원회.txt')
    os.rename(outfilename_dupRemove,'84_영화진흥위원회.txt')

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()