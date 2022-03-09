import cx_Oracle
import os
import csv
import psycopg2
import sys
import datetime
import time
import schedule

###oracle 의 데이터를 csv로 export
# update cmms_list set poi_cat = cmms_origin.poi_cat , net_cat = cmms_origin.net_cat ,map_cat = cmms_origin.map_cat,poi_date = cmms_origin.poi_date , net_date = cmms_origin.net_date ,map_date = cmms_origin.map_date,data_check = cmms_origin.data_check, service_check = cmms_origin.service_check from cmms_origin where cmms_list.nid = cmms_origin.nid;
def oracle_export():
    LOCATION = r"C:\ora64\instantclient_21_3"
    os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]
    db = cx_Oracle.connect(, encoding='UTF-8',
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

def postgresqol_table_create():
    t_host = # either "localhost", a domain name, or an IP address.
    t_port = # default postgres port
    t_dbname = 
    t_user = 
    t_pw = 
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    query = """
    CREATE TABLE cmms.cmms_list (
        "type" varchar(128) NOT NULL,
        "text" varchar(512) NULL,
        nid integer NOT NULL PRIMARY KEY,
        lcode varchar(20) NULL,
        complete_date date NULL,
        limit_date date NULL,
        "result" varchar(8) NULL,
        request_date varchar(10) NULL,
        review_date varchar(10) NULL,
        height_limit varchar(10) NULL,
        weight_limit varchar(10) NULL,
        road_work varchar(50) NULL,
        time_id varchar(50) NULL,
        poi_cat varchar(20) NULL check (poi_cat in ('해당없음','구축요청', '예정', '완료', '확인', '')),
        poi_date varchar(20) NULL,
        net_cat varchar(20) NULL check (net_cat in ('해당없음','구축요청', '예정', '완료', '확인', '')),
        net_date varchar(20) NULL,
        map_cat varchar(20) NULL check (map_cat in ('해당없음','구축요청', '예정', '완료', '확인', '')),
        map_date varchar(20) NULL,
        data_check varchar(10) NULL check (data_check in ('Yes', 'No','YES', 'NO', '')),
        service_check varchar(10) NULL check (service_check in ('Yes', 'No','YES', 'NO', '')),
        url varchar(600) NULL,
        create_date date NULL,
        update_date date NULL,
        del_flag varchar(2) NULL,
        cmms_update_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
        polygon_text varchar NULL
    );
    """
    cursor.execute(query)
    conn.commit()
    conn.close()

def postgresql_backup_update():
    #################### 여기부터는 기존 테이블 업데이트를 위한 코드 ####################

    # 백업 테이블 생성 및 구조 복사
    t_host = # either "localhost", a domain name, or an IP address.
    t_port = # default postgres port
    t_dbname = 
    t_user = 
    t_pw = 
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    query3 = "create table cmms.cmms_list_temp (like cmms.cmms_list including all);"
    cursor.execute(query3)
    conn.commit()
    conn.close()
    print('ORACLE DATA 인서트를 위한 임시 테이블 생성 완료')
    time.sleep(1)

    #백업 테이블 칼럼을 지워서 csv 칼럼과 동일하게 만듦
    t_host = # either "localhost", a domain name, or an IP address.
    t_port = # default postgres port
    t_dbname = 
    t_user = 
    t_pw = 
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    query4 = "alter table cmms.cmms_list_temp drop column cmms_update_date, drop column poi_cat, drop column poi_date, drop column net_cat, drop column net_date, drop column map_cat, drop column map_date, drop column data_check, drop column service_check;"
    cursor.execute(query4)
    conn.commit()
    conn.close()
    print('임시 테이블의 일부 칼럼 삭제')
    time.sleep(1)

    #백업 테이블에 CSV Data inset
    t_host = # either "localhost", a domain name, or an IP address.
    t_port = # default postgres port
    t_dbname = 
    t_user = 
    t_pw = 
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
    t_host = # either "localhost", a domain name, or an IP address.
    t_port = # default postgres port
    t_dbname = 
    t_user = 
    t_pw = 
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw, options="-c search_path=cmms")
    cursor = conn.cursor()
    query5 = "insert into cmms_list(type, text, nid, lcode, complete_date, limit_date ,result, request_date, review_date, height_limit, weight_limit, road_work, time_id, url, create_date, update_date, del_flag, polygon_text) select * from cmms_list_temp ;"
    cursor.execute(query5)
    conn.commit()
    conn.close()
    print("cmms_list 테이블 업데이트 완료")
    time.sleep(1)

    # 백업 테이블 삭제.
    t_host = # either "localhost", a domain name, or an IP address.
    t_port = # default postgres port
    t_dbname = 
    t_user = 
    t_pw = 
    conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
    cursor = conn.cursor()
    query6 = "drop table cmms.cmms_list_temp;"
    cursor.execute(query6)
    conn.commit()
    conn.close()
    print("임시 테이블 Drop 완료")


# oracle_export()
# postgresqol_table_create()

postgresql_backup_update()