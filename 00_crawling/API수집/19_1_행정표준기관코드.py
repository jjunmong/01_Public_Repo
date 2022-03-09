import requests
import zipfile
import codecs
from datetime import datetime
import traceback
import os, sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\19_1_행정표준기관코드\\') == False : os.makedirs('수집결과\\19_1_행정표준기관코드\\')
outfilename_true = '수집결과\\19_1_행정표준기관코드\\행정표준기관코드_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\19_1_행정표준기관코드\\행정표준기관코드_{}.log_실패.txt'.format(today)

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
    url = "https://www.code.go.kr/etc/codeFullDown.do"
    data = {
        'cPage': '1',
        'codeseId': '기관코드',
        'fullNm': '',
        'lowNm': '',
        'orgCd': '',
        'highCd': '0',
        'typebigCd': '',
        'typemidCd': '',
        'typesmlCd': '',
        'sidoCd': '',
        'sggCd': '',
        'stopSelt': '0',
        'CkStopSelt': '1',
        'stdate': '',
        'enddate': '',
    }
    filename = '기관코드_전체자료.zip'
    with open(filename, "wb") as file:
        response = requests.post(url, data = data)
        file.write(response.content)
    print('기관 리스트 다운로드 완료')
    file.close()

    zf = zipfile.ZipFile(filename)
    zipinfo = zf.infolist()
    for ss in zipinfo:
        ss.filename = ss.filename.encode('cp437').decode('euc-kr', 'ignore')
        zf.extract(ss)
    zf.close()
    os.remove(filename)
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\19_1_행정표준기관코드\\행정표준기관코드_{}.txt'.format(today)
    os.rename('기관코드 전체자료.txt',outfilename)
    print('압축 해제 완료')

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()