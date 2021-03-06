import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import codecs
import requests
import random
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\03_1_S-OIL\\') == False : os.makedirs('수집결과\\03_1_S-OIL\\')
outfilename = '수집결과\\03_1_S-OIL\\S-OIL_{}.txt'.format(today)
outfilename_true = '수집결과\\03_1_S-OIL\\S-OIL_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\03_1_S-OIL\\S-OIL_{}.log_실패.txt'.format(today)

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
    code_list = getStore_List_all()
    for code in code_list:
        store_list = getStoreInfo(code)
        print(code)
        for store in store_list:
            outfile.write(u'%s|' % store['code'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s\n' % store['truck'])
        time.sleep(random.uniform(2, 3))
    outfile.close()
    time.sleep(600)
    outfile = codecs.open(outfilename, 'a', 'utf-8')
    code_list = getStore_List_all2()
    for code in code_list:
        store_list = getStoreInfo(code)
        print(code)
        for store in store_list:
            outfile.write(u'%s|' % store['code'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s\n' % store['truck'])
        time.sleep(random.uniform(2, 3))
    outfile.close()
    time.sleep(600)
    outfile = codecs.open(outfilename, 'a', 'utf-8')
    code_list = getStore_List_all3()
    for code in code_list:
        store_list = getStoreInfo(code)
        print(code)
        for store in store_list:
            outfile.write(u'%s|' % store['code'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s\n' % store['truck'])
        time.sleep(random.uniform(2, 3))
    outfile.close()
    time.sleep(600)
    outfile = codecs.open(outfilename, 'a', 'utf-8')
    code_list = getStore_List_all4()
    for code in code_list:
        store_list = getStoreInfo(code)
        print(code)
        for store in store_list:
            outfile.write(u'%s|' % store['code'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s|' % store['ycord'])
            outfile.write(u'%s\n' % store['truck'])
        time.sleep(random.uniform(2, 3))
    outfile.close()

def getStore_List_all():
    chromedriver_dir = r'C:\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)
    driver.get('https://www.s-oilbonus.com/2013/station/station/search.jsp?chainid=22&si_do_nm=&gu_gun_nm=&oiltype=&si_do=&gu_gun=&oil_name=')
    time.sleep(random.uniform(4,5))
    result = []
    for page in range(1,51):
        print(page)
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tr = soup.find_all('tr')
        for info in tr:
            try:
                code = str(info.find('a')['onclick']).replace("mapPop('","").replace("');return false;","")
            except:pass
            else:
                result.append(code)
        try:
            click_list = driver.find_element(By.XPATH,'//*[@id="container"]/ul[2]/li[13]/a/img')
            driver.execute_script("arguments[0].click();", click_list)
        except :
            click_list = driver.find_element(By.XPATH,'//*[@id="container"]/ul[2]/li[11]/a/img')
            driver.execute_script("arguments[0].click();", click_list)
    driver.close()
    return result

def getStore_List_all2():
    chromedriver_dir = r'C:\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)
    driver.get('https://www.s-oilbonus.com/2013/station/station/search.jsp?si_do=&oil_name=&si_do_nm=&chainid=22&oiltype=&gu_gun_nm=&gu_gun=&page=50')
    time.sleep(random.uniform(4,5))
    result = []
    for page in range(1,51):
        print(page)
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tr = soup.find_all('tr')
        for info in tr:
            try:
                code = str(info.find('a')['onclick']).replace("mapPop('","").replace("');return false;","")
            except:pass
            else:
                result.append(code)
        try:
            try:
                click_list = driver.find_element(By.XPATH,'//*[@id="container"]/ul[2]/li[13]/a/img')
                driver.execute_script("arguments[0].click();", click_list)
            except :
                click_list = driver.find_element(By.XPATH,'//*[@id="container"]/ul[2]/li[11]/a/img')
                driver.execute_script("arguments[0].click();", click_list)
        except : pass
    driver.close()
    return result

def getStore_List_all3():
    chromedriver_dir = r'C:\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)
    driver.get('https://www.s-oilbonus.com/2013/station/station/search.jsp?si_do=&oil_name=&si_do_nm=&chainid=22&oiltype=&gu_gun_nm=&gu_gun=&page=100')
    time.sleep(random.uniform(4,5))
    result = []
    for page in range(1,51):
        print(page)
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tr = soup.find_all('tr')
        for info in tr:
            try:
                code = str(info.find('a')['onclick']).replace("mapPop('","").replace("');return false;","")
            except:pass
            else:
                result.append(code)
        try:
            try:
                click_list = driver.find_element(By.XPATH,'//*[@id="container"]/ul[2]/li[13]/a/img')
                driver.execute_script("arguments[0].click();", click_list)
            except :
                click_list = driver.find_element(By.XPATH,'//*[@id="container"]/ul[2]/li[11]/a/img')
                driver.execute_script("arguments[0].click();", click_list)
        except : pass
    driver.close()
    return result

def getStore_List_all4():
    chromedriver_dir = r'C:\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)
    driver.get('https://www.s-oilbonus.com/2013/station/station/search.jsp?si_do=&oil_name=&si_do_nm=&chainid=22&oiltype=&gu_gun_nm=&gu_gun=&page=150')
    time.sleep(random.uniform(4,5))
    result = []
    for page in range(1,51):
        time.sleep(1)
        print(page)
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tr = soup.find_all('tr')
        for info in tr:
            try:
                code = str(info.find('a')['onclick']).replace("mapPop('","").replace("');return false;","")
            except:pass
            else:
                result.append(code)
        try:
            try:
                click_list = driver.find_element(By.XPATH,'//*[@id="container"]/ul[2]/li[13]/a/img')
                driver.execute_script("arguments[0].click();", click_list)
            except :
                try:
                    click_list = driver.find_element(By.XPATH,'//*[@id="container"]/ul[2]/li[11]/a/img')
                    driver.execute_script("arguments[0].click();", click_list)
                except :
                    click_list = driver.find_element(By.XPATH,'//*[@id="container"]/ul[2]/li[12]/a/img')
                    driver.execute_script("arguments[0].click();", click_list)
        except : pass
    driver.close()
    return result

def getStoreInfo(code):
    url = 'https://www.s-oilbonus.com/map/stationResult.jsp'
    data = {
        'result_cd': 'V',
        'type': '3',
        # 'code': 'A12340',
    }
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '30',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'SCOUTER=z3srq8b5js56gp; JSESSIONID=sz9FD19nmn6qrlDpLg5XphW0tsVWct5Ml9en1nqifXVaXzWyVt9E80VW9wBaxcpI.Ym9udXNfZG9tYWluMS9ib251c2NhcmQy; TS014d7408=0151822b2dc145a0aa01cd7ad5f72e55ddf785d4ed2780cbc661aed15e355016cc1219c969dabf6d20bd215ad2960d9e1dd328e638049c6f6056723301e6b2bc4f39b5da1917e3b34e4ccd5b78d9676ed07bab6756',
        'Host': 'www.s-oilbonus.com',
        'Origin': 'https://www.s-oilbonus.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.s-oilbonus.com/map/snb.jsp',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data['code'] = code
    pageString = requests.post(url, data = data, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    result = []
    try:
        code = code
        branch = str(bsObj.select('td')[0]).replace('<td class="brn">','').replace('</td>','')
        addr = str(bsObj.select('td')[1]).replace('<td class="brn">','').replace('</td>','')
        tell = str(bsObj.select('td')[2]).replace('<td class="brn">','').replace('</td>','')
        cord = str(bsObj.find('a')['href']).split(',')
        xcord = cord[2]
        ycord = cord[1]
        try:
            truck = bsObj.find('img',{"src":"/map/images/icon_07.gif"})['alt']
        except : truck = ''
    except:pass
    else:
        result.append({'code':code,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord,'truck':truck})
    return result

def dup_remove():
    outfilename_dupRemove = '수집결과\\03_1_S-OIL\\S-OIL_중복제거.txt'
    w = open(outfilename_dupRemove, 'w')
    r = open(outfilename, 'r',encoding='UTF8')
    # 파일에서 읽은 라인들을 리스트로 읽어들임
    lines = r.readlines()
    # Set에 넣어서 중복 제거 후 다시 리스트 변환
    lines = list(set(lines))
    # 리스트 정렬
    # 정렬,중복제거한 리스트 파일 쓰기
    w.write("CODE|BRANCH|ADDR|TELL|XOCRD|YCORD|TRUCK\n")
    for line in lines:
        w.write(line)
    # 파일 닫기
    w.close()
    r.close()
    os.remove(outfilename)
    os.rename(outfilename_dupRemove,outfilename)

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()