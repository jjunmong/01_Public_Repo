import codecs
from datetime import datetime
import traceback
import os, sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\04_1_고캠핑\\') == False : os.makedirs('수집결과\\04_1_고캠핑\\')
outfilename = '수집결과\\04_1_고캠핑\\고캠핑_{}.txt'.format(today)
outfilename_true = '수집결과\\04_1_고캠핑\\고캠핑_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\04_1_고캠핑\\고캠핑_{}.log_실패.txt'.format(today)

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
    outfile.write("NAME|ADDR|TELL|CATE|WEATHER|DATE\n")


def dup_remove():
    outfilename_dupRemove = '수집결과\\04_1_고캠핑\\23_고캠핑_중복제거.txt'
    w = open(outfilename_dupRemove, 'w')
    r = open(outfilename, 'r',encoding='UTF8')
    # 파일에서 읽은 라인들을 리스트로 읽어들임
    lines = r.readlines()
    # Set에 넣어서 중복 제거 후 다시 리스트 변환
    lines = list(set(lines))
    # 리스트 정렬
    # 정렬,중복제거한 리스트 파일 쓰기
    w.write("NAME|ADDR|TELL|CATE|WEATHER|DATE\n")
    for line in lines:
        w.write(line)
    # 파일 닫기
    w.close()
    r.close()
    os.remove(outfilename)
    os.rename(outfilename_dupRemove, outfilename)


file_move()