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
import myutil

from lxml import html

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # test code starts
    str = u'\ub514\uc2a4\ud06c \ub610\ub294 \ub124\ud2b8\uc6cc\ud06c \uc624\ub958\uc785\ub2c8\ub2e4'
    #a, b, c, d = myutil.postprocess_name(u'디아(THE ā)')
    #a, b, c, d = myutil.postprocess_name(u'연세林(림)치과의원')
    a, b, c, d = myutil.postprocess_name(u' 정철어학원Jr.(주니어)용봉학원')
    a, b, c, d = myutil.postprocess_name(u'(양산점)벨칸토음악학원')

    #msbj, osbj = get_clinic_info('JDQ4MTg4MSM1MSMkMSMkMCMkOTkkMzgxMzUxIzIxIyQxIyQ1IyQ5OSQzNjEwMDIjNDEjJDEjJDgjJDgz')
    #a, b, c = myutil.pp_address(u'전라남도 나주시 내영산 1길 67')
    #a1, b1, c1 = myutil.pp_address(u'대전광역시 대덕구 대덕대로 1591-1 103~104호')
    #a2, b2, c2 = myutil.pp_address(u'경기도 가평군 설악면 유명로 2320')
    #b = myutil.pp_address_jibun(u'경기도 하남시 망월동 843-16')
    #c = myutil.pp_address_jibun(u'경기도 하남시 망월동 843-16 프라자')
    #d = myutil.pp_address_jibun(u'경기도 하남시 망월동 843번지 16호')
    # test code encs

    entity_dict = {}

    infilename = '';    outfilename = '';    encoding_option = '';   pp_option = ''
    mappers_type_cd = ''
    if len(sys.argv) == 1:
        Tkinter.Tk().withdraw()  # Close the root window

        opts = {}
        opts['filetypes'] = [('txt files', '.txt'), ('all files', '.*')]
        opts['initialfile'] = 'input.txt'
        opts['title'] = 'select input file'

        infilename = tkFileDialog.askopenfilename(**opts)
        if infilename == '': errExit('no input file')
        print infilename

        #opts['initialfile'] = 'output_clinic.txt'
        #opts['title'] = 'select output file'
        #outfilename = tkFileDialog.asksaveasfilename(**opts)
        outfilename = infilename + '_out.txt'
        print outfilename

    elif len(sys.argv) == 2:
        infilename = sys.argv[1]

        #opts['initialfile'] = 'output_clinic.txt'
        #opts['title'] = 'select output file'
        #outfilename = tkFileDialog.asksaveasfilename(**opts)
        outfilename = infilename + '_out.txt'
        print outfilename
    elif len(sys.argv) >= 3:
        infilename = sys.argv[1]
        outfilename = sys.argv[2]
        if len(sys.argv) >= 4:
            encoding_option = sys.argv[3].upper()
        if len(sys.argv) >= 5:
            pp_option = sys.argv[4]

        strtemp = ''
        idx = outfilename.rfind('\\')
        if idx != -1: strtemp = outfilename[idx+1:]
        else: strtemp = outfilename
        idx = strtemp.find('_')
        if idx != -1:
            mappers_type_cd = strtemp[:idx]

    try:
        #infile = open(infilename, 'r')
        infile = codecs.open(infilename, 'r', 'utf-8')
    except:
        errExit('invalid input file')

    if encoding_option == 'ANSI': outfile = open(outfilename, 'w')  # ansi
    else : outfile = codecs.open(outfilename, 'w', 'utf-8')    # utf-8

    #outfile.write('##NAME|SUBNAME|X|Y|MAPPERS_TYPE|TELNUM|NEWADDR|ADDR|FEAT1|FEAT2|AREA|DATE|ALTNAME|ETCNAME|ORGNAME|ETCADDR|PNUCODE\n')

    name_idx = -1;   subname_idx=-1;   xcoord_idx = -1;     ycoord_idx = -1;    mtype_idx = -1;     mcode_idx = -1;     pn_idx = -1
    newaddr_idx = -1;   addr_idx = -1;  feat1_idx = -1;     feat2_idx = -1;     area_idx = -1;      date_idx = -1
    altname_idx = -1;   etcname_idx = -1;   orgname_idx = -1;   etcaddr_idx = -1;   pnucode_idx = -1
    status_idx = -1
    info_len = -1

    source_info = ''    # 출처정보
    source_info2 = ''   # 상세출처정보    '@@낚시터_공공데이터포털'와 같은 경우 '공공데이터포털'이 상세출처정보

    while True:
        line = infile.readline()
        if not line: break;

        # convert ANSI to UTF-8
        #line = unicode(line, "cp949").encode("utf-8")
        line = line.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()

        idx = line.find('##')
        if line.startswith('##') or (idx != -1 and idx <= 2):
            source_info = ''
            line = line[idx+2:]
            idx = line.find('@@')
            if idx != -1:   # '@@낚시터_공공데이터포털'과 같이 기록된 출처정보 처리
                source_info = line[idx+2:]
                line = line[:idx]

                if encoding_option == 'ANSI': outfile.write('##NAME|SUBNAME|X|Y|MAPPERS_TYPE|TELNUM|NEWADDR|ADDR|FEAT1|FEAT2|AREA|DATE|ALTNAME|ETCNAME|ORGNAME|ETCADDR|PNUCODE|RD_JIBUN|MAPPERS_CD@@' + source_info.encode("cp949") + '\n')
                else: outfile.write('##NAME|SUBNAME|X|Y|MAPPERS_TYPE|TELNUM|NEWADDR|ADDR|FEAT1|FEAT2|AREA|DATE|ALTNAME|ETCNAME|ORGNAME|ETCADDR|PNUCODE|RD_JIBUN|MAPPERS_CD@@' + source_info + '\n')

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
                elif word_item == 'STATUS': status_idx = i

                if i >= 30: break

            continue

        word_list = line.split('|')
        if len(word_list) >= 30: pass
        elif len(word_list) < info_len:
            print(line)
            print('illegal data %d : %d' % (info_len, len(word_list)))
            continue      # 불량 데이터

        store_name = '';        store_subname = '';        store_xcoord = '';        store_ycoord = '';        store_mtype = '';        store_pn = ''
        store_newaddr = '';        store_addr = '';        store_feat1 = '';        store_feat2 = '';        store_area = '';        store_date = ''
        store_altname = '';        store_etcname = '';        store_orgname = '';        store_etcaddr = '';        store_pnucode = ''
        store_status = ''

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
        if status_idx != -1: store_status = word_list[status_idx].lstrip().rstrip()

        if store_status == u'폐업': continue
        elif store_name == u'사업장명': continue
        elif store_feat2 == u'일반야영장업': continue

          # 가끔 필드에 이상한 문자가 들어가 있어 cp949 인코딩 시에 문제 발생 ㅠㅠ '
        store_name = store_name.replace(u'\u0101', 'a').replace(u'\u9ba8', '').replace(u'\xe9', 'e').replace(u'\xe0', 'a')\
            .replace(u'\xc9', 'e').replace(u'\xea', 'e').replace(u'\xf4', 'o').replace(u'\xe7', 'c').replace(u'\xe8', 'e')\
            .replace(u'\u2013', ' ').replace(u'\u22c5', ' ').replace(u'\u2027', ' ').replace(u'\u30fb', ' ').replace(u'\uff65', ' ')\
            .replace(u'\u2024', ' ').replace(u'\u2219', ' ').replace('-', ' ')      # u'\u2013' = '-'
            # 鮨 = '\u9ba8', ā = '\u0101', '\xe9' = é, '\xc9' = É, '\xea' = ê

        store_name = store_name.replace(u'\u7f4e', '')  # ansi로 표현되지 않는 한자 ㅠㅠ
        store_name = store_name.replace('  ', ' ').replace('  ', ' ').lstrip().rstrip()
        #print(store_name)  # for debugging

        store_newaddr = store_newaddr.replace(u'\u30fb', '.').replace('', '').replace(u'\xa0', ' ').replace(u'\u24b6', ' ').replace( u'\u2219', '')\
            .replace( u'\ufffd', '').replace( u'\xf6', 'o').replace( u'\xfc', 'u').replace(u'\u200b', '')
        store_addr = store_addr.replace('', '').replace(u'\xa0', ' ').replace(u'\u24b6', ' ').replace( u'\u2219', '').replace( u'\ufffd', '')\
            .replace( u'\xf6', 'o').replace( u'\xfc', 'u')
        store_etcaddr = store_etcaddr.replace('', '').replace(u'\xa0', ' ').replace(u'\u24b6', ' ').replace( u'\u2219', '').replace( u'\ufffd', '')
        store_pn = store_pn.replace('', '').replace(u'\xa0', ' ').replace( u'\u2013', '').replace(u'\u200b', '').replace(u'\u202c', '').replace(u'\u2010', '-')

        if pp_option == 'ppname2':
            store_subname = ''
        elif pp_option == 'ppname3' and store_subname == '':
            idx = store_name.rfind('/')
            if idx != -1 and store_name.endswith('점'):
                store_subname = store_name[idx+1:]
                store_name = store_name[:idx]
        # 특정 소스별 예외 처리
        elif source_info == u'갤러리':
            if store_name.startswith('閉'): store_name = store_name[1:].lstrip();    store_feat1 = '(폐관)'
            elif store_name.startswith('休'): store_name = store_name[1:].lstrip();  store_feat1 = '(휴관)'
            elif store_name.startswith('移'):
                print('이사간 갤러리 : %s' % store_name);    continue
            elif store_name.startswith('統'):
                print('통합되어 없어진 갤러리 : %s' % store_name);     continue
        elif source_info == u'찜질방':
            store_addr = store_addr.replace('Jan-', '1-').replace('Feb-', '2-').replace('Mar-', '3-').replace('Apr-', '4-').replace('May-', '5-')\
                .replace('Jun-', '6-').replace('Jul-', '7-').replace('Aug-', '8-').replace('Sep-', '9-').replace('Oct-', '10-').replace('Nov-', '11-').replace('Dec-', '12-')\
                .replace('01월 01일', '1-1').replace('01월 03일', '1-3').replace('01월 15일', '1-15').replace('01월 20일', '1-20').replace('01월 24일', '1-24').replace('01월 26일', '1-26').replace('01월 31일', '1-31')\
                .replace('02월 06일', '2-6').replace('02월 09일', '2-9').replace('02월 10일', '2-10').replace('02월 23일', '2-23').replace('02월 26일', '2-26')\
                .replace('03월 01일', '3-1').replace('03월 02일', '3-2').replace('03월 15일', '3-15').replace('03월 31일', '3-31').replace('04월 17일', '4-17') \
                .replace('05월 01일', '5-1').replace('05월 27일', '5-27').replace('06월 01일', '6-1').replace('07월 13일', '7-13').replace('08월 22일', '8-22') \
                .replace('09월 15일', '9-15').replace('09월 23일', '9-23')\
                .replace('10월 03일', '10-3').replace('10월 16일', '10-16').replace('11월 01일', '11-1').replace('12월 13일', '12-13')
        elif source_info == u'동물병원':
            store_addr = myutil.pp_address_jibun(store_addr)

        if source_info == u'건강검진센터':
            store_orgname = store_name
            name, etcname = myutil.pp_hira_name(store_orgname)
            if name != store_name:
                store_name = name
                store_etcname = etcname
                #print('%s : %s : %s' % (store_name, name, store_orgname))

            name, subname, altname, etcname = myutil.postprocess_name(store_name)
            store_name = name
            if subname != '':
                store_subname = subname
                print('agency %s : %s' % (name, subname))
            if altname != '':
                store_altname = altname
                print('altname %s : %s : %s' % (store_name, name, altname))
            if etcname != '':
                store_etcname = etcname
                if store_etcname != '': store_etcname += ';'
                store_etcname += etcname
                print('etcname %s : %s : %s' % (store_name, name, etcname))

            store_feat1 = store_feat1.replace('[검진항목]', '').lstrip().rstrip().replace(' ', ';')
        elif pp_option =='ppname' or pp_option =='ppname2' or pp_option =='ppname3' or pp_option =='ppname4':
            store_orgname = store_name

            if pp_option == 'ppname4':
                name, etcname = myutil.pp_hira_name(store_orgname)
                if name != store_name:
                    store_name = name
                    store_etcname = etcname
                    print('%s : %s : %s' % (store_name, name, store_orgname))

            store_name, altname1 = myutil.postprocess_oldname(store_name)
            name, subname, altname2, etcname = myutil.postprocess_name(store_name)

            if subname == '' and etcname.endswith(u'호'):    # '1호', '2호'와 같은 이름들은 지점명으로 처리
                if etcname[:-1].isdigit(): subname = etcname;   etcname = ''

            store_name = name
            if subname != '':
                store_subname = subname
                print('agency %s : %s' % (name, subname))

            if altname1 != '':
                store_altname = altname1
                print('old altname %s : %s : %s' % (store_name, name, altname1))
            if altname2 != '':
                if store_altname != '': store_altname += ';'
                store_altname += altname2
                print('altname %s : %s : %s' % (store_name, name, altname2))

            if etcname != '':
                store_etcname = etcname
                if store_etcname != '': store_etcname += ';'
                store_etcname += etcname
                print('etcname %s : %s : %s' % (store_name, name, etcname))

            if store_name.find('(') != -1:  # for debugging
                print('complex name : %s ' % store_orgname)

        elif pp_option == '':
            if store_orgname == '':
                store_orgname = store_name
            store_name = myutil.simple_pp_name(store_name)

        if store_mtype == '' and source_info != '':
            store_mtype = source_info

        #if source_info == u'건강검진센터': store_mtype = u'건강검진센터'
        #elif source_info == u'보건소': store_mtype = u'보건소'
        #elif source_info == u'산후조리원': store_mtype = u'산후조리원'
        #elif source_info == u'동물병원': store_mtype = u'동물병원'

        # store_mtype 정보가 없으면 프랜차이즈 이름을 store_mtype 이름을 적용
        if store_mtype == '': store_mtype = store_name

        if store_orgname == '':
            store_orgname = store_name
            if store_subname != '': store_orgname += ' ' + store_subname

        if store_subname == '' and pp_option == '':
            name, subname, altname, etcname = myutil.postprocess_name(store_name)
            store_name = name
            store_subname = subname
            if altname != '':
                if store_altname != '': store_altname += ';'
                store_altname += altname
            if etcname != '':
                if store_etcname != '': store_etcname += ';'
                store_etcname += etcname

        if store_newaddr != '' and store_addr == '':
            road_addr, jibun_addr, etc_addr = myutil.pp_address(store_newaddr)
            store_newaddr = road_addr
            store_addr = jibun_addr
            if etc_addr != '':
                if store_etcaddr != '': store_etcaddr += ';'
                store_etcaddr += etc_addr
        elif store_newaddr == '' and store_addr != '':
            road_addr, jibun_addr, etc_addr = myutil.pp_address(store_addr)
            store_newaddr = road_addr
            store_addr = jibun_addr
            if etc_addr != '':
                if store_etcaddr != '': store_etcaddr += ';'
                store_etcaddr += etc_addr
        elif store_newaddr != '' and store_addr != '':
            road_addr, jibun_addr, etc_addr = myutil.pp_address(store_newaddr)
            store_newaddr = road_addr
            if etc_addr != '':
                if store_etcaddr != '': store_etcaddr += ';'
                store_etcaddr += etc_addr

            road_addr, jibun_addr, etc_addr = myutil.pp_address(store_addr)
            store_addr = jibun_addr
            if etc_addr != '':
                if store_etcaddr != '': store_etcaddr += ';'
                store_etcaddr += etc_addr

        store_name = store_name.lstrip().rstrip().replace(' ', '/').replace('/(', '(')
        #print(store_name)

        store_name = store_name.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
        #store_pn = store_pn.replace(')', '-')  # to do : 전화번호 정규화 모듈 작성하고 적용할 것!!

        # type 결정
        store_mtype = get_mappers_hotel_type(store_name, store_altname, store_feat1, store_feat2)
        #print(store_mtype)     # for debugging
        mappers_type_cd = ''

        if store_name == '' and store_subname == '': continue

        # 중복 체크
        entity_key = store_name + '|' + store_subname + '|' + store_pn + '|'
        if store_newaddr != '': entity_key += store_newaddr
        elif store_addr != '' : entity_key += store_addr
        elif store_xcoord != '' and store_ycoord != '': entity_key += store_xcoord + store_ycoord
        else: entity_key += 'NOADDRESS'

        if entity_dict.get(entity_key):
            entity_dict[entity_key] += 1
            print('중복(%d) %s' % (entity_dict[entity_key], entity_key))
            continue
        else: entity_dict[entity_key] = 1

        if encoding_option == 'ANSI':
            #print(store_name + store_subname)    # for debugging
            outfile.write('%s|' % store_name.encode("cp949"))
            outfile.write('%s|' % store_subname.encode("cp949"))
            outfile.write('%s|' % store_xcoord.encode("cp949"))
            outfile.write('%s|' % store_ycoord.encode("cp949"))
            outfile.write('%s|' % store_mtype.encode("cp949"))
            outfile.write('%s|' % store_pn.encode("cp949"))
            outfile.write('%s|' % store_newaddr.encode("cp949"))
            outfile.write('%s|' % store_addr.encode("cp949"))
            outfile.write('%s|' % store_feat1.encode("cp949"))
            outfile.write('%s|' % store_feat2.encode("cp949"))
            outfile.write('%s|' % store_area.encode("cp949"))
            outfile.write('%s|' % store_date.encode("cp949"))
            outfile.write('%s|' % store_altname.encode("cp949"))
            outfile.write('%s|' % store_etcname.encode("cp949"))
            outfile.write('%s|' % store_orgname.encode("cp949"))
            outfile.write('%s|' % store_etcaddr.encode("cp949"))
            outfile.write('%s|' % store_pnucode.encode("cp949"))
            outfile.write('|')  # RD_JIBUN
            outfile.write('%s' % mappers_type_cd.encode("cp949"))
            outfile.write('\n')
        else:
            outfile.write('%s|' % store_name)
            outfile.write('%s|' % store_subname)
            outfile.write('%s|' % store_xcoord)
            outfile.write('%s|' % store_ycoord)
            outfile.write('%s|' % store_mtype)
            outfile.write('%s|' % store_pn)
            outfile.write('%s|' % store_newaddr)
            outfile.write('%s|' % store_addr)
            outfile.write('%s|' % store_feat1)
            outfile.write('%s|' % store_feat2)
            outfile.write('%s|' % store_area)
            outfile.write('%s|' % store_date)
            outfile.write('%s|' % store_altname)
            outfile.write('%s|' % store_etcname)
            outfile.write('%s|' % store_orgname)
            outfile.write('%s|' % store_etcaddr)
            outfile.write('%s|' % store_pnucode)
            outfile.write('|')  # RD_JIBUN
            outfile.write('%s' % mappers_type_cd)
            outfile.write('\n')

    infile.close()
    outfile.close()


def get_mappers_hotel_type(src1, src2, type1, type2):
    name = src1.replace(' ', '').upper()
    altname = src2.replace(' ', '').upper()
    type1 = type1.replace(' ', '')
    type2 = type2.replace(' ', '')

    if name.find(u'게스트하우스') != -1 or name.find(u'GUESTHOUSE') != -1: return u'게스트하우스'
    elif altname.find(u'게스트하우스') != -1 or altname.find(u'GUESTHOUSE') != -1: return u'게스트하우스'
    elif name.find(u'고시텔') != -1 or name.find(u'고시원') != -1 or name.find(u'원룸텔') != -1: return u'고시원/원룸텔'
    elif altname.find(u'고시텔') != -1 or altname.find(u'고시원') != -1 or altname.find(u'원룸텔') != -1: return u'고시원/원룸텔'
    elif name.find(u'펜션') != -1 or name.find(u'팬션') != -1: return u'펜션(관광지)'
    elif altname.find(u'펜션') != -1 or altname.find(u'팬션') != -1: return u'펜션(관광지)'
    elif name.endswith(u'모텔') or altname.endswith(u'모텔') or altname.find(u'모텔;') != -1: return u'모텔'     # 모텔, 여관, 여인숙 순으로 점검
    elif name.startswith(u'모텔') or altname.startswith(u'모텔') or altname.find(u';모텔') != -1: return u'모텔'
    elif name.endswith(u'여관') or altname.endswith(u'여관') or altname.find(u'여관;') != -1:return u'여관'
    elif name.startswith(u'여관') or altname.startswith(u'여관') or altname.find(u';여관') != -1:return u'여관'
    elif name.endswith(u'산장') or altname.endswith(u'산장') or altname.find(u'산장;') != -1: return u'여인숙/민박/산장'
    elif name.startswith(u'산장') or altname.startswith(u'산장') or altname.find(u';산장') != -1: return u'여인숙/민박/산장'
    elif name.endswith(u'민박') or altname.endswith(u'민박') or altname.find(u'민박;') != -1:return u'여인숙/민박/산장'
    elif name.startswith(u'민박') or altname.startswith(u'민박') or altname.find(u';민박') != -1:return u'여인숙/민박/산장'
    elif name.endswith(u'여인숙') or altname.endswith(u'여인숙') or altname.find(u'여인숙;') != -1: return u'여인숙/민박/산장'
    elif name.startswith(u'여인숙') or altname.startswith(u'여인숙') or altname.find(u';여인숙') != -1: return u'여인숙/민박/산장'
    elif name.endswith(u'호스텔'):  return u'게스트하우스'

    if (name.endswith(u'호텔') or altname.endswith(u'호텔') or altname.find(u'호텔;') != -1) and type2.find(u'여관업') != -1: return u"모텔"
    elif (name.startswith(u'호텔') or altname.startswith(u'호텔') or altname.find(u';호텔') != -1) and type2.find(u'여관업') != -1: return u"모텔"
    elif type2.find(u'여관업') != -1: return u"여관"
    elif type2.find(u'여인숙업') != -1: return u"여인숙/민박/산장"
    elif type2.find(u'외국인관광도시민박업') != -1: return u"게스트하우스"
    elif type2.find(u'관광펜션업') != -1: return u"펜션(관광지)"
    elif type2.find(u'한옥체험업') != -1: return u"펜션(관광지)"

    if type2.find(u'숙박업(생활)') != -1: return u"펜션(관광지)"

    return u''

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
