import codecs
import requests
import json
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\21_2_창고114\\') == False : os.makedirs('수집결과\\21_2_창고114\\')
outfilename = '수집결과\\21_2_창고114\\창고114_{}.txt'.format(today)
outfilename_true = '수집결과\\21_2_창고114\\창고114_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\21_2_창고114\\창고114_{}.log_실패.txt'.format(today)

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
    dict_keys1 = getStoreInfo(1)[1]
    dict_keys2 = str(dict_keys1).replace('dict_keys','').replace('[','').replace(']','').replace('(','').replace(')','').replace(',','}').replace("'","").replace(' ','')
    outfile.write("%s\n" % dict_keys2)

    key_list = []
    for key in dict_keys1:
        key_list.append(key)

    page = 1
    while True:
        store_list = getStoreInfo(page)[0]
        if store_list == [] : break
        print(page, store_list)
        for store in store_list:
            column_num = 0
            while True:
                if column_num == len(key_list) : break
                elif column_num == len(key_list)-1 :
                    outfile.write(u'%s\n' % store[u'%s' % key_list[column_num]])
                else:
                    outfile.write(u'%s}' % store[u'%s' % key_list[column_num]])
                column_num +=1
        page+=1
    outfile.close()

def getStoreInfo(intPageNo):
    url = 'http://nlic.go.kr/nlic/searchWare.action?bas_ware_nm=&ser_ware_type=&gis_sido=&gis_sido_nm=%EC%8B%9C%EB%8F%84%EC%84%A0%ED%83%9D&gis_sigu=&gis_sigu_nm=%EC%8B%9C%EA%B5%B0%EA%B5%AC%EC%84%A0%ED%83%9D&ware_use=1&chk_lofa1=T&chk_lofa2=T&chk_lofa3=T&chk_port=T&chk_cust=T&chk_chem=T&chk_food=T&chk_anim=T&chk_mari=T&chk_info=T&chk_all=T&orderType=&pageNum={}&is_ajax=1'.format(intPageNo)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    pageString = requests.get(url , headers = headers).text
    jsonString = json.loads(pageString)
    entityList =jsonString['list']
    result = []
    dict_key = ''
    for info in entityList:
        BAS_ADMIN_MOBILE = str(info["BAS_ADMIN_MOBILE"]).replace('\n','').strip()
        BAS_GROSS_AREA = str(info["BAS_GROSS_AREA"]).replace('\n','').strip()
        BAS_ITEM = str(info["BAS_ITEM"]).replace('\n','').strip()
        BAS_WARE_NM = str(info["BAS_WARE_NM"]).replace('\n','').strip().replace('	','')
        CORP_FILE = str(info["CORP_FILE"]).replace('\n','').strip().replace('\\','\\\\')
        CORP_ID = str(info["CORP_ID"]).replace('\n','').strip()
        CORP_NM = str(info["CORP_NM"]).replace('\n','').strip()
        CORP_TEL = str(info["CORP_TEL"]).replace('\n','').strip()
        GIS_JIBUN_ADDR = str(info["GIS_JIBUN_ADDR"]).replace('\n','').strip()
        GIS_JIBUN_ADDR_DO_SI = str(info["GIS_JIBUN_ADDR_DO_SI"]).replace('\n','').strip()
        GIS_NEW_ADDR = str(info["GIS_NEW_ADDR"]).replace('\n','').strip()
        LAW_TYPE = str(info["LAW_TYPE"]).replace('\n','').strip()
        PICT_YN = str(info["PICT_YN"]).replace('\n','').strip()
        RNUM = str(info["RNUM"]).replace('\n','').strip()
        SER_CERT = str(info["SER_CERT"]).replace('\n','').strip()
        SER_DIST = str(info["SER_DIST"]).replace('\n','').strip()
        SER_ETC = str(info["SER_ETC"]).replace('\n','').strip()
        SER_FACI = str(info["SER_FACI"]).replace('\n','').strip()
        SER_INSU = str(info["SER_INSU"]).replace('\n','').strip()
        SER_WARE_TYPE = str(info["SER_WARE_TYPE"]).replace('\n','').strip()
        UPD_DATE = str(info["UPD_DATE"]).replace('\n','').strip()
        VAC_AREA = str(info["VAC_AREA"]).replace('\n','').strip()
        VAC_AREA_GUBUN = str(info["VAC_AREA_GUBUN"]).replace('\n','').strip()
        VAC_RATE = str(info["VAC_RATE"]).replace('\n','').strip()
        WARE_ID = str(info["WARE_ID"]).replace('\n','').strip()
        WARE_ID_SEQ = str(info["WARE_ID_SEQ"]).replace('\n','').strip()
        WARE_INTRO = str(info["WARE_INTRO"]).replace('\n','').strip()
        WARE_NO = str(info["WARE_NO"]).replace('\n','').strip()
        WARE_USE = str(info["WARE_USE"]).replace('\n','').strip()
        result_dict = {"BAS_ADMIN_MOBILE" :BAS_ADMIN_MOBILE,"BAS_GROSS_AREA" :BAS_GROSS_AREA,"BAS_ITEM" :BAS_ITEM,"BAS_WARE_NM" :BAS_WARE_NM,
                       "CORP_FILE" :CORP_FILE,"CORP_ID" :CORP_ID,"CORP_NM" :CORP_NM,"CORP_TEL" :CORP_TEL,"GIS_JIBUN_ADDR" :GIS_JIBUN_ADDR,
                       "GIS_JIBUN_ADDR_DO_SI" :GIS_JIBUN_ADDR_DO_SI,"GIS_NEW_ADDR" :GIS_NEW_ADDR,"LAW_TYPE" :LAW_TYPE,"PICT_YN" :PICT_YN,
                       "RNUM" :RNUM,"SER_CERT" :SER_CERT,"SER_DIST" :SER_DIST,"SER_ETC" :SER_ETC,"SER_FACI" :SER_FACI,"SER_INSU" :SER_INSU,
                       "SER_WARE_TYPE" :SER_WARE_TYPE,"UPD_DATE" :UPD_DATE,"VAC_AREA" :VAC_AREA,"VAC_AREA_GUBUN" :VAC_AREA_GUBUN,"VAC_RATE" :VAC_RATE,
                       "WARE_ID" :WARE_ID,"WARE_ID_SEQ" :WARE_ID_SEQ,"WARE_INTRO" :WARE_INTRO,"WARE_NO" :WARE_NO,"WARE_USE" :WARE_USE,}
        dict_key = result_dict.keys()
        result.append(result_dict)
    return result, dict_key

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()