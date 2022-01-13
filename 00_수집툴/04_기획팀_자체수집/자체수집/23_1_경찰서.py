import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass
import shutil
import codecs
from datetime import datetime
import traceback
import os, sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\23_1_경찰서\\') == False : os.makedirs('수집결과\\23_1_경찰서\\')
outfilename_true = '수집결과\\23_1_경찰서\\경찰서_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\23_1_경찰서\\경찰서_{}.log_실패.txt'.format(today)

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
    outfilename = '수집결과\\23_1_경찰서\\경찰서_{}.csv'.format(today)
    os.rename(copy_file,outfilename)

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()