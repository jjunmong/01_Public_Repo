import requests
import datetime
import time
from selenium import webdriver
import os
import getpass
import shutil

def download_addrDB():
    today = datetime.date.today()
    month_origin = today.month
    if len(str(month_origin)) < 2 : month = '0'+str(month_origin)
    else : month = str(month_origin)
    year = str(today.year)
    fulldate = year+month
    url = "https://www.juso.go.kr/dn.do?reqType=ALLMTCHG&regYmd={}&ctprvnCd=00&gubun=MTCH&stdde={}&fileName={}_%EC%A3%BC%EC%86%8CDB_%EC%A0%84%EC%B2%B4%EB%B6%84.zip&realFileName={}ALLMTCHG00.zip&indutyCd=999&purpsCd=999&indutyRm=%EC%88%98%EC%A7%91%EC%A2%85%EB%A3%8C&purpsRm=%EC%88%98%EC%A7%91%EC%A2%85%EB%A3%8C".format(year,fulldate,fulldate,fulldate)
    response_text = requests.get(url).text
    if '파일을 찾을 수 없습니다' in response_text :
        print('도로명주소DB_ 이번 달 데이터 없음 , 이전 달로 재 호출')
        month_origin = today.month - 1
        if len(str(month_origin)) < 2: month = '0' + str(month_origin)
        else : month = str(month_origin)
        year = str(today.year)
        fulldate = year + month
        filename = '건물DB_{}.zip'.format(fulldate)
        url = "https://www.juso.go.kr/dn.do?reqType=ALLMTCHG&regYmd={}&ctprvnCd=00&gubun=MTCH&stdde={}&fileName={}_%EC%A3%BC%EC%86%8CDB_%EC%A0%84%EC%B2%B4%EB%B6%84.zip&realFileName={}ALLMTCHG00.zip&indutyCd=999&purpsCd=999&indutyRm=%EC%88%98%EC%A7%91%EC%A2%85%EB%A3%8C&purpsRm=%EC%88%98%EC%A7%91%EC%A2%85%EB%A3%8C".format(year, fulldate, fulldate, fulldate)
        with open(filename, "wb") as file:
            response = requests.get(url)
            file.write(response.content)
            print('도로명주소DB_ 다운로드 완료')
    else:
        print('도로명주소DB_ 이번 달 데이터 존재 , 다운로드 진행.')
        filename = '건물DB_{}.zip'.format(fulldate)
        with open(filename, "wb") as file:
            response = requests.get(url)
            file.write(response.content)
            print('도로명주소DB_ 다운로드 완료')

def download_buldDB():
    today = datetime.date.today()
    month_origin = today.month
    if len(str(month_origin)) < 2 : month = '0'+str(month_origin)
    else : month = str(month_origin)
    year = str(today.year)
    fulldate = year+month
    url = "https://www.juso.go.kr/dn.do?reqType=ALLRDNM&regYmd={}&ctprvnCd=00&gubun=RDNM&stdde={}&fileName={}_%EA%B1%B4%EB%AC%BCDB_%EC%A0%84%EC%B2%B4%EB%B6%84.zip&realFileName={}ALLRDNM00.zip&indutyCd=999&purpsCd=999&indutyRm=%EC%88%98%EC%A7%91%EC%A2%85%EB%A3%8C&purpsRm=%EC%88%98%EC%A7%91%EC%A2%85%EB%A3%8C".format(year,fulldate,fulldate,fulldate)
    response_text = requests.get(url).text
    if '파일을 찾을 수 없습니다' in response_text :
        print('건물DB_ 이번 달 데이터 없음 , 이전 달로 재 호출')
        month_origin = today.month - 1
        if len(str(month_origin)) < 2: month = '0' + str(month_origin)
        else : month = str(month_origin)
        year = str(today.year)
        fulldate = year + month
        filename = '건물DB_{}.zip'.format(fulldate)
        url = "https://www.juso.go.kr/dn.do?reqType=ALLRDNM&regYmd={}&ctprvnCd=00&gubun=RDNM&stdde={}&fileName={}_%EA%B1%B4%EB%AC%BCDB_%EC%A0%84%EC%B2%B4%EB%B6%84.zip&realFileName={}ALLRDNM00.zip&indutyCd=999&purpsCd=999&indutyRm=%EC%88%98%EC%A7%91%EC%A2%85%EB%A3%8C&purpsRm=%EC%88%98%EC%A7%91%EC%A2%85%EB%A3%8C".format(year, fulldate, fulldate, fulldate)
        with open(filename, "wb") as file:
            response = requests.get(url)
            file.write(response.content)
            print('건물DB_ 다운로드 완료')
    else:
        print('건물DB_ 이번 달 데이터 존재 , 다운로드 진행.')
        filename = '건물DB_{}.zip'.format(fulldate)
        with open(filename, "wb") as file:
            response = requests.get(url)
            file.write(response.content)
            print('건물DB_ 다운로드 완료')

def download_PObox():
    today = datetime.date.today()
    month = today.month
    month_check = month / 2
    try:
        if str(month_check).endswith('.0') : month = int(month/2)
        else : month = int(month/2)+ 1
        print(month)
        chromedriver_dir = r'C:\chromedriver.exe'
        driver = webdriver.Chrome(chromedriver_dir)
        driver.get('https://www.juso.go.kr/addrlink/addressBuildDevNew.do?menu=post')
        time.sleep(1)
        element = '//*[@id="monthPostAllDownNum"]/a[{}]'.format(month)
        print(element)
        click_list = driver.find_element_by_xpath(element)
        driver.execute_script("arguments[0].click();", click_list)
        time.sleep(3)
    except :
        if str(month_check).endswith('.0') : month = int(month/2)
        else : month = int(month/2)-1
        print(month)
        chromedriver_dir = r'C:\chromedriver.exe'
        driver = webdriver.Chrome(chromedriver_dir)
        driver.get('https://www.juso.go.kr/addrlink/addressBuildDevNew.do?menu=post')
        time.sleep(1)
        element = '//*[@id="monthPostAllDownNum"]/a[{}]'.format(month)
        print(element)
        click_list = driver.find_element_by_xpath(element)
        driver.execute_script("arguments[0].click();", click_list)
        time.sleep(3)

    getuser = getpass.getuser()
    origin_dir = r'C:\Users\{}\Downloads'.format(getuser)
    current_dir = os.getcwd()
    file_list = os.listdir(origin_dir)
    file_name = ''
    for s in file_list:
        if s.endswith('_사서함주소DB_전체분') == True:
            file_name = s

    origin_file = origin_dir + '\\' + file_name
    copy_file = current_dir + '\\수집결과\\' + file_name
    shutil.copy(origin_file, copy_file)
    os.remove(origin_file)
    print('사서함DB_ 다운로드 완료')

download_addrDB()
download_buldDB()
download_PObox()