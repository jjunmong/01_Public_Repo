import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('77_농협은행.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|CAT|XCODR|YCORD\n")
    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if page == 100 : time.sleep(300)
        if page == 200: time.sleep(300)
        if page == 300: time.sleep(300)
        if page == 400: time.sleep(300)
        if page == 500: time.sleep(300)
        if page == 900 : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['cat'])
            outfile.write(u'%s|' % store['cordx'])
            outfile.write(u'%s\n' % store['cordy'])
        page += 1
        if len(store_list) < 8:
            for store in store_list:
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['tell'])
                outfile.write(u'%s|' % store['cat'])
                outfile.write(u'%s|' % store['cordx'])
                outfile.write(u'%s\n' % store['cordy'])
                break
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

    w = open('77_농협은행_중복제거.txt', 'w')
    r = open('77_농협은행.txt', 'r',encoding='UTF8')
    # 파일에서 읽은 라인들을 리스트로 읽어들임
    lines = r.readlines()
    # Set에 넣어서 중복 제거 후 다시 리스트 변환
    lines = list(set(lines))
    # 리스트 정렬
    # 정렬,중복제거한 리스트 파일 쓰기
    w.write("NAME|BRANCH|ADDR|TELL|CAT|XCODR|YCORD\n")
    for line in lines:
        w.write(line)
    # 파일 닫기
    w.close()
    r.close()

def getStoreInfo(intpageNo):
    url = 'http://nonghyup.ttmap.co.kr/list_branch_2017.jsp'
    data ={
        'tab': '1',
        # 'pg': '2',
        'search_word': '',
        'search_type': '1',
        'search_classify': '1',
        'list_tab': '',
        'sido': '',
        'sigungu': '',
        'region_name': '',
        'b_code': '',
        'x': '',
        'y': '',
        'classify': '1',
        'src_by_brname': '',
        'select_sido': '',
        'select_sigungu': '',
        'src_by_addr': '',
        'src_by_subway': '',
        'classify_ATM': '1',
        'src_by_brname': '',
        'select_sido': '',
        'select_sigungu': '',
        'src_by_addr': '',
        'src_by_subway': '',
        'select_hanaroclub': '1',
        'select_hanaroclub_area': '0',
        'select_hanaromart_sido': '',
        'select_nhoil_area': '',
        'select_nhoil_refinery': '0',
        'src_by_nhoil': '',
        'select_commonstore_area': '0',
        'select_factory_sido': '',
        'select_rpc_sido': '',
        'select_material_sido': '',
        'select_headquarter': '1',
        'select_hq': '0',
        'select_education': '0',
        'select_relative': '0',
    }
    data['pg'] = intpageNo
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '559',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=02246E97578E7B248D5438AFC2E8CF08',
        'Host': 'nonghyup.ttmap.co.kr',
        'Origin': 'http://nonghyup.ttmap.co.kr',
        'Referer': 'http://nonghyup.ttmap.co.kr/main.jsp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data['pageNo'] = intpageNo
    pageString = requests.post(url,data =data, headers = headers)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    div = bsObj.find('div',{"id":"result_list"})
    li = div.find_all('li')
    script = bsObj.find_all('script')
    result = []
    for info1, info2 in zip(li, script):
        names = info1.find('a').text
        try:
            name = names.split(' ')[0].upper()
        except :
            name = names
        try:
            branch = names.split(' ')[1].upper()
        except :
            branch = ''
        try:
            addr = info1.find('p',{"class":"list_addr"}).text.replace('\n\t\t\t\t\t','')
        except:
            addr = ''
        try:
            tell = info1.find('p',{"class":"list_telno"}).text
        except:
            tell = ''
        try:
            cat = info1.find('span',{"class":"bank_type_nhbank"}).text
        except :
            cat = ''

        cord = str(info2).split('new daum.maps.LatLng(')[1]
        cord = str(cord).split(',')
        cordy = str(cord[0]).replace('));\t\t\t\t\n\t\t\t</script>','')
        cordx = str(cord[1]).replace('));\t\t\t\t\n\t\t\t</script>','')

        result.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"cat":cat,"cordx":cordx,"cordy":cordy})

    return result



def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()