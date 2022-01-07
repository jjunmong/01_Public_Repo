import os
import requests
import zipfile
from datetime import datetime

def download():
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
    outfilename = '수집결과\\행정표준기관코드_{}.txt'.format(today)
    os.rename('기관코드 전체자료.txt',outfilename)
    print('압축 해제 완료')

download()