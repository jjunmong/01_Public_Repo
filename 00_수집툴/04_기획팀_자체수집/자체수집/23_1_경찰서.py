import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import getpass
import shutil
from datetime import datetime

def csv_down():
    chromedriver_dir = r'C:\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)
    driver.get('https://www.data.go.kr/data/15054711/fileData.do#/tab-layer-file')
    time.sleep(3)

    login_button = driver.find_element(By.XPATH,'//*[@id="tab-layer-file"]/div[2]/div[2]/a[1]')
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(10)
    driver.close()

def file_move():
    getuser = getpass.getuser()
    origin_dir = r'C:\Users\{}\Downloads'.format(getuser)
    current_dir = os.getcwd()
    file_list = os.listdir(origin_dir)
    file_name = ''
    for s in file_list:
        if s.startswith('경찰청_경찰관서') == True :
            file_name = s

    origin_file = origin_dir+'\\'+file_name
    copy_file = current_dir+'\\'+file_name
    shutil.copy(origin_file,copy_file)
    os.remove(origin_file)

    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\경찰서_{}.csv'.format(today)
    os.rename(copy_file,outfilename)

csv_down()
file_move()