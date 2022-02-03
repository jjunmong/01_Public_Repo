import codecs
import requests
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\10_1_알리오플러스\\') == False : os.makedirs('수집결과\\10_1_알리오플러스\\')
outfilename = '수집결과\\10_1_알리오플러스\\알리오플러스_{}.xlsx'.format(today)
outfilename_true = '수집결과\\10_1_알리오플러스\\알리오플러스_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\10_1_알리오플러스\\알리오플러스_{}.log_실패.txt'.format(today)

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
    url = "http://www.alioplus.go.kr/organization/orgExcelDown.do?pageNo=1&excelTitle=%EA%B8%B0%EA%B4%80%EB%A6%AC%EC%8A%A4%ED%8A%B8(%EC%A0%84%EC%B2%B4_+)&schApbaGb=APBA_ALL&schForeignYn=&schApbaCate=&schApbaId=&schSiNa=&schSggNa=&schCont=+"
    filename = '수집결과\\기관리스트(전체_ ).xlsx'
    with open(filename, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    print('기관 리스트 다운로드 완료')
    os.rename(filename, outfilename)

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

