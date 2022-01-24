import codecs
import requests
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\21_3_국가물류통합정보센터\\') == False : os.makedirs('수집결과\\21_3_국가물류통합정보센터\\')
# outfilename = '수집결과\\21_3_국가물류통합정보센터\\알리오플러스_{}.xlsx'.format(today)
outfilename_true = '수집결과\\21_3_국가물류통합정보센터\\국가물류통합정보센터{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\21_3_국가물류통합정보센터\\국가물류통합정보센터{}.log_실패.txt'.format(today)

def main():
    try:
        Crawl_run1()#1.물류 창고 정보
        Crawl_run2()#2.물류 단지 정보
        Crawl_run3()#3.물류 터미널 정보
        Crawl_run4()#4.내륙물류기지 정보
        Crawl_run5()#5.공영차고지정보
        Crawl_run6()#6.화물차휴게소정보
        Crawl_run7()#7.우수녹색물류기업
        Crawl_run8()#8.물류기업정보
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

def Crawl_run1():#1.물류 창고 정보
    url = "https://www.nlic.go.kr/nlic/WhsInfoWarehouseSch.action"
    data= {
        'command': 'DWLOAD',
        'PAGE_CUR': '1',
        'S_CHK_FLAG': 'false',
        'S_CHK_VALUE_GEN': 'true',
        'S_CHK_VALUE_COL': 'true',
        'S_CHK_VALUE_STORE': 'true',
        'S_CHK_VALUE_PORT': 'true',
        'S_CHK_VALUE_CUST': 'true',
        'S_CHK_VALUE_CHEM': 'true',
        'S_CHK_VALUE_FOOD': 'true',
        'S_CHK_VALUE_ANIM': 'true',
        'S_CHK_VALUE_MARI': 'true',
        'S_CHK_VALUE_PRIME_YN': '',
        'S_PAGE_LEN': '4724',
        'S_D_FROM': '1970',
        'S_D_TO': '2022',
        'S_CORP_NM': '',
        'S_SIDO': '',
        'S_GUGUN': '',
        'S_ITEM_TEXT': '',
        'CHK_GEN': 'Y',
        'CHK_COL': 'Y',
        'CHK_STORE': 'Y',
        'CHK_PORT': 'Y',
        'CHK_CUST': 'Y',
        'CHK_CHEM': 'Y',
        'CHK_FOOD': 'Y',
        'CHK_ANIM': 'Y',
        'CHK_MARI': 'Y',
        'chk_all': 'on',
    }
    filename = '수집결과\\21_3_국가물류통합정보센터\\물류창고정보_{}.xls'.format(today)
    with open(filename, "wb") as file:
        response = requests.post(url,data = data)
        file.write(response.content)
    print('물류창고정보 다운로드 완료')
    file.close()

def Crawl_run2():#2.물류 단지 정보
    url = "https://www.nlic.go.kr/nlic/fmComplex0010.action"
    data= {
        'command': 'DWLOAD',
        'PAGE_CUR': '1',
        'S_GUBUN_NM': '',
        'S_GUBUN': '',
        'S_GUBUN_SIDO': ''
    }
    filename = '수집결과\\21_3_국가물류통합정보센터\\물류단지정보_{}.xls'.format(today)
    with open(filename, "wb") as file:
        response = requests.post(url,data = data)
        file.write(response.content)
    print('물류단지정보 다운로드 완료')
    file.close()

def Crawl_run3():#3.물류 터미널 정보
    url = "https://www.nlic.go.kr/nlic/fmTerminal0010.action"
    data= {
        'command': 'DWLOAD',
        'PAGE_CUR': '1',
        'S_GUBUN_NM': '',
        'S_GUBUN_SIDO': ''
    }
    filename = '수집결과\\21_3_국가물류통합정보센터\\물류터미널정보_{}.xls'.format(today)
    with open(filename, "wb") as file:
        response = requests.post(url,data = data)
        file.write(response.content)
    print('물류터미널정보 다운로드 완료')
    file.close()

def Crawl_run4():#4.내륙물류기지 정보
    url = "https://www.nlic.go.kr/nlic/ovseaLgistReportFileDown.action?A"
    data= {
        'ATCHMNFL_ID': 'five001',
        'ATCHMNFL_SN': '0',
    }
    filename = '수집결과\\21_3_국가물류통합정보센터\\내륙물류기지정보_{}.xls'.format(today)
    with open(filename, "wb") as file:
        response = requests.get(url,params = data)
        file.write(response.content)
    print('내륙물류기지정보 다운로드 완료')
    file.close()

def Crawl_run5():#5.공영차고지정보
    url = "https://www.nlic.go.kr/nlic/fmParking0010.action"
    data= {
        'command': 'DWLOAD',
        'PAGE_CUR': '1',
        'S_GUBUN_NM': '',
        'S_GUBUN_SIDO': ''
    }
    filename = '수집결과\\21_3_국가물류통합정보센터\\공영차고지정보_{}.xls'.format(today)
    with open(filename, "wb") as file:
        response = requests.post(url,data = data)
        file.write(response.content)
    print('공영차고지정보 다운로드 완료')
    file.close()

def Crawl_run6():#6.화물차휴게소정보
    url = "https://www.nlic.go.kr/nlic/fmResting0010.action"
    data= {
        'command': 'DWLOAD',
        'PAGE_CUR': '1',
        'S_GUBUN_NM': '',
        'S_GUBUN_SIDO': ''
    }
    filename = '수집결과\\21_3_국가물류통합정보센터\\화물차휴게소정보_{}.xls'.format(today)
    with open(filename, "wb") as file:
        response = requests.post(url, data = data)
        file.write(response.content)
    print('화물차휴게소정보 다운로드 완료')
    file.close()

def Crawl_run7():#7.우수녹색물류기업
    url = "https://www.nlic.go.kr/nlic/bestGreenBusiCertLi.action?command=DWLOAD&S_D_FROM=2000&S_D_TO=2022&S_COMP_NM=&cmbSrchCompGubun="
    filename = '수집결과\\21_3_국가물류통합정보센터\\우수녹색물류기업_{}.xls'.format(today)
    with open(filename, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    print('우수녹색물류기업 다운로드 완료')
    file.close()

def Crawl_run8():#8.물류기업정보
    url = "https://www.nlic.go.kr/nlic/excelLgistEntrInfoListDown.action"
    data = {
        'fldExcelSrchWord': '',
        'fldExcelSrchEntrCd': '',
    }
    filename = '수집결과\\21_3_국가물류통합정보센터\\물류기업정보_{}.xls'.format(today)
    with open(filename, "wb") as file:
        response = requests.post(url, data = data)
        file.write(response.content)
    print('물류기업정보 다운로드 완료')
    file.close()

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

