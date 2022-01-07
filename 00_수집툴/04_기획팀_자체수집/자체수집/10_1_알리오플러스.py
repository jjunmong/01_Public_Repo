import requests
import os
from datetime import datetime

def download_ALIO():
    url = "http://www.alioplus.go.kr/organization/orgExcelDown.do?pageNo=1&excelTitle=%EA%B8%B0%EA%B4%80%EB%A6%AC%EC%8A%A4%ED%8A%B8(%EC%A0%84%EC%B2%B4_+)&schApbaGb=APBA_ALL&schForeignYn=&schApbaCate=&schApbaId=&schSiNa=&schSggNa=&schCont=+"
    filename = '수집결과\\기관리스트(전체_ ).xlsx'
    with open(filename, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    print('기관 리스트 다운로드 완료')

    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\알리오플러스_{}.xlsx'.format(today)

    os.rename(filename, outfilename)

download_ALIO()

