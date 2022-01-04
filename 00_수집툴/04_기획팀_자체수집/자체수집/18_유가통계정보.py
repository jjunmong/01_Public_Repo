import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import os
import getpass
import shutil

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
    time.sleep(60)
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

csv_down()
file_move()