import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import getpass
import zipfile
import datetime
import pandas as pd
import codecs
from datetime import datetime
import traceback
import os, sys

today = str(datetime.today()).split(' ')[0].replace('-', '')

outfilename = '수집결과\\17_1_건축인허가\\건축인허가_{}.txt'.format(today)
outfilename_true = '수집결과\\17_1_건축인허가\\건축인허가_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\17_1_건축인허가\\건축인허가_{}.log_실패.txt'.format(today)

def main():
    try:
        Crawl_run()
        file_edit()
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
    chromedriver_dir = r'C:\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)
    driver.get('https://open.eais.go.kr/main/main.do')
    time.sleep(5)

    login_click = driver.find_element(By.XPATH,'//*[@id="header"]/div[3]/div[1]/ul/li/a/img')
    driver.execute_script("arguments[0].click();", login_click)
    time.sleep(5)

    idInput = driver.find_element(By.XPATH,'//*[@id="membId"]')
    idInput.clear()
    idInput.send_keys("seolyh1005")
    time.sleep(2)

    passInput = driver.find_element(By.XPATH,'//*[@id="pwd"]')
    passInput.clear()
    passInput.send_keys("Wnsdud8787!")
    time.sleep(5)

    login_button = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/div[1]/div[1]/button')
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(20)

    menu1 = driver.find_element(By.XPATH,'//*[@id="gnb_menu_1"]')
    driver.execute_script("arguments[0].click();", menu1)
    time.sleep(2)

    menu2 = driver.find_element(By.XPATH,'//*[@id="menu_d6"]/h4')
    driver.execute_script("arguments[0].click();", menu2)
    time.sleep(2)

    click_list = driver.find_element(By.XPATH,'//*[@id="menu_d6"]/h4')
    driver.execute_script("arguments[0].click();", click_list)
    time.sleep(1)

    click_list2 = driver.find_element(By.XPATH,'//*[@id="searchCondition"]')
    driver.execute_script("arguments[0].click();", click_list2)
    time.sleep(1)

    select = Select(driver.find_element(By.ID,'searchCondition'))
    select.select_by_visible_text('건축인허가')
    select.select_by_value('01')
    time.sleep(1)

    serch_text = driver.find_element(By.XPATH,'//*[@id="searchKeyword"]')
    serch_text.clear()
    serch_text.send_keys("기본개요")
    time.sleep(1)

    click_list3 = driver.find_element(By.XPATH,'//*[@id="boardMasivDataVO"]/div[4]/span/a')
    driver.execute_script("arguments[0].click();", click_list3)
    time.sleep(1)

    down_click = driver.find_element(By.XPATH,'//*[@id="boardMasivDataVO"]/div[5]/table/tbody/tr[2]/td[7]/span/a')
    driver.execute_script("arguments[0].click();", down_click)

    down_click1 = driver.find_element(By.XPATH,'//*[@id="rad0"]')
    driver.execute_script("arguments[0].click();", down_click1)

    down_click2 = driver.find_element(By.XPATH,'//*[@id="btnOk"]')
    driver.execute_script("arguments[0].click();", down_click2)

    time.sleep(480)

def file_edit():
    getuser = getpass.getuser()
    origin_dir = r'C:\Users\{}\Downloads'.format(getuser)
    file_list = os.listdir(origin_dir)
    Zipfile_name = ''
    for s in file_list:
        if s.startswith('국토교통부_건축인허가_기본개요') == True :
            Zipfile_name = s

    zip_fullpath = origin_dir+'\\'+Zipfile_name
    zip_fullpath = r'{}'.format(zip_fullpath)
    print(zip_fullpath)
    zipfile.ZipFile(zip_fullpath).extractall()

    with open('mart_kcy_01.txt') as data:
        lines = data.read().splitlines()
    basic_row = lines

    today = str(datetime.date.today()).replace('-','')
    file_name = '건축인허가_월별확인대상_'+today+'.txt'
    file_open = codecs.open(file_name, 'w')
    file_open.write('관리_허가대장_PK|대지_위치|건물_명|시군구_코드|법정동_코드|대지_구분_코드|번|지|특수지_명|블록|로트|지목_코드_명|지역_코드_명|지구_코드_명|구역_코드_명|지목_코드|지역_코드|지구_코드|구역_코드|건축_구분_코드|건축_구분_코드_명|대지_면적|건축_면적|'
                    '건폐_율|연면적|용적_률_산정_연면적|용적_률|주_건축물_수|부속_건축물_동_수|주_용도_코드|주_용도_코드_명|세대_수|호_수|가구_수|총_주차_수|착공_예정_일|착공_연기_일|실제_착공_일|건축_허가_일|사용승인_일|생성_일자\n')
    for line in basic_row:
        file_open.write(line+'\n')
    file_open.close()

    df = pd.read_csv(file_name, sep="|", encoding='cp949')
    today1 = datetime.date.today()
    year = today1.year
    month = today1.month
    month_fix = today1.month - 1
    day = '00'
    if month == 1 : month_fix = 12
    stand_day = int(str(year)+str(month_fix)+day)
    print(stand_day)
    df_fix = df.loc[:,['대지_위치','건물_명','연면적','실제_착공_일','건축_허가_일','사용승인_일']]
    df_fix['실제_착공_일'] = pd.to_numeric(df_fix['실제_착공_일'], downcast='integer',errors='coerce')
    df_fix['연면적'] = pd.to_numeric(df_fix['연면적'], downcast='integer')
    df_fix1 = df_fix[(df_fix['건물_명'].notnull()) & (df_fix['실제_착공_일'] > stand_day) & (df_fix['연면적'] > 1000)]

    result_name = '수집결과\\17_1_건축인허가\\건축인허가_'+today+'.csv'
    df_fix1.to_csv(result_name, encoding='cp949', sep=',')

    os.remove(zip_fullpath)
    os.remove('mart_kcy_01.txt')
    os.remove(file_name)

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()