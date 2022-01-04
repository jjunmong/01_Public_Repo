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
    a, b, c, d = myutil.postprocess_name(u'디아(THE ā)')
    a, b, c, d = myutil.postprocess_name(u'연세林(림)치과의원')
    #msbj, osbj = get_clinic_info('JDQ4MTg4MSM1MSMkMSMkMCMkOTkkMzgxMzUxIzIxIyQxIyQ1IyQ5OSQzNjEwMDIjNDEjJDEjJDgjJDgz')
    a, b, c = myutil.pp_address(u'전라남도 나주시 내영산 1길 67')
    # test code ends

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


    #infile = open(infilename, 'r')
    infile = codecs.open(infilename, 'r', 'utf-8')

    if encoding_option == 'ANSI': outfile = open(outfilename, 'w')  # ansi
    else : outfile = codecs.open(outfilename, 'w', 'utf-8')    # utf-8

    #outfile.write('##NAME|SUBNAME|X|Y|MAPPERS_TYPE|TELNUM|NEWADDR|ADDR|FEAT1|FEAT2|AREA|DATE|ALTNAME|ETCNAME|ORGNAME|ETCADDR|PNUCODE\n')

    name_idx = -1;   subname_idx=-1;   xcoord_idx = -1;     ycoord_idx = -1;    mtype_idx = -1;     mcode_idx = -1;     pn_idx = -1
    newaddr_idx = -1;   addr_idx = -1;  feat1_idx = -1;     feat2_idx = -1;     area_idx = -1;      date_idx = -1
    altname_idx = -1;   etcname_idx = -1;   orgname_idx = -1;   etcaddr_idx = -1;   pnucode_idx = -1
    subj1_idx = -1;     subj2_idx = -1;     subj3_idx = -1;     subj4_idx = -1;     size_idx = -1;  id_idx = -1
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

                outfile.write('##NAME|SUBNAME|X|Y|MAPPERS_TYPE|TELNUM|NEWADDR|ADDR|FEAT1|FEAT2|AREA|DATE|ALTNAME|ETCNAME|ORGNAME|ETCADDR|PNUCODE|RD_JIBUN|MAPPERS_CD@@' + source_info.encode("cp949") + '\n')

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
                elif word_item == 'X' or word_item == 'XCOORD': xcoord_idx = i
                elif word_item == 'Y' or word_item == 'YCOORD': ycoord_idx = i
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
                elif word_item == 'SUBJ1': subj1_idx = i
                elif word_item == 'SUBJ2': subj2_idx = i
                elif word_item == 'SUBJ3': subj3_idx = i
                elif word_item == 'SUBJ4': subj4_idx = i
                elif word_item == 'SIZE': size_idx = i
                elif word_item == 'ID': id_idx = i

            continue

        word_list = line.split('|')
        if len(word_list) < info_len:
            print(line)
            print('illegal data %d : %d' % (info_len, len(word_list)))
            continue      # 불량 데이터

        store_name = '';        store_subname = '';        store_xcoord = '';        store_ycoord = '';        store_mtype = '';        store_pn = ''
        store_newaddr = '';        store_addr = '';        store_feat1 = '';        store_feat2 = '';        store_area = '';        store_date = ''
        store_altname = '';        store_etcname = '';        store_orgname = '';        store_etcaddr = '';        store_pnucode = ''
        store_subj1 = '';       store_subj2 = '';       store_subj3 = '';       store_subj4 = '';       store_size = '';    store_id = ''

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

        if subj1_idx != -1: store_subj1 = word_list[subj1_idx].lstrip().rstrip()
        if subj2_idx != -1: store_subj2 = word_list[subj2_idx].lstrip().rstrip()
        if subj3_idx != -1: store_subj3 = word_list[subj3_idx].lstrip().rstrip()
        if subj4_idx != -1: store_subj4 = word_list[subj4_idx].lstrip().rstrip()
        if size_idx != -1: store_size = word_list[size_idx].lstrip().rstrip()
        if id_idx != -1: store_id = word_list[id_idx].lstrip().rstrip()

        # 가끔 필드에 이상한 문자가 들어가 있어 cp949 인코딩 시에 문제 발생 ㅠㅠ '
        store_name = store_name.replace(u'\u0101', 'a').replace(u'\u9ba8', '').replace(u'\xe9', 'e').replace(u'\xe0', 'a')\
            .replace(u'\xc9', 'e').replace(u'\xea', 'e').replace(u'\xf4', 'o').replace(u'\xe7', 'c').replace(u'\xe8', 'e').replace('･', ' ')\
            .replace(u'\u2013', ' ').replace( u'\u2022', ' ').replace(u'\u22c5', ' ').replace(u'\u2027', ' ').replace(u'\u30fb', ' ').replace(u'\u2024', ' ') \
            .replace(u'\u207a', ' ').replace(u'\u7075', ' ').replace('-', ' ')        # u'\u2013' = '-'
            # 鮨 = '\u9ba8', ā = '\u0101', '\xe9' = é, '\xc9' = É, '\xea' = ê
        store_name = store_name.replace(u'\u7f4e', '').lstrip().rstrip()  # ansi로 표현되지 않는 한자 ㅠㅠ
        #print(store_name)  # for debugging

        store_newaddr = store_newaddr.replace(u'\u30fb', '.').replace('', '').replace(u'\xa0', '').replace( u'\u2219', '').replace( u'\ufffd', '').replace( u'\u2022', ',')
        store_addr = store_addr.replace('', '').replace(u'\xa0', '').replace( u'\u2219', '').replace( u'\ufffd', '')
        store_etcaddr = store_etcaddr.replace('', '').replace(u'\xa0', '').replace( u'\u2219', '').replace( u'\ufffd', '')
        store_pn = store_pn.replace('', '').replace(u'\xa0', '').replace( u'\u2013', '').replace(u'\u200b', '').replace(u'\u202c', '')

        if pp_option == 'ppname2':
            store_subname = ''
        elif pp_option == 'ppname3' and store_subname == '':
            idx = store_name.rfind('/')
            if idx != -1 and store_name.endswith('점'):
                store_subname = store_name[idx+1:]
                store_name = store_name[:idx]

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
        elif pp_option =='ppname' or pp_option =='ppname2' or pp_option =='ppname3':
            store_orgname = store_name

            store_name, altname1 = myutil.postprocess_oldname(store_name)
            name, subname, altname2, etcname = myutil.postprocess_name(store_name)

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

            if False:
            #if store_name.find('(') != -1:  # test code
                print('complex name : %s' % store_orgname)
                name2, subname2, altname2, etcname2 = myutil.postprocess_name(store_name)
                if altname2 != '':
                    if store_altname != '': store_altname += ';'
                    store_altname += altname2
                    if store_subname != '':
                        store_altname += ' ' + store_subname

                    store_name = name2
                    print('altname2 %s : %s : %s' % (store_name, store_orgname, altname2))

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
        #if store_mtype == '': store_mtype = store_name

        # store_mtype, mappers_type_cd 정하기
        store_mtype, mappers_type_cd = get_private_academy_type(store_name, store_feat2, store_subj1, store_subj2, store_subj3, store_subj4, store_size)

        # 분류코드 정보 기록
        store_feat2 += ';' + store_subj1 + ';' + store_subj2 + ';' + store_subj4
        store_feat2 = store_feat2.replace(u'\u30fb', '')    # ansi로 인쇄되지 않는 문자 제거
        # 선생님 수 정보 기록
        store_feat1 = store_size

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

        if store_name == '' and store_subname == '': continue
        if store_name == '학원명' or store_name == '교습소명': continue

        # 중복 체크
        entity_key = ''
        if store_id != '': entity_key = store_name + '|' + store_id
        else: entity_key = store_name + '|' + store_pn  + '|' + store_newaddr

        if entity_dict.get(entity_key):
            entity_dict[entity_key] += 1
            #print('중복(%d) %s' % (entity_dict[entity_key], entity_key))
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

def get_private_academy_type(academy_name, academy_type, store_subj1, store_subj2, store_subj3, store_subj4, store_size):
    if store_size == '': store_size = '0'
    mtype = '일반학원';     mcode = '20315'

    if academy_name.endswith('컴퓨터학원'): return u'컴퓨터학원', '20310'
    elif academy_name.endswith('컴퓨터아트학원'): return u'컴퓨터학원', '20310'
    elif academy_name.startswith('케이지아이티뱅크'): return u'컴퓨터학원', '20310'
    #elif academy_name.endswith('종합학원'): return u'종합학원', '20318'     # 분류 추가로 만들었음

    if store_subj4 == u'독서실': return u'독서실', '20317'
    elif store_subj4 == u'외국어': return u'외국어학원', '20305'
    elif store_subj4 == u'국제': return u'외국어학원', '20305'
    elif store_subj4 == u'컴퓨터': return u'컴퓨터학원', '20310'
    elif store_subj2 == u'컴퓨터(소)': return u'컴퓨터학원', '20310'
    elif store_subj2 == u'음악' or store_subj2 == u'미술' or store_subj2 == u'국악': return u'음악/미술학원', '20309'
    elif store_subj2.find(u'음악') != -1 or store_subj2.find(u'미술') != -1: return u'음악/미술학원', '20309'
    elif store_subj2 == u'성인고시': return u'국가고시학원', '20308'
    elif (store_subj2 == u'보습' or store_subj2 == u'입시') and int(store_size) >= 50: return u'대형입시학원', '20302'
    elif store_subj2 == u'마술(매직)': return u'취미학원', '20313'
    elif store_subj2 == u'무용': return u'취미학원', '20313'  # ???
    elif store_subj2.startswith(u'연기('): return u'취미학원', '20313'    # ???
    elif store_subj2.startswith(u'공예('): return u'취미학원', '20313'
    elif store_subj2 == u'댄스': return u'스포츠학원', '20312'
    elif store_subj1 == u'직업기술':
        if int(store_size) >= 50: return u'대형직업학교', '20301'
        else: return u'전문자격학원', '20307'     # '직업기술학원'이 더 좋을 듯...
    # '보습학원' 분류 있어야 할 듯...

    return mtype, mcode

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
