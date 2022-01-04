# -*- coding: utf-8 -*-
# 1. 폴더 내의 파일 중 AlterD.JUSUBM.YYYYMMDD.TI_SPBD_BULD.TXT  형식을 가진 텍스트 파일만 리스트( 풀경로 ) 로 추출
# 2. postgresql 에 리스트 경로의 txt 파일을 인서트.

import os
import codecs
import psycopg2
import time


def main():

    list = file_list()

    for path in list:
        insert_data(path)
        print(path)
        time.sleep(2)


def list_save(dirname):
    outfile = codecs.open('raw_file_list.txt', 'a')
    file_list = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        if os.path.isdir(full_filename):
            list_save(full_filename)
        else:
            # ext = os.path.splitext(full_filename)[-1]
            # if ext == '.csv':
            print(full_filename)
            fullname_fix = full_filename.upper()
            fullname = full_filename + '\n'
            if fullname_fix.endswith('.TI_SPBD_BULD.TXT') == True :
                outfile.write(fullname)
                file_list.append(full_filename)
            else: pass
                # QApplication.processEvents()
    outfile.close()
    return file_list

def file_list():
    with open('raw_file_list.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    return SearchList

def insert_data(path):
    try:
        conn = psycopg2.connect(host="192.168.11.61", database="postgres", user="postgres",
                                password="rjator", port="5432", options="-c search_path=TI_SPBD_BULD")
        print('DB connected')

    except (Exception, psycopg2.Error) as error:
        # Confirm unsuccessful connection and stop program execution.
        print("Error while fetching data from PostgreSQL", error)
        print("Database connection unsuccessful.")
        quit()
    cur = conn.cursor()

    query = "INSERT INTO TI_SPBD_BULD_MERGE2(법정동코드, 시도명, 시군구명, 법정읍면동명, 법정리명, 산여부, 지번본번, 지번부번, 도로명코드, 도로명, 지하여부, 건물본번,건물부번, 건축물대장건물명, 상세건물명,건물관리번호, 읍면동일련번호, 행정동코드, 행정동명, 우편번호, 우편일련번호, 다량배달처명, 이동사유코드, 변동일자, 변동전도로명주소, 시군구용건물명, 공동주택여부,기초구역번호,상세주소여부, 비고1, 비고2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    f = open(path, 'r')
    content = f.readlines()
    values = [line.strip().split('|') for line in content]

    if content[0] == 'No Data' : pass
    else:
        try:
            cur.executemany(query, values)
        except (Exception, psycopg2.DatabaseError) as error:
            quit()
            print(error)
        except IndexError :
            pass
        finally:
            if conn is not None:
                conn.commit()
                conn.close()

def create_table():
    try:
        conn = psycopg2.connect(host="192.168.11.61", database="postgres", user="postgres",
                                password="rjator", port="5432", options="-c search_path=TI_SPBD_BULD")
        print('DB connected')

    except (Exception, psycopg2.Error) as error:
        # Confirm unsuccessful connection and stop program execution.
        print("Error while fetching data from PostgreSQL", error)
        print("Database connection unsuccessful.")
        quit()
    cur = conn.cursor()

    create_table = "CREATE TABLE TI_SPBD_BULD.TI_SPBD_BULD_MERGE2(법정동코드 varchar,시도명 varchar,시군구명 varchar,법정읍면동명 varchar,법정리명 varchar,산여부 varchar,지번본번 integer,지번부번 integer,도로명코드 varchar,도로명 varchar,지하여부 varchar,건물본번 integer,건물부번 integer,건축물대장건물명 varchar,상세건물명 varchar,건물관리번호 varchar,읍면동일련번호 varchar,행정동코드 varchar,행정동명 varchar,우편번호 varchar,우편일련번호 varchar,다량배달처명 varchar,이동사유코드 varchar,변동일자 varchar,변동전도로명주소 varchar,시군구용건물명 varchar,공동주택여부 varchar,기초구역번호 varchar,상세주소여부 varchar,비고1 varchar,비고2 varchar)"
    cur.execute(create_table)
    conn.commit()
# create_table()
# list_save('C:\\Users\\jyseol\\Downloads\\rowdata')
main()


def insert_data(path):
    print(path)
    try:
        conn = psycopg2.connect(host="192.168.11.61", database="postgres", user="postgres",
                                password="rjator", port="5432", options="-c search_path=TI_SPBD_BULD")
        print('DB connected')

    except (Exception, psycopg2.Error) as error:
        # Confirm unsuccessful connection and stop program execution.
        print("Error while fetching data from PostgreSQL", error)
        print("Database connection unsuccessful.")
        quit()
    cur = conn.cursor()

    query = "INSERT INTO TI_SPBD_BULD_MERGE2(법정동코드, 시도명, 시군구명, 법정읍면동명, 법정리명, 산여부, 지번본번, 지번부번, 도로명코드, 도로명, 지하여부, 건물본번,건물부번, 건축물대장건물명, 상세건물명,건물관리번호, 읍면동일련번호, 행정동코드, 행정동명, 우편번호, 우편일련번호, 다량배달처명, 이동사유코드, 변동일자, 변동전도로명주소, 시군구용건물명, 공동주택여부,기초구역번호,상세주소여부, 비고1, 비고2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    f = open(path, 'r')
    content = f.readlines()
    print(content[0])
    values = [line.strip().split('|') for line in content]
    if content[0] == 'No Data' : pass
    else:
        try:
            cur.executemany(query, values)
        except (Exception, psycopg2.DatabaseError) as error:
            quit()
            print(error)
        except IndexError :
            pass
        finally:
            if conn is not None:
                conn.commit()
                conn.close()

# insert_data('C:\\Users\\jyseol\\Downloads\\rowdata\\2020\\2020-01\\20200126\\AlterD.JUSUBM.20200126.TI_SPBD_BULD.TXT')

