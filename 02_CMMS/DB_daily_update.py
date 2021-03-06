import cx_Oracle
import csv
import psycopg2
import datetime
import time
import schedule
import os
import sys
import openpyxl
import codecs
import traceback

def main():

    print('Start', datetime.date.today())
    schedule.every().day.at("23:00").do(oracle_export)
    schedule.every().day.at("23:01").do(postgresql_backup_update)
    print('다음 작업 수행 대기중')
    while True :
        schedule.run_pending()

###oracle 의 데이터를 csv로 export!
def oracle_export():
    try:
        LOCATION = r"C:\ora64\instantclient_21_3"
        os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]
        db = cx_Oracle.connect(encoding='UTF-8',
                               nencoding='UTF-8')
        cursor = db.cursor()
        csv_file = open("workList.csv", "w")
        writer = csv.writer(csv_file, lineterminator="\n", delimiter='}', quoting=csv.QUOTE_NONE, escapechar='\\')
        csv_file.write(
            "TYPE}TEXT}NID}LCODE}COMPETE_DATE}LIMIT_DATE}RESULT}REQUEST_DATE}REVIEW_DATE}HEIGHT_LIMIT}WEIGHT_LIMIT}ROAD_WORK}TIME_ID}URL}CREATE_DATE}UPDATE_DATE}DEL_FLAG}POLYGON_TEXT\n")
        r = cursor.execute("SELECT TYPE, REGEXP_replace(REGEXP_replace(REGEXP_replace(text, chr(13)||chr(10), ''),'\\',''),'\n',''), NID, LCODE, COMPLETE_DATE,LIMIT_DATE,RESULT, REQUEST_DATE, REVIEW_DATE,HEIGHT_LIMIT,WEIGHT_LIMIT,ROAD_WORK,TIME_ID,REGEXP_replace(REGEXP_replace(replace(URL, chr(10)||chr(13), ''), '\n',''),chr(34),''), CREATE_DATE,UPDATE_DATE, REGEXP_REPLACE(DEL_FLAG,',',''),sdo_util.to_wktgeometry(gshape) FROM imduser.tbw_dt_infocol")
        for row in r:
            writer.writerow(row)

        cursor.close()
        db.close()
        csv_file.close()
        print('오라클 DB 추출 완료')
    except:
        outfile = codecs.open('Oracle DB export', 'w', 'utf-8')
        write_text = str(datetime.date.today()) + '|' + '오라클 DB 추출 실패' + '|' + str(traceback.format_exc())
        print(traceback.format_exc())
        outfile.write(write_text)
        outfile.close()

def postgresql_backup_update():
    try:
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

        #백업 테이블에 CSV Data inset #칼럼 구조 맞춰 주기
        t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
        t_port = "5432"  # default postgres port
        t_dbname = "postgres"
        t_user = "postgres"
        t_pw = "rjator"
        conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw)
        cursor = conn.cursor()
        csv_file_name = 'workList.csv'
        sql = """
        copy cmms.cmms_list_temp from STDIN DELIMITER '}' HEADER CSV;
        alter table cmms.cmms_list_temp add column poi_cat varchar(20) Null;
        alter table cmms.cmms_list_temp add column poi_date varchar(20) Null;
        alter table cmms.cmms_list_temp add column net_cat varchar(20) Null;
        alter table cmms.cmms_list_temp add column net_date varchar(20) Null;
        alter table cmms.cmms_list_temp add column map_cat varchar(20) Null;
        alter table cmms.cmms_list_temp add column map_date varchar(20) Null;
        alter table cmms.cmms_list_temp add column data_check varchar(20) Null;
        alter table cmms.cmms_list_temp add column service_check varchar(20) Null;
        """
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
        query5 = """
        update cmms_list SET type=cmms_list_temp.type, text=cmms_list_temp.text, nid=cmms_list_temp.nid, lcode=cmms_list_temp.lcode, complete_date=cmms_list_temp.complete_date, limit_date=cmms_list_temp.limit_date, result=cmms_list_temp.result, request_date=cmms_list_temp.request_date, review_date=cmms_list_temp.review_date, height_limit=cmms_list_temp.height_limit, weight_limit=cmms_list_temp.weight_limit, road_work=cmms_list_temp.road_work, time_id=cmms_list_temp.time_id, url=cmms_list_temp.url, create_date=cmms_list_temp.create_date, update_date=cmms_list_temp.update_date, del_flag=cmms_list_temp.del_flag, polygon_text=cmms_list_temp.polygon_text from cmms_list_temp where cmms_list.nid = cmms_list_temp.nid;
        insert into cmms_list (type, text, nid, lcode, complete_date, limit_date, result, request_date, review_date, height_limit, weight_limit, road_work, time_id,poi_cat,poi_date,net_cat,net_date,map_cat,map_date,data_check,service_check, url, create_date, update_date, del_flag, polygon_text) 
        select a.type, a.text, a.nid ,a.lcode, a.complete_date, a.limit_date, a.result, a.request_date, a.review_date, a.height_limit, a.weight_limit, a.road_work, a.time_id ,a.poi_cat,a.poi_date,a.net_cat,a.net_date,a.map_cat,a.map_date,a.data_check,a.service_check, a.url, a.create_date, a.update_date, a.del_flag, a.polygon_text
        from cmms_list_temp a
        left join cmms_list
        on  cmms_list.nid = a.nid 
        where cmms_list.nid is null;   
        """
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
    except:
        outfile = codecs.open('DB_UPDATE_FAIL.txt', 'w', 'utf-8')
        write_text = str(datetime.date.today()) + '|' + 'DB동기화 실패' + '|' + str(traceback.format_exc())
        print(traceback.format_exc())
        outfile.write(write_text)
        outfile.close()

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

