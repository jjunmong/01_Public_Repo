import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import os, sys
import getpass
import shutil
from datetime import datetime
import codecs
import traceback

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\01_2_주유소판매가격\\') == False : os.makedirs('수집결과\\01_2_주유소판매가격\\')
outfilename = '수집결과\\01_2_주유소판매가격\\주유소판매가격_{}.csv'.format(today)
outfilename_true = '수집결과\\01_2_주유소판매가격\\주유소판매가격_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\01_2_주유소판매가격\\주유소판매가격_{}.log_실패.txt'.format(today)
def main():
    try:
        csv_down()
        file_move()
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

def csv_down():
    chromedriver_dir = r'C:\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)
    driver.get('https://www.opinet.co.kr/user/opdown/opDownload.do')
    time.sleep(2)
    click_list = driver.find_element(By.XPATH,'//*[@id="rdo4_2"]')
    driver.execute_script("arguments[0].click();", click_list)
    time.sleep(2)
    click_list2 = driver.find_element(By.XPATH,'//*[@id="priceInfoVO"]/div/div[3]/table/tbody/tr[4]/td[2]/a[2]')
    driver.execute_script("arguments[0].click();", click_list2)
    time.sleep(2)
    Alert(driver).accept()
    time.sleep(20)
    print('수집완료')
    driver.close()

def file_move():
    getuser = getpass.getuser()
    origin_dir = r'C:\Users\{}\Downloads'.format(getuser)
    current_dir = os.getcwd()
    file_list = os.listdir(origin_dir)
    file_name = ''
    for s in file_list:
        if s.startswith('과거_판매가격') == True :
            file_name = s

    origin_file = origin_dir+'\\'+file_name
    copy_file = current_dir+'\\'+file_name
    shutil.copy(origin_file,copy_file)
    os.remove(origin_file)
    os.rename(copy_file, outfilename)

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()