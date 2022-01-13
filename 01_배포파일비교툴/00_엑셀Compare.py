from glob import glob
import sys
import codecs
import time
import random
import pandas as pd
import os

def main():

    old = get_old_xlsx_list()
    new = get_new_xlsx_list()
    for olds,news in zip(old, new):
        print(olds, news)
        compare_excel(olds,news,'BRANCH')

def compare_excel(old_xlsx, new_xlsx, column_name):
    import pandas as pd

    df_old = pd.read_excel(old_xlsx)
    df_new = pd.read_excel(new_xlsx)

    # 불러온 데이터의 버전 구분
    df_old['ver'] = 'old'
    df_new['ver'] = 'new'

    id_dropped = set(df_old[column_name]) - set(df_new[column_name])
    id_added = set(df_new[column_name]) - set(df_old[column_name])

    # 삭제된 데이터
    df_dropped = df_old[df_old[column_name].isin(id_dropped)].iloc[:, :-1]
    # 추가된 데이터
    df_added = df_new[df_new[column_name].isin(id_added)].iloc[:, :-1]

    #두 데이터프레임을 하나로 합침
    df_concatted = pd.concat([df_old, df_new], ignore_index=True)
    #모든 컬럼의 내용이 중복되는 데이터는 삭제
    changes = df_concatted.drop_duplicates(df_concatted.columns[:-1], keep='last')

    #남은 데이터 중 동일한 아이디 값이 두개 이상 존재하면 정보가 변경된 데이터.
    duplicated_list = changes[changes[column_name].duplicated()][column_name].to_list()
    df_changed = changes[changes[column_name].isin(duplicated_list)]

    df_changed_old = df_changed[df_changed['ver'] == 'old'].iloc[:, :-1]
    df_changed_old.sort_values(by=column_name, inplace=True)

    df_changed_new = df_changed[df_changed['ver'] == 'new'].iloc[:, :-1]
    df_changed_new.sort_values(by=column_name, inplace=True)

    # 정보가 변경된 데이터 정리
    df_info_changed = df_changed_old.copy()
    for i in range(len(df_changed_new.index)):
        for j in range(len(df_changed_new.columns)):
            if (df_changed_new.iloc[i, j] != df_changed_old.iloc[i, j]):
                df_info_changed.iloc[i, j] = str(df_changed_old.iloc[i, j]) + " ==> " + str(df_changed_new.iloc[i, j])
    result_name = str(new_xlsx).replace('.xlsx','').replace('new_','')+'_'+'result.xlsx'
    # 엑셀 저장
    with pd.ExcelWriter(result_name) as writer:
        df_info_changed.to_excel(writer, sheet_name='info changed', index=False)
        df_added.to_excel(writer, sheet_name='added', index=False)
        df_dropped.to_excel(writer, sheet_name='dropped', index=False)

def get_new_xlsx_list():
    path = "./"
    file_list = os.listdir(path)
    file_list_txt = [file for file in file_list if file.startswith("new_") and file.endswith(".xlsx")]
    return file_list_txt

def get_old_xlsx_list():
    path = "./"
    file_list = os.listdir(path)
    file_list_txt = [file for file in file_list if file.startswith("old_") and file.endswith(".xlsx")]
    return file_list_txt

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()


