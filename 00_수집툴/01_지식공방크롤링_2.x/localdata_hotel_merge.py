# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import codecs
import urllib
import urllib2,cookielib
import json
import time
import random
import Tkinter
import tkFileDialog

from lxml import html

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    #a, b = split_newaddr('서울특별시 강남구 학동로97길 17, 1층 (청담동)')
    #a, b, c, d = postprocess_name('비알코리아(주)던킨도너츠비발디파크점')

    Tkinter.Tk().withdraw()  # Close the root window

    opts = {}
    opts['filetypes'] = [('txt files', '.txt'), ('all files', '.*')]
    opts['initialfile'] = 'input.txt'
    opts['title'] = 'select input file'

    infilename = tkFileDialog.askopenfilename(**opts)
    if infilename == '': errExit('no input file')
    #print infilename

    opts['initialfile'] = 'output_hotel_merged.txt'
    opts['title'] = 'select output file'
    outfilename = tkFileDialog.asksaveasfilename(**opts)
    if outfilename == '': errExit('no output file')
    #print outfilename

    infile = open(infilename, 'r')      # ANSI file open
    #infile = codecs.open(infilename, 'r', 'utf-8')
    #outfile = open(outfilename, 'w')
    outfile = codecs.open(outfilename, 'w', 'utf-8')

    #                0         1    2      3     4        5    6        7        8     9     10    11    12     13     14     15       16   17    18      19       20
    outfile.write('##NEWADDR|NAME|ENAME|TYPE|TELNUM|ADDR|STATUS|STATUS2|CAT1|CAT2|SIZE|TROOM|ROOM1|ROOM2|SINCE|CLOSED|YEAR|FEAT|BUSAGE|LUSAGE|LUSAGE2'
                  '|X|Y|ORGNAME|SUBNAME|ALTNAME|ETCNAME|ETCADDR|AZNAME|MAPPERSTYPE@@LOCALHOTEL\n')
    #                    23        24       25        26       27

    name_idx = 1;   ename_idx = 2;      newaddr_idx = 0;    addr_idx = 5;   pn_idx = 4
    type_idx = 3;   cat1_idx = 8;       cat2_idx = 9;       size_idx = 10
    troom_idx = 11; room1_idx = 12;     room2_idx = 13;     date_idx = 14
    orgname_idx = 23;   subname_idx = 24;       altname_idx = 25;       etcname_idx = 26;   etcaddr_idx = 27
    info_len = 28

    prev_list = None
    curr_list = None

    while True:
        line = infile.readline()
        if not line: break;

        # convert ANSI to UTF-8
        line = unicode(line, "cp949").encode("utf-8")
        line = line.replace('\r', '').replace('\t', '').replace('\n', '')
        #print(line)

        if line.startswith('##'):
            line = line[2:]
            idx = line.rfind('@@')
            if idx != -1: line = line[:idx]
            word_list = line.split('|')
            info_len = len(word_list)

            for i in range(len(word_list)):
                word_item = word_list[i]

                # '##NEWADDR|NAME|ENAME|TYPE|TELNUM|ADDR|STATUS|STATUS2|CAT1|CAT2|SIZE|TROOM|ROOM1|ROOM2|SINCE|CLOSED|YEAR|FEAT|BUSAGE|LUSAGE|LUSAGE2|X|Y|ORGNAME|SUBNAME|ALTNAME|ETCNAME|ETCADDR@@LOCALDATA
                if word_item == 'NAME': name_idx = i
                elif word_item == 'TELNUM': pn_idx = i
                elif word_item == 'NEWADDR': newaddr_idx = i
                elif word_item == 'ADDR': addr_idx = i
                elif word_item == 'TYPE': type_idx = i
                elif word_item == 'CAT1': cat1_idx = i
                elif word_item == 'CAT2': cat2_idx = i
                elif word_item == 'SIZE': size_idx = i
                elif word_item == 'SUBNAME': subname_idx = i
                elif word_item == 'ENAME': ename_idx = i
                elif word_item == 'TROOM': troom_idx = i
                elif word_item == 'ROOM1': room1_idx = i
                elif word_item == 'ROOM2': room2_idx = i
                elif word_item == 'SINCE': date_idx = i
                elif word_item == 'ORGNAME': orgname_idx = i
                elif word_item == 'ALTNAME': altname_idx = i
                elif word_item == 'ETCNAME': etcname_idx = i
                elif word_item == 'ETCADDR': etcaddr_idx = i

            word_list.append('AZNAME')
            prev_list = word_list

            continue

        curr_list = line.split('|')
        if len(curr_list) < info_len: continue      # 불량 데이터

        store_name = curr_list[name_idx].lstrip().rstrip()
        store_azname = store_name.replace(' ', '/')
        store_name = store_name.replace(' ', '')
        #curr_list[name_idx] = store_name
        curr_list.append(store_azname)

        store_pn = curr_list[pn_idx].lstrip().rstrip()
        store_type = curr_list[type_idx].lstrip().rstrip()
        store_cat1 = curr_list[cat1_idx].lstrip().rstrip()
        store_cat2 = curr_list[cat2_idx].lstrip().rstrip()
        store_newaddr = curr_list[newaddr_idx].lstrip().rstrip()
        store_addr = curr_list[addr_idx].lstrip().rstrip()
        store_size = curr_list[size_idx].lstrip().rstrip()

        store_ename = curr_list[ename_idx].lstrip().rstrip()
        store_troom = curr_list[troom_idx].lstrip().rstrip()
        store_room1 = curr_list[room1_idx].lstrip().rstrip()
        store_room2 = curr_list[room2_idx].lstrip().rstrip()
        store_date = curr_list[date_idx].lstrip().rstrip()
        store_altname = curr_list[altname_idx].lstrip().rstrip()
        store_etcname = curr_list[etcname_idx].lstrip().rstrip()
        store_etcaddr = curr_list[etcaddr_idx].lstrip().rstrip()

        # 앞의 POI와 동일여부 체크 (주소가 같고, 이름이 같거나, 전화번호가 같으면...) <= 전화번호 비교하면 본의 아니게 호텔, 콘도가 같이 묶이는 경우 발생 ㅠㅠ (쏠비치호텔, 콘도가 그 예...)
        if (is_same_hotel_name(curr_list[name_idx], prev_list[name_idx]) or is_same_phone_num(curr_list[pn_idx], prev_list[pn_idx]))\
                and curr_list[newaddr_idx] == prev_list[newaddr_idx]:

            if curr_list[orgname_idx] != prev_list[orgname_idx]:
                if prev_list[date_idx] < curr_list[date_idx]:
                    prev_list[orgname_idx] = curr_list[orgname_idx]

            if curr_list[ename_idx] != prev_list[ename_idx]:
                if prev_list[ename_idx] != '':
                    if prev_list[altname_idx] != '': prev_list[altname_idx] += ';'
                    prev_list[altname_idx] += prev_list[ename_idx]

                if prev_list[date_idx] < curr_list[date_idx]:
                    if curr_list[ename_idx] != '':
                        prev_list[ename_idx] = curr_list[ename_idx]
                    elif not is_same_hotel_name(curr_list[name_idx], prev_list[name_idx]):
                        prev_list[ename_idx] = ''

            if curr_list[etcname_idx] != prev_list[etcname_idx]:
                if prev_list[date_idx] < curr_list[date_idx]:
                    prev_list[etcname_idx] = curr_list[etcname_idx]

            if curr_list[etcaddr_idx] != prev_list[etcaddr_idx]:
                if is_same_hotel_name(curr_list[name_idx], prev_list[name_idx]):    # 이름이 같으면 etcaddr 정보 더함
                    if curr_list[etcaddr_idx] != '':
                        if prev_list[etcaddr_idx] != '': prev_list[etcaddr_idx] += ';'
                        prev_list[etcaddr_idx] += curr_list[etcaddr_idx]
                elif prev_list[date_idx] < curr_list[date_idx]:
                    prev_list[etcaddr_idx] = curr_list[etcaddr_idx]

            if curr_list[type_idx] != prev_list[type_idx]:
                if curr_list[type_idx] != '':
                    if prev_list[type_idx] != '': prev_list[type_idx] += ';'
                    prev_list[type_idx] += curr_list[type_idx]

            if curr_list[cat1_idx] != prev_list[cat1_idx]:
                if curr_list[cat1_idx] != '':
                    if prev_list[cat1_idx] != '': prev_list[cat1_idx] += ';'
                    prev_list[cat1_idx] += curr_list[cat1_idx]

            if curr_list[cat2_idx] != prev_list[cat2_idx]:
                if curr_list[cat2_idx] != '':
                    if prev_list[cat2_idx] != '': prev_list[cat2_idx] += ';'
                    prev_list[cat2_idx] += curr_list[cat2_idx]

            if curr_list[troom_idx] != prev_list[troom_idx]:
                if curr_list[troom_idx] != '':
                    if prev_list[date_idx] < curr_list[date_idx]:
                        prev_list[troom_idx] = curr_list[troom_idx]

            if curr_list[room1_idx] != prev_list[room1_idx]:
                if prev_list[type_idx] == '관광숙박업':
                    prev_list[room1_idx] = curr_list[room1_idx]
                elif curr_list[type_idx] != '관광숙박업':
                    if prev_list[date_idx] < curr_list[date_idx]:
                        if curr_list[room1_idx] == '':
                            if not is_same_hotel_name(curr_list[name_idx], prev_list[name_idx]):
                                prev_list[room1_idx] = curr_list[room1_idx]
                        else:
                            prev_list[room1_idx] = curr_list[room1_idx]
                    elif prev_list[room1_idx] == '':
                        if curr_list[room1_idx] != '':
                            if is_same_hotel_name(curr_list[name_idx], prev_list[name_idx]):
                                prev_list[room1_idx] = curr_list[room1_idx]

            if curr_list[room2_idx] != prev_list[room2_idx]:
                if prev_list[type_idx] == '관광숙박업':
                    prev_list[room2_idx] = curr_list[room2_idx]
                elif curr_list[type_idx] != '관광숙박업':
                    if prev_list[date_idx] < curr_list[date_idx]:
                        if curr_list[room2_idx] == '':
                            if not is_same_hotel_name(curr_list[name_idx], prev_list[name_idx]):
                                prev_list[room2_idx] = curr_list[room2_idx]
                        else:
                            prev_list[room2_idx] = curr_list[room2_idx]
                    elif prev_list[room2_idx] == '':
                        if curr_list[room2_idx] != '':
                            if is_same_hotel_name(curr_list[name_idx], prev_list[name_idx]):
                                prev_list[room2_idx] = curr_list[room2_idx]

            if curr_list[size_idx] != prev_list[size_idx]:
                if curr_list[size_idx] != '':
                    if prev_list[size_idx] != '': prev_list[size_idx] += ';'
                    prev_list[size_idx] += curr_list[size_idx]

            if not is_same_phone_num(curr_list[pn_idx], prev_list[pn_idx]):
                if curr_list[pn_idx] != '':
                    if prev_list[pn_idx] != '' and curr_list[pn_idx].find(prev_list[pn_idx]) != -1:    # '610-7000,033-610-7000' 이런 경우가 있어서...
                        prev_list[pn_idx] = curr_list[pn_idx]
                    else:
                        if prev_list[pn_idx] != '': prev_list[pn_idx] += ';'
                        prev_list[pn_idx] += curr_list[pn_idx]

            if curr_list[altname_idx] != prev_list[altname_idx]:
                if curr_list[altname_idx] != '':
                    if prev_list[altname_idx] != '': prev_list[altname_idx] += ';'
                    prev_list[altname_idx] += curr_list[altname_idx]

            if curr_list[subname_idx] != prev_list[subname_idx]:
                if is_same_hotel_name(curr_list[name_idx], prev_list[name_idx]):
                    if curr_list[subname_idx] != '':
                        if prev_list[altname_idx] != '': prev_list[altname_idx] += ';'
                        prev_list[altname_idx] += curr_list[name_idx] + ' ' + curr_list[subname_idx]
                    if prev_list[subname_idx] != '':
                        if prev_list[altname_idx] != '': prev_list[altname_idx] += ';'
                        prev_list[altname_idx] += prev_list[name_idx] + ' ' + prev_list[subname_idx]

                    prev_list[subname_idx] = ''
                    prev_list[etcname_idx] = ''
                    #prev_list[etcaddr_idx] = ''
                else:
                    if prev_list[date_idx] < curr_list[date_idx]:
                        if prev_list[date_idx] < curr_list[date_idx]:
                            if prev_list[subname_idx] != '':
                                if prev_list[altname_idx] != '': prev_list[altname_idx] += ';'
                                prev_list[altname_idx] += prev_list[name_idx] + ' ' + prev_list[subname_idx]   # 이 경우 'prev_list 값이 'prev_list의 이름+지점명' 정보를 별칭으로 기록
                        else:
                            if curr_list[subname_idx] != '':
                                if prev_list[altname_idx] != '': prev_list[altname_idx] += ';'
                                prev_list[altname_idx] += curr_list[name_idx] + ' ' + curr_list[subname_idx]

                        prev_list[subname_idx] = curr_list[subname_idx]   # 최신 정보를 우선적으로 적용
                    else:
                        if curr_list[subname_idx] != '':
                            if prev_list[altname_idx] != '': prev_list[altname_idx] += ';'
                            prev_list[altname_idx] += curr_list[name_idx] + ' ' + curr_list[subname_idx]

                #if curr_list[subname_idx] != '':      # SUBNAME 비교 (표현력 좋은 이름을 사용)
                #    if len(prev_list[subname_idx]) < len(curr_list[subname_idx]):
                #        prev_list[subname_idx] = curr_list[subname_idx]

            if curr_list[info_len] != prev_list[info_len]:      # AZNAME 비교
                if prev_list[date_idx] < curr_list[date_idx]:
                    prev_list[info_len] = curr_list[info_len]   # 최신 정보를 우선적으로 적용
                #if curr_list[info_len] != '':
                #    if len(prev_list[info_len]) < len(curr_list[info_len]):
                #        prev_list[info_len] = curr_list[info_len]

            if curr_list[name_idx] != prev_list[name_idx]:      # 최신 정보 우선 적용
                # 이름이 다르면 별칭으로 추가
                if curr_list[name_idx].replace(' ', '') != prev_list[name_idx].replace(' ', ''):
                    if prev_list[altname_idx] != '': prev_list[altname_idx] += ';'

                    if prev_list[date_idx] < curr_list[date_idx]: prev_list[altname_idx] += prev_list[name_idx]     # 이 경우 'prev_list[name_idx]'이 없어지므로 'prev_list[name_idx]'를 별칭으로 기록
                    else: prev_list[altname_idx] += curr_list[name_idx]

                if prev_list[date_idx] < curr_list[date_idx]:
                    prev_list[name_idx] = curr_list[name_idx]
                    prev_list[date_idx] = curr_list[date_idx]   # 새로 개업했다고 생각하고, 개업일자 변경 (날짜 덮어쓰는 로직을 제일 뒤에 둬야 함... 당연히 날짜 비교를 모두 한 뒤에 위치해야 함...)

                #if (prev_list[subname_idx] != '' and curr_list[subname_idx] != '') or (prev_list[subname_idx] == '' and curr_list[subname_idx] == ''):
                #    if len(prev_list[name_idx]) < len(curr_list[name_idx]):
                #        prev_list[name_idx] = curr_list[name_idx]
                #elif prev_list[subname_idx] != '':;
                #elif curr_list[subname_idx] != '':
                #    prev_list[name_idx] = curr_list[name_idx]
        else:
            if prev_list[type_idx] != '관광숙박업':      # '관광숙박업'만 남은 경우는 인쇄하지 않음 (이 경우는 쓰레기 데이터임...)
                if prev_list[ename_idx] != '':      # 영어이름 정보도 별칭 정보에 추가
                    if prev_list[altname_idx] != '': prev_list[altname_idx] += ';'
                    prev_list[altname_idx] += prev_list[ename_idx]

                final_size_info = prev_list[size_idx] + '/'
                troom_info = prev_list[troom_idx]
                if troom_info != '': final_size_info += troom_info
                else:
                    room_count = 0
                    room1_info = prev_list[room1_idx];  room2_info = prev_list[room2_idx]
                    if room1_info.isdigit(): room_count += int(room1_info)
                    if room2_info.isdigit(): room_count += int(room2_info)

                    if room_count != 0:
                        final_size_info += str(room_count)

                prev_list[size_idx] = final_size_info

                for i in range(len(prev_list)):

                    if i != 0: outfile.write('|')
                    outfile.write('%s' % prev_list[i])

                mappers_hotel_type = get_mappers_hotel_type(prev_list[name_idx], prev_list[altname_idx], prev_list[type_idx], prev_list[cat2_idx])
                outfile.write('|%s\n' % mappers_hotel_type)

            prev_list = curr_list

    # for loop 종료 후에 남아 있는 마지막 항목 인쇄... (위의 코드와 동일한 코드 반복...)
    if prev_list[type_idx] != '관광숙박업':  # '관광숙박업'만 남은 경우는 인쇄하지 않음 (이 경우는 쓰레기 데이터임...)
        if prev_list[ename_idx] != '':  # 영어이름 정보도 별칭 정보에 추가
            if prev_list[altname_idx] != '': prev_list[altname_idx] += ';'
            prev_list[altname_idx] += prev_list[ename_idx]

        final_size_info = prev_list[size_idx] + '/'
        troom_info = prev_list[troom_idx]
        if troom_info != '':
            final_size_info += troom_info
        else:
            room_count = 0
            room1_info = prev_list[room1_idx];
            room2_info = prev_list[room2_idx]
            if room1_info.isdigit(): room_count += int(room1_info)
            if room2_info.isdigit(): room_count += int(room2_info)

            if room_count != 0:
                final_size_info += str(room_count)

        prev_list[size_idx] = final_size_info

        for i in range(len(prev_list)):

            if i != 0: outfile.write('|')
            outfile.write('%s' % prev_list[i])

        mappers_hotel_type = get_mappers_hotel_type(prev_list[name_idx], prev_list[altname_idx], prev_list[type_idx], '')
        outfile.write('|%s\n' % mappers_hotel_type)

    outfile.close()


def is_same_hotel_name(src1, src2):
    name1 = src1.replace(' ', '')
    name2 = src2.replace(' ', '')
    if name1 == name2: return True
    elif name1.find(name2) == 0: return True
    elif name2.find(name1) == 0: return True

    return False

def is_same_phone_num(src1, src2):
    pn1 = src1.replace('-', '')
    pn2 = src2.replace('-', '')
    if pn1 == '' or pn2 == '': return False
    elif pn1 == pn2: return True
    else: return False

def get_mappers_hotel_type(src1, src2, type1, type2):
    name = src1.replace(' ', '').upper()
    altname = src2.replace(' ', '').upper()

    if name.find('게스트하우스') != -1 or name.find('GUESTHOUSE') != -1: return '게스트하우스'
    elif altname.find('게스트하우스') != -1 or altname.find('GUESTHOUSE') != -1: return '게스트하우스'
    elif name.find('고시텔') != -1 or name.find('고시원') != -1 or name.find('원룸텔') != -1: return '고시원/원룸텔'
    elif altname.find('고시텔') != -1 or altname.find('고시원') != -1 or altname.find('원룸텔') != -1: return '고시원/원룸텔'
    elif name.find('펜션') != -1 or name.find('팬션') != -1: return '펜션(관광지)'
    elif altname.find('펜션') != -1 or altname.find('팬션') != -1: return '펜션(관광지)'
    elif name.endswith('모텔') or altname.endswith('모텔') or altname.find('모텔;') != -1: return '모텔'     # 모텔, 여관, 여인숙 순으로 점검
    elif name.startswith('모텔') or altname.startswith('모텔') or altname.find(';모텔') != -1: return '모텔'
    elif name.endswith('여관') or altname.endswith('여관') or altname.find('여관;') != -1:return '여관'
    elif name.startswith('여관') or altname.startswith('여관') or altname.find(';여관') != -1:return '여관'
    elif name.endswith('산장') or altname.endswith('산장') or altname.find('산장;') != -1: return '여인숙/민박/산장'
    elif name.startswith('산장') or altname.startswith('산장') or altname.find(';산장') != -1: return '여인숙/민박/산장'
    elif name.endswith('민박') or altname.endswith('민박') or altname.find('민박;') != -1:return '여인숙/민박/산장'
    elif name.startswith('민박') or altname.startswith('민박') or altname.find(';민박') != -1:return '여인숙/민박/산장'
    elif name.endswith('여인숙') or altname.endswith('여인숙') or altname.find('여인숙;') != -1: return '여인숙/민박/산장'
    elif name.startswith('여인숙') or altname.startswith('여인숙') or altname.find(';여인숙') != -1: return '여인숙/민박/산장'

    if (name.endswith('호텔') or altname.endswith('호텔') or altname.find('호텔;') != -1) and type1.find('여관업') != -1: return "모텔"
    elif (name.startswith('호텔') or altname.startswith('호텔') or altname.find(';호텔') != -1) and type1.find('여관업') != -1: return "모텔"
    elif type1.find('여관업') != -1: return "여관"
    elif type1.find('여인숙업') != -1: return "여인숙/민박/산장"
    elif type1.find('외국인관광도시민박업') != -1: return "게스트하우스"
    elif type1.find('관광펜션업') != -1: return "펜션(관광지)"

    if type2.find('숙박업(생활)') != -1: return "펜션(관광지)"

    return ''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
