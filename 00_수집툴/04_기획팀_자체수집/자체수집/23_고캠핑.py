import random
import time
import codecs
import requests
import bs4
import os

def main():

    outfile = codecs.open('23_고캠핑.txt', 'w', 'utf-8')
    outfile.write("NAME|ADDR|TELL|CATE|WEATHER|DATE\n")

    url_list = getUrl()

    count = 1
    for url in url_list:
        store_list = getStoreInfo(url)
        print(url, count)
        count+=1
        count_num = count / 500
        if str(count_num).endswith('.0') == True:
            print('대기중'), time.sleep(60)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['cate'])
            outfile.write(u'%s|' % store['weather'])
            outfile.write(u'%s\n' % store['date'])
        # time.sleep(random.uniform(1.2,1.6))
    outfile.close()

def getStoreInfo_list(intPageNo):
    url = "https://www.gocamping.or.kr/bsite/camp/info/list.do?pageUnit=10&searchKrwd=&listOrdrTrget=last_updusr_pnttm&pageIndex={}".format(intPageNo)
    pageString = requests.get(url = url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    try:
        div = bsObj.find_all('div',{"class":"c_list update"})
    except:
        time.sleep(10)
        div = bsObj.find_all('div', {"class": "c_list update"})
    result = []
    for info in div:
        try:
            a = info.find('a')['href']
        except: pass
        else:
            result.append(a)
    return result

def getStore_list_all():
    page = 1
    result = []
    while True:
        result = result + getStoreInfo_list(page)
        print(page)
        if getStoreInfo_list(page) == [] : break
        page+=1
        if page == 50 : time.sleep(60)
        if page == 100 : time.sleep(60)
        time.sleep(random.uniform(1,1.6))
    return result

def getStore_list():
    alllist = getStore_list_all()
    outfile_tv = codecs.open('GoCaming_list.txt', 'a')
    for lists in alllist:
        id_list = str(lists) + '\n'
        outfile_tv.write(id_list)
    outfile_tv.close()

def getUrl():
    with open('GoCaming_list.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    return SearchList

def getStoreInfo(urls):
    result2 = []
    url = 'https://www.gocamping.or.kr/'+urls
    headers = {
        'Cookie': '_ga=GA1.3.1414988089.1627979054; _gid=GA1.3.1502612972.1627979054; JSESSIONID=ECF3DF799894E5181D98F63C4C1319CF; _gat_gtag_UA_52705464_2=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    try :
        pageString = requests.get(url = url, headers = headers).text
        bsObj = bs4.BeautifulSoup(pageString, "html.parser")
        tbody = bsObj.find('tbody')
        tr = tbody.find_all('tr')
        name = bsObj.find('p', {"class": "camp_name"}).text.replace('\n', '').replace('\t', '')
    except:
        result2.append({'name': '상세페이지없음', 'addr': '', 'tell': '', 'cate': '', 'weather': '', 'date': ''})
    else:
        result = []
        for info in tr:
            try:
                th =info.find('th').text.replace('\n','').replace('\t','')
            except:
                th =''
            try:
                td =info.find('td').text.replace('\n','').replace('\t','')
            except:
                td = info.find('a')['href']
            infos = str(th + ' | ' + td)
            result.append(infos)
        addr = str([x for x in result if x.startswith('주소')==True]).replace('[','').replace(']','').replace("'","").replace('주소 | ','')
        tell = str([x for x in result if x.startswith('문의처')==True]).replace('[','').replace(']','').replace("'","").replace('문의처 | ','')
        cate = str([x for x in result if x.startswith('캠핑장 유형')==True]).replace('[','').replace(']','').replace("'","").replace('캠핑장 유형 | ','')
        weather = str([x for x in result if x.startswith('운영기간')==True]).replace('[','').replace(']','').replace("'","").replace('운영기간 | ','')
        date = str([x for x in result if x.startswith('운영일')==True]).replace('[','').replace(']','').replace("'","").replace('운영일 | ','')
        result2.append({'name':name,'addr':addr,'tell':tell,'cate':cate,'weather':weather,'date':date})
    return result2

def dup_remove():
    w = open('23_고캠핑_중복제거.txt', 'w')
    r = open('23_고캠핑.txt', 'r',encoding='UTF8')
    # 파일에서 읽은 라인들을 리스트로 읽어들임
    lines = r.readlines()
    # Set에 넣어서 중복 제거 후 다시 리스트 변환
    lines = list(set(lines))
    # 리스트 정렬
    # 정렬,중복제거한 리스트 파일 쓰기
    w.write("NAME|ADDR|TELL|CATE|WEATHER|DATE\n")
    for line in lines:
        w.write(line)
    # 파일 닫기
    w.close()
    r.close()
    # os.remove('DAUM_TV맛집_간편수집결과.txt')

getStore_list()
main()
dup_remove()