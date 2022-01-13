import requests
import bs4
import codecs
from datetime import datetime
import traceback
import os, sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\16_1_신설법인\\') == False : os.makedirs('수집결과\\16_1_신설법인\\')
outfilename_true = '수집결과\\16_1_신설법인\\신설법인_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\16_1_신설법인\\신설법인_{}.log_실패.txt'.format(today)

def main():
    try:
        Crawl_run()
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
    url = 'https://www.mk.co.kr/news/business/new-corporation/'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    dl = bsObj.find('dl',{"class":"article_list pt0"})
    source_url = dl.find('a')['href']

    url = source_url
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    div = bsObj.find('div',{"id":"article_body"})
    down_url = div.find('a')['href']
    file_name = div.find('b').text.replace(' ','')+'_'+today+'.xls'
    url = down_url
    with open('수집결과\\16_1_신설법인\\'+file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    print('신설법인 다운로드 완료')

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()







