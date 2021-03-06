import json
import time
import codecs
import requests
import random
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\06_3_폐교학교\\') == False : os.makedirs('수집결과\\06_3_폐교학교\\')
outfilename = '수집결과\\06_3_폐교학교\\폐교학교_{}.txt'.format(today)
outfilename_true = '수집결과\\06_3_폐교학교\\폐교학교_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\06_3_폐교학교\\폐교학교_{}.log_실패.txt'.format(today)
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
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("MTRP_PRVC_NM|EDU_OFFC|ABOL_SCH_NM|GRADE|ADDRESS|DEPT_NM|CHRGR_TEL|ABOL_SCH_YY|USE_STATE|"
                  "BUDG_AREA|GRD_AREA|SUM_PRIC|LOAN_CD|LOAN_DESC|LOAN_COST|LOAN_COMP_DAY|WISEOPEN_CNT\n")
    page = 1
    while True :
        store_list = getinfo(page)
        if store_list == []: break;
        for store in store_list:
            outfile.write(u'%s|' % store['MTRP_PRVC_NM'])
            outfile.write(u'%s|' % store['EDU_OFFC'])
            outfile.write(u'%s|' % store['ABOL_SCH_NM'])
            outfile.write(u'%s|' % store['GRADE'])
            outfile.write(u'%s|' % store['ADDRESS'])
            outfile.write(u'%s|' % store['DEPT_NM'])
            outfile.write(u'%s|' % store['CHRGR_TEL'])
            outfile.write(u'%s|' % store['ABOL_SCH_YY'])
            outfile.write(u'%s|' % store['USE_STATE'])
            outfile.write(u'%s|' % store['BUDG_AREA'])
            outfile.write(u'%s|' % store['GRD_AREA'])
            outfile.write(u'%s|' % store['SUM_PRIC'])
            outfile.write(u'%s|' % store['LOAN_CD'])
            outfile.write(u'%s|' % store['LOAN_DESC'])
            outfile.write(u'%s|' % store['LOAN_COST'])
            outfile.write(u'%s|' % store['LOAN_COMP_DAY'])
            outfile.write(u'%s\n' % store['WISEOPEN_CNT'])
        page += 1
        if page == 100: break
        time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getinfo(intPageNo):
    url = 'http://www.eduinfo.go.kr/portal/service/openInfSColViewListAll.do?ibpage={}&onepagerow=100&colWidth=&infId=ZX' \
          '5EM8TMQIKPJE0AWBW67766468&infSeq=1&srvCd=S&SSheetNm=Scol3&fileDownType=&applyYn=N&gridItem=&tblId=&popColId=' \
          'fsYn=N&gofDivCd=&myDataCd=2&MTRP_PRVC_CD=&comboFiltNeed=N&ADDRESS=&wordsFiltNeed=N&queryString=colWidth@!~~!' \
          '@infId@!~ZX5EM8TMQIKPJE0AWBW67766468~!@infSeq@!~1~!@srvCd@!~S~!@SSheetNm@!~Scol3~!@fileDownType@!~~!@applyYn' \
          '@!~N~!@gridItem@!~~!@tblId@!~~!@popColId@!~~!@fsYn@!~N~!@gofDivCd@!~~!@myDataCd@!~2~!@MTRP_PRVC_CD@!~~!@comb' \
          'oFiltNeed@!~N~!@ADDRESS@!~~!@wordsFiltNeed@!~N&iborderby='.format(intPageNo)
    jsonData = requests.get(url)
    print(url)
    josonData = jsonData.text
    josonString = json.loads(josonData)
    entityList = josonString['DATA']
    data = []
    for info in entityList:
        MTRP_PRVC_NM = info['MTRP_PRVC_NM']
        EDU_OFFC = info['EDU_OFFC']
        ABOL_SCH_NM = info['ABOL_SCH_NM']
        GRADE = info['GRADE']
        ADDRESS = info['ADDRESS']
        DEPT_NM = info['DEPT_NM']
        CHRGR_TEL = info['CHRGR_TEL']
        ABOL_SCH_YY = info['ABOL_SCH_YY']
        USE_STATE = info['USE_STATE']
        BUDG_AREA = info['BUDG_AREA']
        GRD_AREA = info['GRD_AREA']
        SUM_PRIC = info['SUM_PRIC']
        try:
            LOAN_CD = info['LOAN_CD'].replace('\n','')
        except :
            LOAN_CD = ''
        try:
            LOAN_DESC = info['LOAN_DESC'].replace('\n','')
        except :
            LOAN_DESC = ''
        LOAN_COST = info['LOAN_COST']
        LOAN_COMP_DAY = info['LOAN_COMP_DAY']
        WISEOPEN_CNT = info['WISEOPEN_CNT']
        data.append(
            {"MTRP_PRVC_NM": MTRP_PRVC_NM, "EDU_OFFC": EDU_OFFC, "ABOL_SCH_NM": ABOL_SCH_NM, "GRADE": GRADE
                , "ADDRESS": ADDRESS, "DEPT_NM": DEPT_NM,"CHRGR_TEL": CHRGR_TEL, "ABOL_SCH_YY": ABOL_SCH_YY, "USE_STATE": USE_STATE, "BUDG_AREA": BUDG_AREA,
             "GRD_AREA": GRD_AREA, "SUM_PRIC": SUM_PRIC,"LOAN_CD":LOAN_CD,"LOAN_DESC":LOAN_DESC,"LOAN_COST":LOAN_COST,"LOAN_COMP_DAY":LOAN_COMP_DAY,"WISEOPEN_CNT":WISEOPEN_CNT})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()