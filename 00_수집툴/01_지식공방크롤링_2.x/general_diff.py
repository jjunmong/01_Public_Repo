# -*- coding: utf-8 -*-

'''
Created on 10 Oct 2018

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
import myutil

from lxml import html

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # test code starts
    # test code encs

    entity_dict = {}
    entity_dict2 = {}

    infilename1 = '';   infilename2 = '';    outfilename = '';    encoding_option = 'ANSI';   pp_option = ''

    if len(sys.argv) == 1:
        Tkinter.Tk().withdraw()  # Close the root window

        opts = {}
        opts['filetypes'] = [('txt files', '.txt'), ('all files', '.*')]
        opts['initialfile'] = 'input.txt'
        opts['title'] = 'select input file'

        infilename1 = tkFileDialog.askopenfilename(**opts)
        if infilename1 == '': errExit('no input file')
        print infilename1

        infilename2 = ''
        idx = infilename1.rfind('/')
        if idx != -1:
            infilename2 = infilename1[:idx] + '/baseline' + infilename1[idx:]
        else:
            infilename2 = tkFileDialog.askopenfilename(**opts)

        if infilename2 == '': errExit('no input file')
        print infilename2

        outfilename = infilename1.replace('.txt', '') + '_diff.txt'
        print outfilename

    elif len(sys.argv) == 2:
        infilename1 = sys.argv[1]

        infilename2 = ''
        idx = infilename1.rfind('/')
        if idx != -1:
            infilename2 = infilename1[:idx] + '/baseline' + infilename1[idx:]
        else:
            infilename2 = 'baseline\\' + infilename1
            #infilename2 = tkFileDialog.askopenfilename(**opts)

        if infilename2 == '': errExit('no input file')
        print infilename2

        outfilename = infilename1.replace('.txt', '') + '_diff.txt'
        print outfilename
    elif len(sys.argv) >= 3:
        infilename = sys.argv[1]
        infilename2 = sys.argv[2]


        if len(sys.argv) >= 4: outfilename = sys.argv[3]
        else: outfilename = infilename1.replace('.txt', '') + '_diff.txt'

    # 기존 데이터 읽기
    infile = open(infilename2, 'r')

    outfile = None
    if encoding_option == 'ANSI': outfile = open(outfilename, 'w')  # ansi
    else : outfile = codecs.open(outfilename, 'w', 'utf-8')    # utf-8

    # default index 값
    name_idx = 0;   subname_idx = 1;   xcoord_idx = 2;     ycoord_idx = 3;    mtype_idx = 4;     mcode_idx = -1;     pn_idx = 5
    newaddr_idx = 6;   addr_idx = 7;  feat1_idx = 8;     feat2_idx = 9;     area_idx = 10;      date_idx = 11
    altname_idx = 12;   etcname_idx = 13;   orgname_idx = 14;   etcaddr_idx = 15;   pnucode_idx = 16
    info_len = 17

    source_info = ''    # 출처정보
    source_info2 = ''   # 상세출처정보    '@@낚시터_공공데이터포털'와 같은 경우 '공공데이터포털'이 상세출처정보

    while True:
        orgline = infile.readline()
        if not orgline: break;
        orgline = orgline.replace('\n', '')

        # convert ANSI to UTF-8
        line = unicode(orgline, "cp949").encode("utf-8")
        line = line.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()

        idx = line.find('##')
        if line.startswith('##') or (idx != -1 and idx <= 2):
            source_info = ''
            line = line[idx+2:]
            idx = line.find('@@')
            if idx != -1:   # '@@낚시터_공공데이터포털'과 같이 기록된 출처정보 처리
                source_info = line[idx+2:]
                line = line[:idx]

                #if encoding_option == 'ANSI': outfile.write('##NAME|SUBNAME|X|Y|MAPPERS_TYPE|TELNUM|NEWADDR|ADDR|FEAT1|FEAT2|AREA|DATE|ALTNAME|ETCNAME|ORGNAME|ETCADDR|PNUCODE|RD_JIBUN|MAPPERS_CD|EDIT@@' + source_info.encode("cp949") + '\n')
                #else: outfile.write('##NAME|SUBNAME|X|Y|MAPPERS_TYPE|TELNUM|NEWADDR|ADDR|FEAT1|FEAT2|AREA|DATE|ALTNAME|ETCNAME|ORGNAME|ETCADDR|PNUCODE|RD_JIBUN|MAPPERS_CD|EDIT@@' + source_info + '\n')

                idx = source_info.find('_')
                if idx != -1:
                    source_info2 = source_info[idx+1:]
                    source_info = source_info[:idx]

            word_list = line.split('|')
            info_len = len(word_list)

            for i in range(len(word_list)):
                word_item = word_list[i]
                if word_item == 'NAME': name_idx = i
                elif word_item == 'SUBNAME': subname_idx = i
                elif word_item == 'X' or word_item == 'XCOORD' or word_item =='KATECX': xcoord_idx = i
                elif word_item == 'Y' or word_item == 'YCOORD' or word_item =='KATECY': ycoord_idx = i
                elif word_item == 'MTYPE' or word_item == 'MAPPERSTYPE': mtype_idx = i
                elif word_item == 'MAPPERS_CD' or word_item == 'MAPPERSCD': mcode_idx = i
                elif word_item == 'TELNUM': pn_idx = i
                elif word_item == 'NEWADDR': newaddr_idx = i
                elif word_item == 'ADDR': addr_idx = i
                elif word_item == 'FEAT': feat1_idx = i
                elif word_item == 'FEAT2' or word_item == 'TYPE' or word_item == 'TYPE1': feat2_idx = i
                elif word_item == 'AREA': area_idx = i
                elif word_item == 'DATE': date_idx = i
                elif word_item == 'ALTNAME': altname_idx = i
                elif word_item == 'ETCNAME': etcname_idx = i
                elif word_item == 'ORGNAME': orgname_idx = i
                elif word_item == 'ETCADDR': etcaddr_idx = i
                elif word_item == 'PNUCODE': pnucode_idx = i

            continue

        word_list = line.split('|')
        if len(word_list) < info_len:
            print(line)
            print('illegal data %d : %d' % (info_len, len(word_list)))
            continue      # 불량 데이터

        store_name = '';        store_subname = '';        store_xcoord = '';        store_ycoord = '';        store_mtype = '';        store_pn = ''
        store_newaddr = '';        store_addr = '';        store_feat1 = '';        store_feat2 = '';        store_area = '';        store_date = ''
        store_altname = '';        store_etcname = '';        store_orgname = '';        store_etcaddr = '';        store_pnucode = ''

        if name_idx != -1: store_name = word_list[name_idx].replace('/', ' ').lstrip().rstrip()
        if subname_idx != -1: store_subname = word_list[subname_idx].lstrip().rstrip()
        if xcoord_idx != -1: store_xcoord = word_list[xcoord_idx].lstrip().rstrip()
        if ycoord_idx != -1: store_ycoord = word_list[ycoord_idx].lstrip().rstrip()
        if mtype_idx != -1: store_mtype = word_list[mtype_idx].lstrip().rstrip()
        if mcode_idx != -1: mappers_type_cd = word_list[mcode_idx].lstrip().rstrip()
        if pn_idx != -1: store_pn = word_list[pn_idx].lstrip().rstrip()
        if newaddr_idx != -1: store_newaddr = word_list[newaddr_idx].lstrip().rstrip()
        if addr_idx != -1: store_addr = word_list[addr_idx].lstrip().rstrip()
        if feat1_idx != -1: store_feat1 = word_list[feat1_idx].lstrip().rstrip()
        if feat2_idx != -1: store_feat2 = word_list[feat2_idx].lstrip().rstrip()
        if area_idx != -1: store_area = word_list[area_idx].lstrip().rstrip()
        if date_idx != -1: store_date = word_list[date_idx].lstrip().rstrip()
        if altname_idx != -1: store_altname = word_list[altname_idx].lstrip().rstrip()
        if etcname_idx != -1: store_etcname = word_list[etcname_idx].lstrip().rstrip()
        if orgname_idx != -1: store_orgname = word_list[orgname_idx].lstrip().rstrip()
        if etcaddr_idx != -1: store_etcaddr = word_list[etcaddr_idx].lstrip().rstrip()
        if pnucode_idx != -1: store_pnucode = word_list[pnucode_idx].lstrip().rstrip()


        if store_name == '' and store_subname == '': continue

        #print(store_name)   # for debugging

        # 중복 체크
        entity_key = store_name + '|' + store_subname + '|' + store_pn + '|'
        if store_newaddr != '': entity_key += store_newaddr
        elif store_addr != '' : entity_key += store_addr
        elif store_xcoord != '' and store_ycoord != '': entity_key += store_xcoord + store_ycoord
        else: entity_key += 'NOADDRESS'

        entity_key2 = store_name + '|' + store_subname + '|' + '' + '|'     # 전화번호 제외
        if store_newaddr != '': entity_key2 += store_newaddr
        elif store_addr != '' : entity_key2 += store_addr
        elif store_xcoord != '' and store_ycoord != '': entity_key2 += store_xcoord + store_ycoord
        else: entity_key2 += 'NOADDRESS'

        entity_key = entity_key.replace('"', '').lstrip().rstrip()      # delete white noise characters
        entity_key2 = entity_key2.replace('"', '').lstrip().rstrip()    # delete white noise characters

        if entity_dict.get(entity_key2):
            if encoding_option == 'ANSI':
                tempvalue = entity_dict[entity_key2]
                utf8value = unicode(tempvalue, "cp949").encode("utf-8")
                #print('duplication(%s) %s' % (utf8value, entity_key))
                print(u'duplication %s' % entity_key)
            else: print('duplication(%s) %s' % (entity_dict[entity_key2], entity_key))
            continue
        else: entity_dict[entity_key2] = orgline

        #if entity_dict2.get(entity_key2):
        #    print('중복2(%d) %s' % (entity_dict2[entity_key2], entity_key2))
        #    continue
        #else: entity_dict2[entity_key2] = orgline

    infile.close()
    print('previous data loaded!')

    # 신규 데이터 읽기
    infile = open(infilename1, 'r')
    line_count = 0
    while True:
        orgline = infile.readline()
        if not orgline: break;
        orgline = orgline.replace('\n', '')

        # convert ANSI to UTF-8
        line = unicode(orgline, "cp949").encode("utf-8")
        line = line.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
        line_count += 1

        idx = line.find('##')
        if line.startswith('##') or (idx != -1 and idx <= 2):
            source_info = ''
            line = line[idx+2:]
            idx = line.find('@@')
            if idx != -1:   # '@@낚시터_공공데이터포털'과 같이 기록된 출처정보 처리
                source_info = line[idx+2:]
                line = line[:idx]

                #if encoding_option == 'ANSI': outfile.write('##NAME|SUBNAME|X|Y|MAPPERS_TYPE|TELNUM|NEWADDR|ADDR|FEAT1|FEAT2|AREA|DATE|ALTNAME|ETCNAME|ORGNAME|ETCADDR|PNUCODE|RD_JIBUN|MAPPERS_CD@@' + source_info.encode("cp949") + '\n')
                #else: outfile.write('##NAME|SUBNAME|X|Y|MAPPERS_TYPE|TELNUM|NEWADDR|ADDR|FEAT1|FEAT2|AREA|DATE|ALTNAME|ETCNAME|ORGNAME|ETCADDR|PNUCODE|RD_JIBUN|MAPPERS_CD@@' + source_info + '\n')

                idx = source_info.find('_')
                if idx != -1:
                    source_info2 = source_info[idx+1:]
                    source_info = source_info[:idx]

            word_list = line.split('|')
            info_len = len(word_list)

            for i in range(len(word_list)):
                word_item = word_list[i]
                if word_item == 'NAME': name_idx = i
                elif word_item == 'SUBNAME': subname_idx = i
                elif word_item == 'X' or word_item == 'XCOORD' or word_item =='KATECX': xcoord_idx = i
                elif word_item == 'Y' or word_item == 'YCOORD' or word_item =='KATECY': ycoord_idx = i
                elif word_item == 'MTYPE' or word_item == 'MAPPERSTYPE': mtype_idx = i
                elif word_item == 'MAPPERS_CD' or word_item == 'MAPPERSCD': mcode_idx = i
                elif word_item == 'TELNUM': pn_idx = i
                elif word_item == 'NEWADDR': newaddr_idx = i
                elif word_item == 'ADDR': addr_idx = i
                elif word_item == 'FEAT': feat1_idx = i
                elif word_item == 'FEAT2' or word_item == 'TYPE' or word_item == 'TYPE1': feat2_idx = i
                elif word_item == 'AREA': area_idx = i
                elif word_item == 'DATE': date_idx = i
                elif word_item == 'ALTNAME': altname_idx = i
                elif word_item == 'ETCNAME': etcname_idx = i
                elif word_item == 'ORGNAME': orgname_idx = i
                elif word_item == 'ETCADDR': etcaddr_idx = i
                elif word_item == 'PNUCODE': pnucode_idx = i

            continue

        word_list = line.split('|')
        if len(word_list) < info_len:
            print('line count = %d (%s)' % (line_count, line))
            print('illegal data %d : %d' % (info_len, len(word_list)))
            continue      # 불량 데이터

        store_name = '';        store_subname = '';        store_xcoord = '';        store_ycoord = '';        store_mtype = '';        store_pn = ''
        store_newaddr = '';        store_addr = '';        store_feat1 = '';        store_feat2 = '';        store_area = '';        store_date = ''
        store_altname = '';        store_etcname = '';        store_orgname = '';        store_etcaddr = '';        store_pnucode = ''

        if name_idx != -1: store_name = word_list[name_idx].replace('/', ' ').lstrip().rstrip()
        if subname_idx != -1: store_subname = word_list[subname_idx].lstrip().rstrip()
        if xcoord_idx != -1: store_xcoord = word_list[xcoord_idx].lstrip().rstrip()
        if ycoord_idx != -1: store_ycoord = word_list[ycoord_idx].lstrip().rstrip()
        if mtype_idx != -1: store_mtype = word_list[mtype_idx].lstrip().rstrip()
        if mcode_idx != -1: mappers_type_cd = word_list[mcode_idx].lstrip().rstrip()
        if pn_idx != -1: store_pn = word_list[pn_idx].lstrip().rstrip()
        if newaddr_idx != -1: store_newaddr = word_list[newaddr_idx].lstrip().rstrip()
        if addr_idx != -1: store_addr = word_list[addr_idx].lstrip().rstrip()
        if feat1_idx != -1: store_feat1 = word_list[feat1_idx].lstrip().rstrip()
        if feat2_idx != -1: store_feat2 = word_list[feat2_idx].lstrip().rstrip()
        if area_idx != -1: store_area = word_list[area_idx].lstrip().rstrip()
        if date_idx != -1: store_date = word_list[date_idx].lstrip().rstrip()
        if altname_idx != -1: store_altname = word_list[altname_idx].lstrip().rstrip()
        if etcname_idx != -1: store_etcname = word_list[etcname_idx].lstrip().rstrip()
        if orgname_idx != -1: store_orgname = word_list[orgname_idx].lstrip().rstrip()
        if etcaddr_idx != -1: store_etcaddr = word_list[etcaddr_idx].lstrip().rstrip()
        if pnucode_idx != -1: store_pnucode = word_list[pnucode_idx].lstrip().rstrip()

        if store_name == '' and store_subname == '': continue

        # 중복 체크
        entity_key = store_name + '|' + store_subname + '|' + store_pn + '|'
        if store_newaddr != '': entity_key += store_newaddr
        elif store_addr != '' : entity_key += store_addr
        elif store_xcoord != '' and store_ycoord != '': entity_key += store_xcoord + store_ycoord
        else: entity_key += 'NOADDRESS'

        entity_key2 = store_name + '|' + store_subname + '|' + '' + '|'     # 전화번호 제외
        if store_newaddr != '': entity_key2 += store_newaddr
        elif store_addr != '' : entity_key2 += store_addr
        elif store_xcoord != '' and store_ycoord != '': entity_key2 += store_xcoord + store_ycoord
        else: entity_key2 += 'NOADDRESS'

        entity_key = entity_key.replace('"', '').lstrip().rstrip()      # delete white noise characters
        entity_key2 = entity_key2.replace('"', '').lstrip().rstrip()    # delete white noise characters

        if entity_dict.get(entity_key2):
            if entity_dict[entity_key2] != orgline:
                diff_info = get_diff_info(entity_dict[entity_key2], orgline, 'NAME|SUBNAME|X|Y|MAPPERS_TYPE|TELNUM|NEWADDR|ADDR|FEAT1|FEAT2|AREA|DATE|ALTNAME|ETCNAME|ORGNAME|ETCADDR|PNUCODE|RD_JIBUN|MAPPERS_CD')
                if diff_info != '':
                    outfile.write('%s|UPDATE(%s)\n' % (orgline, diff_info))

            del entity_dict[entity_key2]
            continue
        else:
            outfile.write('%s|ADD\n' % orgline)

    infile.close()

    for key in entity_dict:
        outfile.write('%s|DELETE\n' % entity_dict[key])

    outfile.close()
    print('finished!')


def get_diff_info(src1, src2, refsrc):
    result = ''

    list1 = src1.replace('\n', '').split('|')
    list2 = src2.replace('\n', '').split('|')
    ref_list = refsrc.split('|')

    for i in range(len(list1)):
        if i >= len(list2): break   # for safety

        if list1[i] != list2[i]:
            if result != '': result += '|'
            if i < len(ref_list): result += ref_list[i]     # _postprocessed.txt 파일은 뒤에 임의로 추가한 데이터가 있어서 이 체크를 해야 함!!

    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
