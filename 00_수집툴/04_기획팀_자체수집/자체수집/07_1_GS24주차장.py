import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import codecs
import requests
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\07_1_GS24주차장\\') == False : os.makedirs('수집결과\\07_1_GS24주차장\\')
outfilename = '수집결과\\07_1_GS24주차장\\GS24주차장_{}.txt'.format(today)
outfilename_true = '수집결과\\07_1_GS24주차장\\GS24주차장_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\07_1_GS24주차장\\GS24주차장_{}.log_실패.txt'.format(today)

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
    outfile.write("IDX|PARK_AREA_NAME|E_PARK_AREA_NAME|CAR_PARK_NUM|PERIOD_PARK_NUM|PARK_KIND|PARK_NUM|PARK_P_NUM|ZIP"
                  "|ADDRESS1|ADDRESS2|E_ADDRESS|WORK_TIME1|WORK_TIME2|WORK_TIME3|WORK_TIME4|WORK_TIME5|WORK_TIME6"
                  "|WORK_TIME7|WORK_TIME8|WORK_TIME9|WORK_TIME10|TEL|E_TEL|HP|PERIOD_TICKET1|PERIOD_TICKET2|PERIOD_TICKET3"
                  "|PERIOD_TICKET4|PERIOD_TICKET5|DC_TICKET1|DC_TICKET2|DC_TICKET3|DC_TICKET4|DC_TICKET5|COMPANY_NO"
                  "|BANK_NO|PIC1|PIC2|PIC3|PIC4|PIC5|PLACE_INFO|AREA_INFO|DEPT|DEPT_WOKER|DEPT_CONT_WORKER|CONT_STR_DATE"
                  "|CONT_END_DATE|OPEN_DATE|CREDIT_COST|RENTAL_COST|REGDT|ETC|SITE_REMOVE|BASIC_TICKET|STATUS|BANK_USER"
                  "|CARD_SITECODE|CARD_SITEKEY|CARD_SITENAME|CARD_COMPANY|TICKET_END_DATE|PERIOD_ETC|DC_ETC|PERIOD_TICKET6"
                  "|PERIOD_TICKET7|PERIOD_TICKET8|PERIOD_TICKET9|PERIOD_TICKET10|DC_TICKET6|DC_TICKET7|DC_TICKET8|DC_TICKET9"
                  "|DC_TICKET10|x|y|\n")
    store_list = getinfo()
    for ss in store_list:
        print(ss)
    for store in store_list:
        outfile.write(u'%s|' % store['IDX'])
        outfile.write(u'%s|' % store['PARK_AREA_NAME'])
        outfile.write(u'%s|' % store['E_PARK_AREA_NAME'])
        outfile.write(u'%s|' % store['CAR_PARK_NUM'])
        outfile.write(u'%s|' % store['PERIOD_PARK_NUM'])
        outfile.write(u'%s|' % store['PARK_KIND'])
        outfile.write(u'%s|' % store['PARK_NUM'])
        outfile.write(u'%s|' % store['PARK_P_NUM'])
        outfile.write(u'%s|' % store['ZIP'])
        outfile.write(u'%s|' % store['ADDRESS1'])
        outfile.write(u'%s|' % store['ADDRESS2'])
        outfile.write(u'%s|' % store['E_ADDRESS'])
        outfile.write(u'%s|' % store['WORK_TIME1'])
        outfile.write(u'%s|' % store['WORK_TIME2'])
        outfile.write(u'%s|' % store['WORK_TIME3'])
        outfile.write(u'%s|' % store['WORK_TIME4'])
        outfile.write(u'%s|' % store['WORK_TIME5'])
        outfile.write(u'%s|' % store['WORK_TIME6'])
        outfile.write(u'%s|' % store['WORK_TIME7'])
        outfile.write(u'%s|' % store['WORK_TIME8'])
        outfile.write(u'%s|' % store['WORK_TIME9'])
        outfile.write(u'%s|' % store['WORK_TIME10'])
        outfile.write(u'%s|' % store['TEL'])
        outfile.write(u'%s|' % store['E_TEL'])
        outfile.write(u'%s|' % store['HP'])
        outfile.write(u'%s|' % store['PERIOD_TICKET1'])
        outfile.write(u'%s|' % store['PERIOD_TICKET2'])
        outfile.write(u'%s|' % store['PERIOD_TICKET3'])
        outfile.write(u'%s|' % store['PERIOD_TICKET4'])
        outfile.write(u'%s|' % store['PERIOD_TICKET5'])
        outfile.write(u'%s|' % store['DC_TICKET1'])
        outfile.write(u'%s|' % store['DC_TICKET2'])
        outfile.write(u'%s|' % store['DC_TICKET3'])
        outfile.write(u'%s|' % store['DC_TICKET4'])
        outfile.write(u'%s|' % store['DC_TICKET5'])
        outfile.write(u'%s|' % store['COMPANY_NO'])
        outfile.write(u'%s|' % store['BANK_NO'])
        outfile.write(u'%s|' % store['PIC1'])
        outfile.write(u'%s|' % store['PIC2'])
        outfile.write(u'%s|' % store['PIC3'])
        outfile.write(u'%s|' % store['PIC4'])
        outfile.write(u'%s|' % store['PIC5'])
        outfile.write(u'%s|' % store['PLACE_INFO'])
        outfile.write(u'%s|' % store['AREA_INFO'])
        outfile.write(u'%s|' % store['DEPT'])
        outfile.write(u'%s|' % store['DEPT_WOKER'])
        outfile.write(u'%s|' % store['DEPT_CONT_WORKER'])
        outfile.write(u'%s|' % store['CONT_STR_DATE'])
        outfile.write(u'%s|' % store['CONT_END_DATE'])
        outfile.write(u'%s|' % store['OPEN_DATE'])
        outfile.write(u'%s|' % store['CREDIT_COST'])
        outfile.write(u'%s|' % store['RENTAL_COST'])
        outfile.write(u'%s|' % store['REGDT'])
        outfile.write(u'%s|' % store['ETC'])
        outfile.write(u'%s|' % store['SITE_REMOVE'])
        outfile.write(u'%s|' % store['BASIC_TICKET'])
        outfile.write(u'%s|' % store['STATUS'])
        outfile.write(u'%s|' % store['BANK_USER'])
        outfile.write(u'%s|' % store['CARD_SITECODE'])
        outfile.write(u'%s|' % store['CARD_SITEKEY'])
        outfile.write(u'%s|' % store['CARD_SITENAME'])
        outfile.write(u'%s|' % store['CARD_COMPANY'])
        outfile.write(u'%s|' % store['TICKET_END_DATE'])
        outfile.write(u'%s|' % store['PERIOD_ETC'])
        outfile.write(u'%s|' % store['DC_ETC'])
        outfile.write(u'%s|' % store['PERIOD_TICKET6'])
        outfile.write(u'%s|' % store['PERIOD_TICKET7'])
        outfile.write(u'%s|' % store['PERIOD_TICKET8'])
        outfile.write(u'%s|' % store['PERIOD_TICKET9'])
        outfile.write(u'%s|' % store['PERIOD_TICKET10'])
        outfile.write(u'%s|' % store['DC_TICKET6'])
        outfile.write(u'%s|' % store['DC_TICKET7'])
        outfile.write(u'%s|' % store['DC_TICKET8'])
        outfile.write(u'%s|' % store['DC_TICKET9'])
        outfile.write(u'%s|' % store['DC_TICKET10'])
        outfile.write(u'%s|' % store['x'])
        outfile.write(u'%s\n' % store['y'])
    outfile.close()

def getinfo():
    url = 'https://www.gspark24.co.kr/api/parking/ticket/search'
    data = {
        'type': '%EC%A7%80%EC%97%AD%EB%AA%85&keyword=',
        'keyword': '',
        'init': 'true',
        'cpage': ''
    }
    jsonString = requests.post(url, data=data, verify=False).text
    print(url , data)
    jsonData = json.loads(jsonString)
    data = []
    for info in jsonData:
        IDX = info['IDX']
        PARK_AREA_NAME = info['PARK_AREA_NAME']
        E_PARK_AREA_NAME = info['E_PARK_AREA_NAME']
        CAR_PARK_NUM = info['CAR_PARK_NUM']
        PERIOD_PARK_NUM = info['PERIOD_PARK_NUM']
        PARK_KIND = info['PARK_KIND']
        PARK_NUM = info['PARK_NUM']
        PARK_P_NUM = info['PARK_P_NUM']
        ZIP = info['ZIP']
        ADDRESS1 = info['ADDRESS1'].lstrip().rstrip()
        ADDRESS2 = info['ADDRESS2'].lstrip().rstrip()
        E_ADDRESS = info['E_ADDRESS']
        WORK_TIME1 = info['WORK_TIME1']
        WORK_TIME2 = info['WORK_TIME2']
        WORK_TIME3 = info['WORK_TIME3']
        WORK_TIME4 = info['WORK_TIME4']
        WORK_TIME5 = info['WORK_TIME5']
        WORK_TIME6 = info['WORK_TIME6']
        WORK_TIME7 = info['WORK_TIME7']
        WORK_TIME8 = info['WORK_TIME8']
        WORK_TIME9 = info['WORK_TIME9']
        WORK_TIME10 = info['WORK_TIME10']
        TEL = info['TEL']
        E_TEL = info['E_TEL']
        HP = info['HP']
        PERIOD_TICKET1 = info['PERIOD_TICKET1']
        PERIOD_TICKET2 = info['PERIOD_TICKET2']
        PERIOD_TICKET3 = info['PERIOD_TICKET3']
        PERIOD_TICKET4 = info['PERIOD_TICKET4']
        PERIOD_TICKET5 = info['PERIOD_TICKET5']
        DC_TICKET1 = info['DC_TICKET1']
        DC_TICKET2 = info['DC_TICKET2']
        DC_TICKET3 = info['DC_TICKET3']
        DC_TICKET4 = info['DC_TICKET4']
        DC_TICKET5 = info['DC_TICKET5']
        COMPANY_NO = info['COMPANY_NO']
        BANK_NO = info['BANK_NO']
        PIC1 = info['PIC1']
        PIC2 = info['PIC2']
        PIC3 = info['PIC3']
        PIC4 = info['PIC4']
        PIC5 = info['PIC5']
        PLACE_INFO = info['PLACE_INFO']
        AREA_INFO = info['AREA_INFO'].replace('\n','')
        DEPT = info['DEPT']
        DEPT_WOKER = info['DEPT_WOKER']
        DEPT_CONT_WORKER = info['DEPT_CONT_WORKER']
        CONT_STR_DATE = info['CONT_STR_DATE']
        CONT_END_DATE = info['CONT_END_DATE']
        OPEN_DATE = info['OPEN_DATE']
        CREDIT_COST = info['CREDIT_COST']
        RENTAL_COST = info['RENTAL_COST']
        REGDT = info['REGDT']
        ETC = info['ETC'].replace('\n','').replace(' ','')
        SITE_REMOVE = info['SITE_REMOVE']
        BASIC_TICKET = info['BASIC_TICKET']
        STATUS = info['STATUS']
        BANK_USER = info['BANK_USER']
        CARD_SITECODE = info['CARD_SITECODE']
        CARD_SITEKEY = info['CARD_SITEKEY']
        CARD_SITENAME = info['CARD_SITENAME']
        CARD_COMPANY = info['CARD_COMPANY']
        TICKET_END_DATE = info['TICKET_END_DATE']
        PERIOD_ETC = info['PERIOD_ETC'].replace('\n','')
        DC_ETC = info['DC_ETC'].replace('\n','')
        PERIOD_TICKET6 = info['PERIOD_TICKET6']
        PERIOD_TICKET7 = info['PERIOD_TICKET7']
        PERIOD_TICKET8 = info['PERIOD_TICKET8']
        PERIOD_TICKET9 = info['PERIOD_TICKET9']
        PERIOD_TICKET10 = info['PERIOD_TICKET10']
        DC_TICKET6 = info['DC_TICKET6']
        DC_TICKET7 = info['DC_TICKET7']
        DC_TICKET8 = info['DC_TICKET8']
        DC_TICKET9 = info['DC_TICKET9']
        DC_TICKET10 = info['DC_TICKET10']
        x = info['x']
        y = info['y']
        data.append({"IDX":IDX, "PARK_AREA_NAME":PARK_AREA_NAME, "E_PARK_AREA_NAME":E_PARK_AREA_NAME, "CAR_PARK_NUM":CAR_PARK_NUM,
                     "PERIOD_PARK_NUM":PERIOD_PARK_NUM, "PARK_KIND":PARK_KIND, "PARK_NUM":PARK_NUM, "PARK_P_NUM":PARK_P_NUM,
                     "ZIP":ZIP, "ADDRESS1":ADDRESS1, "ADDRESS2":ADDRESS2, "E_ADDRESS":E_ADDRESS, "WORK_TIME1":WORK_TIME1,
                     "WORK_TIME2":WORK_TIME2, "WORK_TIME3":WORK_TIME3, "WORK_TIME4":WORK_TIME4, "WORK_TIME5":WORK_TIME5,
                     "WORK_TIME6":WORK_TIME6, "WORK_TIME7":WORK_TIME7, "WORK_TIME8":WORK_TIME8, "WORK_TIME9":WORK_TIME9,
                     "WORK_TIME10":WORK_TIME10, "TEL":TEL, "E_TEL":E_TEL, "HP":HP, "PERIOD_TICKET1":PERIOD_TICKET1,
                     "PERIOD_TICKET2":PERIOD_TICKET2, "PERIOD_TICKET3":PERIOD_TICKET3, "PERIOD_TICKET4":PERIOD_TICKET4,
                     "PERIOD_TICKET5":PERIOD_TICKET5, "DC_TICKET1":DC_TICKET1, "DC_TICKET2":DC_TICKET2, "DC_TICKET3":DC_TICKET3,
                     "DC_TICKET4":DC_TICKET4, "DC_TICKET5":DC_TICKET5, "COMPANY_NO":COMPANY_NO, "BANK_NO":BANK_NO, "PIC1":PIC1,
                     "PIC2":PIC2, "PIC3":PIC3, "PIC4":PIC4, "PIC5":PIC5, "PLACE_INFO":PLACE_INFO, "AREA_INFO":AREA_INFO, "DEPT":DEPT,
                     "DEPT_WOKER":DEPT_WOKER, "DEPT_CONT_WORKER":DEPT_CONT_WORKER, "CONT_STR_DATE":CONT_STR_DATE, "CONT_END_DATE":CONT_END_DATE,
                     "OPEN_DATE":OPEN_DATE, "CREDIT_COST":CREDIT_COST, "RENTAL_COST":RENTAL_COST, "REGDT":REGDT, "ETC":ETC,
                     "SITE_REMOVE":SITE_REMOVE, "BASIC_TICKET":BASIC_TICKET, "STATUS":STATUS, "BANK_USER":BANK_USER,
                     "CARD_SITECODE":CARD_SITECODE, "CARD_SITEKEY":CARD_SITEKEY, "CARD_SITENAME":CARD_SITENAME,
                     "CARD_COMPANY":CARD_COMPANY, "TICKET_END_DATE":TICKET_END_DATE, "PERIOD_ETC":PERIOD_ETC, "DC_ETC":DC_ETC,
                     "PERIOD_TICKET6":PERIOD_TICKET6, "PERIOD_TICKET7":PERIOD_TICKET7, "PERIOD_TICKET8":PERIOD_TICKET8,
                     "PERIOD_TICKET9":PERIOD_TICKET9, "PERIOD_TICKET10":PERIOD_TICKET10, "DC_TICKET6":DC_TICKET6,
                     "DC_TICKET7":DC_TICKET7, "DC_TICKET8":DC_TICKET8, "DC_TICKET9":DC_TICKET9, "DC_TICKET10":DC_TICKET10,
                     "x":x, "y":y})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()