import time
import codecs
import requests
import random
import json
from datetime import datetime

def main():
    today = str(datetime.today()).split(' ')[0].replace('-','')
    outfilename = '수집결과\\전국학교_{}.txt'.format(today)

    outfile = codecs.open(outfilename, 'w', 'utf-8')
    outfile.write("SD_EDU_OFFC_NM|SCHL_NM|SCHL_GRAD_NM|ADDRESS|RG_EDU_OFFC_NM|OPEN_DATE|SCHL_URL|SCHL_TEL|TOT_CLASS_CNT|TOT_STDT_CNT|TOT_TCHR_CNT|TOT_OFWR_CNT|WISEOPEN_CNT\n")

    sidoCode = ['B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'I10', 'J10', 'K10', 'M10', 'N10', 'P10', 'Q10', 'R10',
                'S10', 'T10']
    for code in sidoCode:
        page = 1
        while True :
            store_list = getinfo(page,code)
            if store_list == [] : break;

            for store in store_list:
                outfile.write(u'%s|' % store['SD_EDU_OFFC_NM'])
                outfile.write(u'%s|' % store['SCHL_NM'])
                outfile.write(u'%s|' % store['SCHL_GRAD_NM'])
                outfile.write(u'%s|' % store['ADDRESS'])
                outfile.write(u'%s|' % store['ESTB_DIV_NM'])
                outfile.write(u'%s|' % store['RG_EDU_OFFC_NM'])
                outfile.write(u'%s|' % store['OPEN_DATE'])
                outfile.write(u'%s|' % store['SCHL_URL'])
                outfile.write(u'%s|' % store['SCHL_TEL'])
                outfile.write(u'%s|' % store['TOT_CLASS_CNT'])
                outfile.write(u'%s|' % store['TOT_STDT_CNT'])
                outfile.write(u'%s|' % store['TOT_TCHR_CNT'])
                outfile.write(u'%s|' % store['TOT_OFWR_CNT'])
                outfile.write(u'%s\n' % store['WISEOPEN_CNT'])

            page += 1

            if page == 99 : break

            time.sleep(random.uniform(0.3,0.6))

    outfile.close()


def getinfo(intPageNo, sidoCode):
    url = 'http://www.eduinfo.go.kr/portal/service/openInfSColViewListAll.do?ibpage={}&onepagerow=100&colWidth=&infId=RY4AY792FINLCGGD1DW37745620&infSeq=1&srvCd=S&SSheetNm=Scol0&fileDownType=&applyYn=N&gridItem=&tblId=&popColId=&fsYn=N&gofDivCd=&myDataCd=2&SD_EDU_OFFC_DIV={}&comboFiltNeed=Y&SGG_NM=&wordsFiltNeed=N&SCHL_GRAD_CD=&comboFiltNeed=N&queryString=colWidth@!~~!@infId@!~RY4AY792FINLCGGD1DW37745620~!@infSeq@!~1~!@srvCd@!~S~!@SSheetNm@!~Scol0~!@fileDownType@!~~!@applyYn@!~N~!@gridItem@!~~!@tblId@!~~!@popColId@!~~!@fsYn@!~N~!@gofDivCd@!~~!@myDataCd@!~2~!@SD_EDU_OFFC_DIV@!~{}~!@comboFiltNeed@!~Y~!@SGG_NM@!~~!@wordsFiltNeed@!~N~!@SCHL_GRAD_CD@!~~!@comboFiltNeed@!~N&iborderby='.format(
        intPageNo, sidoCode, sidoCode)
    # url = 'http://www.eduinfo.go.kr/portal/service/openInfSColViewListAll.do'
    data = {
        # 'ibpage':'1',
        # 'onepagerow':'50',
        # 'colWidth':'',
        # 'infId':'RY4AY792FINLCGGD1DW37745620',
        # 'infSeq':'1',
        # 'srvCd':'S',
        # 'SSheetNm':'Scol0',
        # 'fileDownType':'',
        # 'applyYn':'N',
        # 'gridItem':'',
        # 'tblId':'',
        # 'popColId':'',
        # 'fsYn':'N',
        # 'gofDivCd':'',
        # 'myDataCd':'2',
        # 'SD_EDU_OFFC_DIV':'C10',
        # 'comboFiltNeed':'Y',
        # 'SGG_NM':'',
        # 'wordsFiltNeed':'N',
        # 'SCHL_GRAD_CD':'',
        # 'comboFiltNeed':'N',
        # 'queryString': 'colWidth@!~~!@infId@!~RY4AY792FINLCGGD1DW37745620~!@infSeq@!~1~!@srvCd@!~S~!@SSheetNm@!~Scol0~!@fileDownType@!~~!@applyYn@!~N~!@gridItem@!~~!@tblId@!~~!@popColId@!~~!@fsYn@!~N~!@gofDivCd@!~~!@myDataCd@!~2~!@SD_EDU_OFFC_DIV@!~{}~!@comboFiltNeed@!~Y~!@SGG_NM@!~~!@wordsFiltNeed@!~N~!@SCHL_GRAD_CD@!~~!@comboFiltNeed@!~N'.format(sidoCode)
        # 'iborderby':'',
    }
    # data['ibpage'] = intPageNo
    jsonData = requests.get(url)
    print(url)
    josonData = jsonData.text
    josonString = json.loads(josonData)
    entityList = josonString['DATA']
    data = []
    for info in entityList:
        SD_EDU_OFFC_NM = info['SD_EDU_OFFC_NM']
        SCHL_NM = info['SCHL_NM']
        SCHL_GRAD_NM = info['SCHL_GRAD_NM']
        ADDRESS = info['ADDRESS']
        ESTB_DIV_NM = info['ESTB_DIV_NM']
        RG_EDU_OFFC_NM = info['RG_EDU_OFFC_NM']
        OPEN_DATE = info['OPEN_DATE']
        SCHL_URL = info['SCHL_URL']
        SCHL_TEL = info['SCHL_TEL']
        TOT_CLASS_CNT = info['TOT_CLASS_CNT']
        TOT_STDT_CNT = info['TOT_STDT_CNT']
        TOT_TCHR_CNT = info['TOT_TCHR_CNT']
        TOT_OFWR_CNT = info['TOT_OFWR_CNT']
        WISEOPEN_CNT = info['WISEOPEN_CNT']
        data.append(
            {"SD_EDU_OFFC_NM": SD_EDU_OFFC_NM, "SCHL_NM": SCHL_NM, "SCHL_GRAD_NM": SCHL_GRAD_NM, "ADDRESS": ADDRESS
                , "ESTB_DIV_NM": ESTB_DIV_NM, "RG_EDU_OFFC_NM": RG_EDU_OFFC_NM, "OPEN_DATE": OPEN_DATE,
             "SCHL_URL": SCHL_URL
                , "SCHL_TEL": SCHL_TEL, "TOT_CLASS_CNT": TOT_CLASS_CNT, "TOT_STDT_CNT": TOT_STDT_CNT,
             "TOT_TCHR_CNT": TOT_TCHR_CNT
                , "TOT_OFWR_CNT": TOT_OFWR_CNT, "WISEOPEN_CNT": WISEOPEN_CNT})
    return data

main()