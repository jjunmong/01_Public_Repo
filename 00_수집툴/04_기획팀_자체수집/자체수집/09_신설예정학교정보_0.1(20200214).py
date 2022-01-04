import time
import codecs
import requests
import random
import json
#
# def main():
#
#     outfile = codecs.open('신설예정학교정보.txt', 'w', 'utf-8')
#     outfile.write("SD_EDU_OFFC_NM|SGG_NM|EDU_OFFC_NM|SCHL_NM|SCHL_GRAD_NM|OPEN_SCHD_YM|ADDRESS|CLASS_CNT|GNRL_CLASS_CNT|"
#                   "SPCL_CLASS_CNT|KNDR_CLASS_CNT|WISEOPEN_CNT\n")
#     page = 1
#     while True :
#         store_list = getinfo(page)
#         if store_list == []: break;
#         for store in store_list:
#             outfile.write(u'%s|' % store['SD_EDU_OFFC_NM'])
#             outfile.write(u'%s|' % store['SGG_NM'])
#             outfile.write(u'%s|' % store['EDU_OFFC_NM'])
#             outfile.write(u'%s|' % store['SCHL_NM'])
#             outfile.write(u'%s|' % store['SCHL_GRAD_NM'])
#             outfile.write(u'%s|' % store['OPEN_SCHD_YM'])
#             outfile.write(u'%s|' % store['ADDRESS'])
#             outfile.write(u'%s|' % store['CLASS_CNT'])
#             outfile.write(u'%s|' % store['GNRL_CLASS_CNT'])
#             outfile.write(u'%s|' % store['SPCL_CLASS_CNT'])
#             outfile.write(u'%s|' % store['KNDR_CLASS_CNT'])
#             outfile.write(u'%s\n' % store['WISEOPEN_CNT'])
#         page += 1
#         if page == 10: break
#         time.sleep(random.uniform(0.3,0.6))
#
#     outfile.close()
#
#
# def getinfo(intPageNo):
#     url = 'http://www.eduinfo.go.kr/portal/service/openInfSColViewListAll.do?ibpage={}&onepagerow=100&colWidth=&infId=6XL' \
#           '5JLKXZUNHK4GWJ87X7758606&infSeq=1&srvCd=S&SSheetNm=Scol2&fileDownType=&applyYn=N&gridItem=&tblId=&popColId=&' \
#           'fsYn=N&gofDivCd=&myDataCd=2&SD_EDU_OFFC_DIV=&comboFiltNeed=N&SGG_NM=&wordsFiltNeed=N&SCHL_GRAD_CD=&comboFilt' \
#           'Need=N&queryString=colWidth@!~~!@infId@!~6XL5JLKXZUNHK4GWJ87X7758606~!@infSeq@!~1~!@srvCd@!~S~!@SSheetNm@!~Sc' \
#           'ol2~!@fileDownType@!~~!@applyYn@!~N~!@gridItem@!~~!@tblId@!~~!@popColId@!~~!@fsYn@!~N~!@gofDivCd@!~~!@myDataCd' \
#           '@!~2~!@SD_EDU_OFFC_DIV@!~~!@comboFiltNeed@!~N~!@SGG_NM@!~~!@wordsFiltNeed@!~N~!@SCHL_GRAD_CD@!~~!@comboFiltNeed@!~N&iborderby='.format(intPageNo)
#     jsonData = requests.get(url)
#     print(url)
#     josonData = jsonData.text
#     josonString = json.loads(josonData)
#     entityList = josonString['DATA']
#     data = []
#     for info in entityList:
#         SD_EDU_OFFC_NM = info['SD_EDU_OFFC_NM']
#         SGG_NM = info['SGG_NM']
#         EDU_OFFC_NM = info['EDU_OFFC_NM']
#         SCHL_NM = info['SCHL_NM']
#         SCHL_GRAD_NM = info['SCHL_GRAD_NM']
#         OPEN_SCHD_YM = info['OPEN_SCHD_YM']
#         ADDRESS = info['ADDRESS']
#         CLASS_CNT = info['CLASS_CNT']
#         GNRL_CLASS_CNT = info['GNRL_CLASS_CNT']
#         SPCL_CLASS_CNT = info['SPCL_CLASS_CNT']
#         KNDR_CLASS_CNT = info['KNDR_CLASS_CNT']
#         WISEOPEN_CNT = info['WISEOPEN_CNT']
#         data.append(
#             {"SD_EDU_OFFC_NM": SD_EDU_OFFC_NM, "SGG_NM": SGG_NM, "EDU_OFFC_NM": EDU_OFFC_NM, "SCHL_NM": SCHL_NM
#                 , "SCHL_GRAD_NM": SCHL_GRAD_NM, "SCHL_GRAD_NM": SCHL_GRAD_NM, "OPEN_SCHD_YM": OPEN_SCHD_YM,
#              "ADDRESS": ADDRESS, "CLASS_CNT": CLASS_CNT, "GNRL_CLASS_CNT": GNRL_CLASS_CNT, "SPCL_CLASS_CNT": SPCL_CLASS_CNT,
#              "KNDR_CLASS_CNT": KNDR_CLASS_CNT, "WISEOPEN_CNT": WISEOPEN_CNT})
#     return data
#
# def errExit(msg):
#     sys.stderr.write(msg + '\n')
#     sys.exit(0)
#
# if __name__ == '__main__':
#     main()


def main():

    outfile = codecs.open('09_신설예정학교정보.txt', 'w', 'utf-8')
    outfile.write("schlNm|classCnt|ditcNm|eduOffcNm|openSchdYm|pointX|pointY|realAddr|remk\n")

    Code_list = ['B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'I10', 'J10', 'K10', 'L10', 'M10', 'N10', 'O10',
                 'P10', 'Q10', 'R10', 'S10', 'T10', ]

    for code in Code_list:
        store_list = getinfo(code)
        print(code)
        for store in store_list:
            outfile.write(u'%s|' % store['schlNm'])
            outfile.write(u'%s|' % store['classCnt'])
            outfile.write(u'%s|' % store['ditcNm'])
            outfile.write(u'%s|' % store['eduOffcNm'])
            outfile.write(u'%s|' % store['openSchdYm'])
            outfile.write(u'%s|' % store['pointX'])
            outfile.write(u'%s|' % store['pointY'])
            outfile.write(u'%s|' % store['realAddr'])
            outfile.write(u'%s\n' % store['remk'])
        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getinfo(regionCode):
    url = 'http://eduinfo.go.kr/portal/theme/newSchInfoDetail.do'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'AJAX': 'true',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '51',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=F6FA417B90A6764235BF19DA6C5F546A',
        'Host': 'eduinfo.go.kr',
        'Origin': 'http://eduinfo.go.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://eduinfo.go.kr/portal/theme/newSchMapPage.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'schlSeq': '',
        'yymmdd': '',
        'searchRg': 'J10',
        'searchOffc': '',
        'searchWd': '',
    }
    data['searchRg'] = regionCode
    jsonData = requests.post(url,headers = headers, data = data)
    josonData = jsonData.text
    josonString = json.loads(josonData)
    entityList = josonString['result']
    print(entityList)
    data = []
    for info in entityList:
        schlNm = info['schlNm']
        classCnt = info['classCnt']
        ditcNm = info['ditcNm']
        eduOffcNm = info['eduOffcNm']
        openSchdYm = info['openSchdYm']
        pointX = info['pointX']
        pointY = info['pointY']
        realAddr = info['realAddr']
        remk = info['remk']
        data.append({'schlNm':schlNm,'classCnt':classCnt,'ditcNm':ditcNm,'eduOffcNm':eduOffcNm,'openSchdYm':openSchdYm,'pointX':pointX,'pointY':pointY,'realAddr':realAddr,'remk':remk})

    return data

main()