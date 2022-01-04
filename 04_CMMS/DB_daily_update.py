import smtplib
from email.mime.text import MIMEText
import cx_Oracle
import csv
import psycopg2
import datetime
import time
import schedule
import os
import sys
import openpyxl

###oracle 의 데이터를 csv로 export!
def oracle_export():
    LOCATION = r"C:\ora64\instantclient_21_3"
    os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]
    db = cx_Oracle.connect('contentsteam', 'zjsxpscm', '192.168.10.30:1521/imdb', encoding='UTF-8',
                           nencoding='UTF-8')
    cursor = db.cursor()
    csv_file = open("workList.csv", "w")
    writer = csv.writer(csv_file, lineterminator="\n", delimiter='}', quoting=csv.QUOTE_NONE, escapechar='\\')
    csv_file.write(
        "TYPE}TEXT}NID}LCODE}COMPETE_DATE}LIMIT_DATE}RESULT}REQUEST_DATE}REVIEW_DATE}HEIGHT_LIMIT}WEIGHT_LIMIT}ROAD_WORKD}TIME_ID}URL}CREATE_DATE}UPDATE_DATE}DEL_FLAG}POLYGON_TEXT\n")
    r = cursor.execute("SELECT TYPE, REGEXP_replace(REGEXP_replace(REGEXP_replace(text, chr(13)||chr(10), ''),'\\',''),'\n',''), NID, LCODE, COMPLETE_DATE,LIMIT_DATE,RESULT, REQUEST_DATE, REVIEW_DATE,HEIGHT_LIMIT,WEIGHT_LIMIT,ROAD_WORK,TIME_ID,REGEXP_replace(REGEXP_replace(replace(URL, chr(10)||chr(13), ''), '\n',''),chr(34),''), CREATE_DATE,UPDATE_DATE, REGEXP_REPLACE(DEL_FLAG,',',''),sdo_util.to_wktgeometry(gshape) FROM imduser.tbw_dt_infocol")
    for row in r:
        writer.writerow(row)

    cursor.close()
    db.close()
    csv_file.close()
    print('오라클 DB 추출 완료')

def postgresql_backup_update():
    # 기존 백업 테이블 있으면 삭제.
    try:
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
        cursor = conn.cursor()
        date = str(datetime.date.today()).replace('-', '')
        query1 = "drop table cmms.cmms_list_{};".format(date)
        cursor.execute(query1)
        conn.commit()
        conn.close()
        print('기존 백업_날짜 테이블 삭제.')
        time.sleep(1)
    except :
        pass

    # 테이블 구조 전체를 백업테이블에 복사
    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
    t_port = "5432"  # default postgres port
    t_dbname = "postgres"
    t_user = "postgres"
    t_pw = "rjator"
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    date = str(datetime.date.today()).replace('-', '')
    query1 = "create table cmms.cmms_list_{} (like cmms.cmms_list including all);".format(date)
    cursor.execute(query1)
    conn.commit()
    conn.close()
    print('백업 테이블 생성 완료')
    time.sleep(1)

    #테이블 내용 백업 테이블에 전체 복사
    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
    t_port = "5432"  # default postgres port
    t_dbname = "postgres"
    t_user = "postgres"
    t_pw = "rjator"
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    date = str(datetime.date.today()).replace('-', '')
    query2 = "insert into cmms.cmms_list_{} (select * from cmms.cmms_list);".format(date)
    cursor.execute(query2)
    conn.commit()
    conn.close()
    print('백업 테이블 데이터 복사 완료')
    time.sleep(1)

    #################### 여기부터는 기존 테이블 업데이트를 위한 코드 ####################
    #백업 테이블 이미 있으면 삭제.
    try:
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
        cursor = conn.cursor()
        query3 = "drop table cmms.cmms_list_temp;"
        cursor.execute(query3)
        conn.commit()
        conn.close()
        print('기존 백업 테이블 삭제.')
        time.sleep(1)
    except:
        pass

    #백업 테이블 생성 및 구조 복사
    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
    t_port = "5432"  # default postgres port
    t_dbname = "postgres"
    t_user = "postgres"
    t_pw = "rjator"
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    query3 = "create table cmms.cmms_list_temp (like cmms.cmms_list including all);"
    cursor.execute(query3)
    conn.commit()
    conn.close()
    print('ORACLE DATA 인서트를 위한 임시 테이블 생성 완료')
    time.sleep(1)

    #백업 테이블 칼럼을 지워서 csv 칼럼과 동일하게 만듦
    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
    t_port = "5432"  # default postgres port
    t_dbname = "postgres"
    t_user = "postgres"
    t_pw = "rjator"
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    query4 = "alter table cmms.cmms_list_temp drop column cmms_update_date, drop column poi_cat, drop column poi_date, drop column net_cat, drop column net_date, drop column map_cat, drop column map_date, drop column data_check, drop column service_check;"
    cursor.execute(query4)
    conn.commit()
    conn.close()
    print('임시 테이블의 일부 칼럼 삭제')
    time.sleep(1)

    #백업 테이블에 CSV Data inset
    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
    t_port = "5432"  # default postgres port
    t_dbname = "postgres"
    t_user = "postgres"
    t_pw = "rjator"
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    csv_file_name = 'workList.csv'
    sql = "copy cmms.cmms_list_temp from STDIN DELIMITER '}' HEADER CSV"
    cursor.copy_expert(sql,open(csv_file_name, "r"))
    conn.commit()
    conn.close()
    print("임시 테이블 Data Insert 완료")
    time.sleep(1)

    #백업테이블 데이터 cmms_list 로 업데이트.
    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
    t_port = "5432"  # default postgres port
    t_dbname = "postgres"
    t_user = "postgres"
    t_pw = "rjator"
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw, options="-c search_path=cmms")
    cursor = conn.cursor()
    query5 = "update cmms_list SET type=cmms_list_temp.type, text=cmms_list_temp.text, lcode=cmms_list_temp.lcode, result=cmms_list_temp.result, request_date=cmms_list_temp.request_date, review_date=cmms_list_temp.review_date, url=cmms_list_temp.url, del_flag=cmms_list_temp.del_flag, polygon_text =cmms_list_temp.polygon_text  from cmms_list_temp  where cmms_list.nid = cmms_list_temp.nid;"
    cursor.execute(query5)
    conn.commit()
    conn.close()
    print("cmms_list 테이블 업데이트 완료")
    time.sleep(1)

    # 구축시한 값이 변경될 경우 구축완료 상태인 것들 요청으로 변경하기.
    try:
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw,
                                options="-c search_path=cmms")
        cursor = conn.cursor()
        query5 = "update cmms_list SET poi_cat = '구축요청' where nid in (select nid from cmms_list where nid in (select A.nid from cmms_list A, cmms_list_temp b where a.limit_date <> b.limit_date and a.nid = b.nid)) and poi_cat = '구축완료';"
        cursor.execute(query5)
        conn.commit()
        conn.close()
        print("POI 구축시한 변경 된 케이스 중 구축완료 상태인것들 구축요청으로 변경")
    except : pass

    try:
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw,
                                options="-c search_path=cmms")
        cursor = conn.cursor()
        query5 = "update cmms_list SET net_cat = '구축요청' where nid in (select nid from cmms_list where nid in (select A.nid from cmms_list A, cmms_list_temp b where a.limit_date <> b.limit_date and a.nid = b.nid)) and net_cat = '구축완료';"
        cursor.execute(query5)
        conn.commit()
        conn.close()
        print("NET 구축시한 변경 된 케이스 중 구축완료 상태인것들 구축요청으로 변경")
    except : pass

    try:
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw,
                                options="-c search_path=cmms")
        cursor = conn.cursor()
        query5 = "update cmms_list SET map_cat = '구축요청' where nid in (select nid from cmms_list where nid in (select A.nid from cmms_list A, cmms_list_temp b where a.limit_date <> b.limit_date and a.nid = b.nid)) and map_cat = '구축완료';"
        cursor.execute(query5)
        conn.commit()
        conn.close()
        print("MAP 구축시한 변경 된 케이스 중 구축완료 상태인것들 구축요청으로 변경")
    except : pass

    # 백업 테이블 삭제.
    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
    t_port = "5432"  # default postgres port
    t_dbname = "postgres"
    t_user = "postgres"
    t_pw = "rjator"
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    query6 = "drop table cmms.cmms_list_temp;"
    cursor.execute(query6)
    conn.commit()
    conn.close()
    print("임시 테이블 Drop 완료")

    #type 에 따라 poi_cat, net_cat, map_cat 칼럼의 요청 상태 값 설정, null 일 경우 에만 설정. 최초 1회 입력 업데이트 쿼리도 처음에만 세팅.
    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
    t_port = "5432"  # default postgres port
    t_dbname = "postgres"
    t_user = "postgres"
    t_pw = "rjator"
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    query6 = "update cmms.cmms_list SET poi_cat = '구축요청' where poi_cat is NULL and type not in ('도로 : 고속도로', '도로 : 도시고속화도로','도로 : 국도','도로 : 지방도','도로 : 주요간선','도로 : 일반도로','도로 : 기타(도로관련)') "
    cursor.execute(query6)
    conn.commit()
    conn.close()
    print("구축 요청 설정 ELSE.")

    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
    t_port = "5432"  # default postgres port
    t_dbname = "postgres"
    t_user = "postgres"
    t_pw = "rjator"
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    query6 = "update cmms.cmms_list SET net_cat = '구축요청' where net_cat is NULL and type not in ('도로 : 고속도로', '도로 : 도시고속화도로','도로 : 국도','도로 : 지방도','도로 : 주요간선','도로 : 일반도로','도로 : 기타(도로관련)') "
    cursor.execute(query6)
    conn.commit()
    conn.close()
    print("구축 요청 설정 ELSE.")

    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
    t_port = "5432"  # default postgres port
    t_dbname = "postgres"
    t_user = "postgres"
    t_pw = "rjator"
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    query6 = "update cmms.cmms_list SET map_cat = '구축요청' where map_cat is NULL and type not in ('도로 : 고속도로', '도로 : 도시고속화도로','도로 : 국도','도로 : 지방도','도로 : 주요간선','도로 : 일반도로','도로 : 기타(도로관련)') "
    cursor.execute(query6)
    conn.commit()
    conn.close()
    print("구축 요청 설정 ELSE.")

    t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
    t_port = "5432"  # default postgres port
    t_dbname = "postgres"
    t_user = "postgres"
    t_pw = "rjator"
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    query6 = "update cmms.cmms_list SET net_cat = '구축요청' where net_cat is NULL and type in ('도로 : 고속도로', '도로 : 도시고속화도로','도로 : 국도','도로 : 지방도','도로 : 주요간선','도로 : 일반도로','도로 : 기타(도로관련)') "
    cursor.execute(query6)
    conn.commit()
    conn.close()
    print("구축 요청 설정 NET.")


    #7일 전 백업 DB는 삭제.
    try:
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
        delete_date = datetime.datetime.now() - datetime.timedelta(days=7)
        delete_date = str(delete_date).split(' ')[0]
        delete_date = delete_date.replace('-', '')
        cursor = conn.cursor()
        query6 = "drop table cmms.cmms_list_{};".format(delete_date)
        cursor.execute(query6)
        conn.commit()
        conn.close()
    except :
        pass
        print('7일전 DB 삭제 실패.')
    print(datetime.date.today(), '날짜의 데이터 백업 완료')

#######################################################################################################################
###########################################메일 보내기 함수###############################################################
#
# def SendMail():
#     close_poi_nid_list = str(close_poi_nid_list_export()).replace('(','').replace(',)','').replace('[','(').replace(']',')')
#     close_net_nid_list = str(close_net_nid_list_export()).replace('(','').replace(',)','').replace('[','(').replace(']',')')
#     close_map_nid_list = str(close_map_nid_list_export()).replace('(','').replace(',)','').replace('[','(').replace(']',')')
#     delay_poi_nid_list=str(delay_poi_nid_list_export()).replace('(','').replace(',)','').replace('[','(').replace(']',')')
#     delay_net_nid_list=str(delay_net_nid_list_export()).replace('(','').replace(',)','').replace('[','(').replace(']',')')
#     delay_map_nid_list=str(delay_map_nid_list_export()).replace('(','').replace(',)','').replace('[','(').replace(']',')')
#     if close_poi_nid_list != [] or delay_poi_nid_list_export != []:
#         smtpName = "smtp.naver.com"
#         smtpPort = 587
#
#         sendEmail = "soelyh1005@naver.com"
#         password = "Wnsdud87!"
#         # recvEmail = 'hd.kim@mappers.kr','habang@mappers.kr','arhan@mappers.kr'
#         recvEmail = 'jyseol@mappers.kr'
#
#         title = "CMMS 구축 요청 알림(POI)"
#         content = """
#         #아래 리스트들에 대한 구축 요청 알림#\n
#         임박 NID = {}
#         지연 NID = {}
#         """.format(close_poi_nid_list,delay_poi_nid_list)
#
#         msg = MIMEText(content)
#         msg['From'] = sendEmail
#         msg['To'] = recvEmail
#         msg['Subject'] = title
#
#         s = smtplib.SMTP(smtpName, smtpPort)
#         s.starttls()
#         s.login(sendEmail, password)
#         s.sendmail(sendEmail, recvEmail, msg.as_string())
#         s.close()
#     else:
#         pass
#     ###############
#     if close_net_nid_list != [] or delay_net_nid_list != []:
#         smtpName = "smtp.naver.com"
#         smtpPort = 587
#
#         sendEmail = "soelyh1005@naver.com"
#         password = "Wnsdud87!"
#         # recvEmail = "khkim@mappers.kr" , "pgpark@mappers.kr"
#         recvEmail = 'jyseol@mappers.kr'
#
#         title = "CMMS 구축 요청 알림(NET)"
#         content = """
#         #아래 리스트들에 대한 구축 요청 알림#\n
#         임박 NID = {}
#         지연 NID = {}
#         """.format(close_net_nid_list, delay_net_nid_list)
#
#         msg = MIMEText(content)
#         msg['From'] = sendEmail
#         msg['To'] = recvEmail
#         msg['Subject'] = title
#
#         s = smtplib.SMTP(smtpName, smtpPort)
#         s.starttls()
#         s.login(sendEmail, password)
#         s.sendmail(sendEmail, recvEmail, msg.as_string())
#         s.close()
#     else:
#         pass
#     #################
#     if close_map_nid_list != [] or delay_map_nid_list != []:
#         smtpName = "smtp.naver.com"
#         smtpPort = 587
#
#         sendEmail = "soelyh1005@naver.com"
#         password = "Wnsdud87!"
#         # recvEmail = 'hecho@mappers.kr', 'jmlim@mappers.kr', 'jhkim@mappers.kr'
#         recvEmail = 'jyseol@mappers.kr'
#
#         title = "CMMS 구축 요청 알림(MAP)"
#         content = """
#         #아래 리스트들에 대한 구축 요청 알림#\n
#         임박 NID = {}
#         지연 NID = {}
#         """.format(close_map_nid_list, delay_map_nid_list)
#
#         msg = MIMEText(content)
#         msg['From'] = sendEmail
#         msg['To'] = recvEmail
#         msg['Subject'] = title
#
#         s = smtplib.SMTP(smtpName, smtpPort)
#         s.starttls()
#         s.login(sendEmail, password)
#         s.sendmail(sendEmail, recvEmail, msg.as_string())
#         s.close()
#     else:
#         pass
#     print("메일 발송 완료")
#
# def close_poi_nid_list_export():
#     dday10 = str(datetime.datetime.now() - datetime.timedelta(days=10)).replace('-', '').split(' ')[0]
#     dday9 = str(datetime.datetime.now() - datetime.timedelta(days=9)).replace('-', '').split(' ')[0]
#     dday8 = str(datetime.datetime.now() - datetime.timedelta(days=8)).replace('-', '').split(' ')[0]
#     dday7 = str(datetime.datetime.now() - datetime.timedelta(days=7)).replace('-', '').split(' ')[0]
#     dday6 = str(datetime.datetime.now() - datetime.timedelta(days=6)).replace('-', '').split(' ')[0]
#     dday5 = str(datetime.datetime.now() - datetime.timedelta(days=5)).replace('-', '').split(' ')[0]
#     dday4 = str(datetime.datetime.now() - datetime.timedelta(days=4)).replace('-', '').split(' ')[0]
#     dday3 = str(datetime.datetime.now() - datetime.timedelta(days=3)).replace('-', '').split(' ')[0]
#     dday2 = str(datetime.datetime.now() - datetime.timedelta(days=2)).replace('-', '').split(' ')[0]
#     dday1 = str(datetime.datetime.now() - datetime.timedelta(days=1)).replace('-', '').split(' ')[0]
#     dday0 = str(datetime.date.today()).replace('-', '')
#     dday_list = (dday10, dday9, dday8, dday7, dday6, dday5, dday4, dday3, dday2, dday1, dday0)
#
#     t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
#     t_port = "5432"  # default postgres port
#     t_dbname = "postgres"
#     t_user = "postgres"
#     t_pw = "rjator"
#     conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
#     cursor = conn.cursor()
#     query = "select nid from cmms.cmms_list where poi_cat in ('구축요청','예정') and limit_date in {} and del_flag = '0' and data_check is NULL;".format(dday_list)
#     cursor.execute(query)
#     a = cursor.fetchall()
#     conn.close()
#     return a
#
# def close_net_nid_list_export():
#     dday10 = str(datetime.datetime.now() - datetime.timedelta(days=10)).replace('-', '').split(' ')[0]
#     dday9 = str(datetime.datetime.now() - datetime.timedelta(days=9)).replace('-', '').split(' ')[0]
#     dday8 = str(datetime.datetime.now() - datetime.timedelta(days=8)).replace('-', '').split(' ')[0]
#     dday7 = str(datetime.datetime.now() - datetime.timedelta(days=7)).replace('-', '').split(' ')[0]
#     dday6 = str(datetime.datetime.now() - datetime.timedelta(days=6)).replace('-', '').split(' ')[0]
#     dday5 = str(datetime.datetime.now() - datetime.timedelta(days=5)).replace('-', '').split(' ')[0]
#     dday4 = str(datetime.datetime.now() - datetime.timedelta(days=4)).replace('-', '').split(' ')[0]
#     dday3 = str(datetime.datetime.now() - datetime.timedelta(days=3)).replace('-', '').split(' ')[0]
#     dday2 = str(datetime.datetime.now() - datetime.timedelta(days=2)).replace('-', '').split(' ')[0]
#     dday1 = str(datetime.datetime.now() - datetime.timedelta(days=1)).replace('-', '').split(' ')[0]
#     dday0 = str(datetime.date.today()).replace('-', '')
#     dday_list = (dday10, dday9, dday8, dday7, dday6, dday5, dday4, dday3, dday2, dday1, dday0)
#
#     t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
#     t_port = "5432"  # default postgres port
#     t_dbname = "postgres"
#     t_user = "postgres"
#     t_pw = "rjator"
#     conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
#     cursor = conn.cursor()
#     query = "select nid from cmms.cmms_list where net_cat in ('구축요청','예정') and limit_date in {} and del_flag = '0' and data_check is NULL;".format(dday_list)
#     cursor.execute(query)
#     a = cursor.fetchall()
#     conn.close()
#     return a
#
# def close_map_nid_list_export():
#     dday10 = str(datetime.datetime.now() - datetime.timedelta(days=10)).replace('-', '').split(' ')[0]
#     dday9 = str(datetime.datetime.now() - datetime.timedelta(days=9)).replace('-', '').split(' ')[0]
#     dday8 = str(datetime.datetime.now() - datetime.timedelta(days=8)).replace('-', '').split(' ')[0]
#     dday7 = str(datetime.datetime.now() - datetime.timedelta(days=7)).replace('-', '').split(' ')[0]
#     dday6 = str(datetime.datetime.now() - datetime.timedelta(days=6)).replace('-', '').split(' ')[0]
#     dday5 = str(datetime.datetime.now() - datetime.timedelta(days=5)).replace('-', '').split(' ')[0]
#     dday4 = str(datetime.datetime.now() - datetime.timedelta(days=4)).replace('-', '').split(' ')[0]
#     dday3 = str(datetime.datetime.now() - datetime.timedelta(days=3)).replace('-', '').split(' ')[0]
#     dday2 = str(datetime.datetime.now() - datetime.timedelta(days=2)).replace('-', '').split(' ')[0]
#     dday1 = str(datetime.datetime.now() - datetime.timedelta(days=1)).replace('-', '').split(' ')[0]
#     dday0 = str(datetime.date.today()).replace('-', '')
#     dday_list = (dday10, dday9, dday8, dday7, dday6, dday5, dday4, dday3, dday2, dday1, dday0)
#
#     t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
#     t_port = "5432"  # default postgres port
#     t_dbname = "postgres"
#     t_user = "postgres"
#     t_pw = "rjator"
#     conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
#     cursor = conn.cursor()
#     query = "select nid from cmms.cmms_list where map_cat in ('구축요청','예정') and limit_date in {} and del_flag = '0' and data_check is NULL;".format(dday_list)
#     cursor.execute(query)
#     a = cursor.fetchall()
#     conn.close()
#     return a
#
# def delay_poi_nid_list_export():
#     dday0 = str(datetime.date.today())
#     t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
#     t_port = "5432"  # default postgres port
#     t_dbname = "postgres"
#     t_user = "postgres"
#     t_pw = "rjator"
#     conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
#     cursor = conn.cursor()
#     query = "select nid from cmms.cmms_list where poi_cat in ('구축요청','예정') and limit_date < '{}' and del_flag = '0' and data_check is NULL;".format(dday0)
#     cursor.execute(query)
#     a = cursor.fetchall()
#     conn.close()
#     return a
#
# def delay_net_nid_list_export():
#     dday0 = str(datetime.date.today())
#     t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
#     t_port = "5432"  # default postgres port
#     t_dbname = "postgres"
#     t_user = "postgres"
#     t_pw = "rjator"
#     conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
#     cursor = conn.cursor()
#     query = "select nid from cmms.cmms_list where net_cat in ('구축요청','예정') and limit_date < '{}' and del_flag = '0' and data_check is NULL;".format(dday0)
#     cursor.execute(query)
#     a = cursor.fetchall()
#     conn.close()
#     return a
#
# def delay_map_nid_list_export():
#     dday0 = str(datetime.date.today())
#     t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
#     t_port = "5432"  # default postgres port
#     t_dbname = "postgres"
#     t_user = "postgres"
#     t_pw = "rjator"
#     conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
#     cursor = conn.cursor()
#     query = "select nid from cmms.cmms_list where map_cat in ('구축요청','예정') and limit_date < '{}' and del_flag = '0' and data_check is NULL;".format(dday0)
#     cursor.execute(query)
#     a = cursor.fetchall()
#     conn.close()
#     return a


######### test#######
# print('Start', datetime.date.today())
# schedule.every().day.at("15:14").do(oracle_export)
# schedule.every().day.at("15:14").do(postgresql_backup_update)
# schedule.every().day.at("15:13").do(SendMail)
# print('다음 작업 수행 대기중')
#
# while True :
#     schedule.run_pending()

print('Start', datetime.date.today())
# schedule.every().day.at("08:00").do(SendMail)
schedule.every().day.at("23:00").do(oracle_export)
schedule.every().day.at("23:05").do(postgresql_backup_update)

print('다음 작업 수행 대기중')
while True :
    schedule.run_pending()


# postgresql_backup_update()
# oracle_export()