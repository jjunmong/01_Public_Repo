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

mappers_code_dict = {
    u'대학병원': '30101',
    u'종합병원': '30102',
    u'전문병원': '30105',
    u'일반병원': '30106',
    u'치과': '30201',
    u'안과': '30202',
    u'피부과': '30203',
    u'소아과': '30204',
    u'산부인과': '30205',
    u'이비인후과': '30206',
    u'비뇨기과': '30207',
    u'내과': '30208',
    u'외과/흉부외과/신경외과': '30209',
    u'성형외과': '30210',
    u'정신과/신경정신과': '30211',
    u'가정의학과': '30212',
    u'재활의학과': '30213',
    u'정형외과': '30216',
    u'일반의원': '30217',
    u'요양원': '30218',
    u'방사선과': '30219',
    u'보건소': '30301',
    u'대형한방병원': '30402',
    u'한의원': '30403',
    u'일반약국': '30501',
    u'한약국/한약방': '30503',
    u'기타': '30200'   # ???
}

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    a, b, c, d = myutil.postprocess_name(u'연세林(림)치과의원')
    #msbj, osbj = get_clinic_info('JDQ4MTg4MSM1MSMkMSMkMCMkOTkkMzgxMzUxIzIxIyQxIyQ1IyQ5OSQzNjEwMDIjNDEjJDEjJDgjJDgz')
    a, b, c = myutil.pp_address(u'경상남도 창원시 마산회원구 양덕동 38 (양덕동, 대한산업보건센터)')

    Tkinter.Tk().withdraw()  # Close the root window

    opts = {}
    opts['filetypes'] = [('txt files', '.txt'), ('all files', '.*')]
    opts['initialfile'] = 'output_clinic.txt'
    opts['title'] = 'select input file'

    infilename = tkFileDialog.askopenfilename(**opts)
    if infilename == '': errExit('no input file')
    print infilename

    outfilestream_dict = {}
    for type_name in mappers_code_dict:
        type_code = mappers_code_dict[type_name]
        outfilename = type_code + '_' + type_name.replace('/', '') + '.txt'
        #outfilestream = codecs.open(outfilename, 'w', 'utf-8')  # uft-8
        outfilestream = codecs.open(outfilename, 'w')  # ansi
        outfilestream_dict[type_name] = outfilestream

    a = outfilestream_dict.get(u'가가가')
    b = outfilestream_dict.get(u'외과')
    c = outfilestream_dict.get(u'외과/흉부외과/신경외과')

    #opts['initialfile'] = 'output_clinic.txt'
    #opts['title'] = 'select output file'
    #outfilename = tkFileDialog.asksaveasfilename(**opts)
    #outfilename = infilename + '_out.txt'
    #print outfilename

    #infile = open(infilename, 'r')
    infile = codecs.open(infilename, 'r', 'utf-8')

    #outfile = open(outfilename, 'w')
    #outfile = codecs.open(outfilename, 'w', 'utf-8')
    #outfile.write('##NAME|SUBNAME|X|Y|MAPPERS_TYPE|TELNUM|NEWADDR|ADDR|FEAT1|FEAT2|AREA|DATE|ALTNAME|ETCNAME|ORGNAME|ETCADDR|PNUCODE\n')

    name_idx = -1;   subname_idx=-1;   xcoord_idx = -1;     ycoord_idx = -1;    mtype_idx = -1;     pn_idx = -1
    newaddr_idx = -1;   addr_idx = -1;  feat1_idx = -1;     feat2_idx = -1;     area_idx = -1;      date_idx = -1
    altname_idx = -1;   etcname_idx = -1;   orgname_idx = -1;   etcaddr_idx = -1;   pnucode_idx = -1
    info_len = -1

    source_info = ''

    while True:
        line = infile.readline()
        if not line: break;

        # convert ANSI to UTF-8
        #line = unicode(line, "cp949").encode("utf-8")
        line = line.replace('\r', '').replace('\t', '').replace('\n', '').lstrip().rstrip()
        #print(line)

        idx = line.find('##')
        if line.startswith('##') or (idx != -1 and idx <= 2):
            source_info = ''
            line = line[idx+2:]
            idx = line.find('@@')
            if idx != -1:
                source_info = line[idx+2:]
                line = line[:idx]

            word_list = line.split('|')
            info_len = len(word_list)

            for i in range(len(word_list)):
                word_item = word_list[i]
                if word_item == 'NAME': name_idx = i
                elif word_item == 'SUBNAME': subname_idx = i
                elif word_item == 'X': xcoord_idx = i
                elif word_item == 'Y': ycoord_idx = i
                elif word_item == 'MTYPE': mtype_idx = i
                elif word_item == 'TELNUM': pn_idx = i
                elif word_item == 'NEWADDR': newaddr_idx = i
                elif word_item == 'ADDR': addr_idx = i
                elif word_item == 'FEAT': feat1_idx = i
                elif word_item == 'FEAT2': feat2_idx = i
                elif word_item == 'AREA': area_idx = i
                elif word_item == 'DATE': date_idx = i
                elif word_item == 'ALTNAME': altname_idx = i
                elif word_item == 'ETCNAME': etcname_idx = i
                elif word_item == 'ORGNAME': orgname_idx = i
                elif word_item == 'ETCADDR': etcaddr_idx = i
                elif word_item == 'PNUCODE': pnucode_idx = i

            continue

        word_list = line.split('|')
        if len(word_list) < info_len: continue      # 불량 데이터

        store_name = '';        store_subname = '';        store_xcoord = '';        store_ycoord = '';        store_mtype = '';        store_pn = ''
        store_newaddr = '';        store_addr = '';        store_feat1 = '';        store_feat2 = '';        store_area = '';        store_date = ''
        store_altname = '';        store_etcname = '';        store_orgname = '';        store_etcaddr = '';        store_pnucode = ''

        if name_idx != -1: store_name = word_list[name_idx].replace('/', ' ').lstrip().rstrip()
        if subname_idx != -1: store_subname = word_list[subname_idx].lstrip().rstrip()
        if xcoord_idx != -1: store_xcoord = word_list[xcoord_idx].lstrip().rstrip()
        if ycoord_idx != -1: store_ycoord = word_list[ycoord_idx].lstrip().rstrip()
        if mtype_idx != -1: store_mtype = word_list[mtype_idx].lstrip().rstrip()
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

        if store_orgname == '':
            store_orgname = store_name
            if store_subname != '': store_orgname += ' ' + store_subname

        if store_subname == '':
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

        store_rdjibun = ''
        store_mtype_code = '30200'
        if mappers_code_dict.get(store_mtype):
            store_mtype_code = mappers_code_dict[store_mtype]
        #else: print(store_mtype)    # for debugging

        outfile = outfilestream_dict[u'기타']
        if outfilestream_dict.get(store_mtype) == None:
            strtemp = get_clinic_type_from_hiratype(store_mtype)
            if outfilestream_dict.get(strtemp) != None:
                #print('%s : %s' % (store_mtype, strtemp))
                outfile = outfilestream_dict[strtemp]
                store_mtype = strtemp
            elif store_mtype != strtemp:
                if not store_mtype.startswith(u'기타'): store_mtype = strtemp
        else: outfile = outfilestream_dict[store_mtype]

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
        outfile.write('%s|' % store_rdjibun.encode("cp949"))
        outfile.write('%s' % store_mtype_code.encode("cp949"))
        outfile.write('\n')

    for type_name in outfilestream_dict:
        outfilestream = outfilestream_dict[type_name]
        outfilestream.close()


def get_clinic_type_from_hiratype(src):    # hira type을 mappers type으로 변환
    if src == '가정의학과': return src
    elif src == '결핵과': return u'기타/결핵과'
    elif src == '내과': return src
    elif src == '마취통증의학과': return u'기타/마취과'  # 분류 없음...
    elif src == '방사선종양학과': return u'방사선과'
    elif src == '병리과': return u'기타/병리과'          # 분류 없음
    elif src == '비뇨기과': return src
    elif src == '비뇨의학과': return u'비뇨기과'
    elif src == '산부인과': return src
    elif src == '성형외과': return src
    elif src == '소아청소년과': return u'소아과'
    elif src == '신경과': return u'외과/흉부외과/신경외과'    # 분류 맞음??? 신경과는 신경내과로 따로 분류 만드는 것이 좋을 듯... 신경정신과도 아니고, 신경외과도 아님...
    elif src == '신경외과': return u'외과/흉부외과/신경외과'
    elif src == '안과': return src
    elif src == '영상의학과': return u'기타/영상의학과'  # 분류 없음...
    elif src == '예방의학과': return u'기타/예방의학과'  # 분류 없음...
    elif src == '외과': return u'외과/흉부외과/신경외과'
    elif src == '응급의학과': return u'기타/응급의학과'  # 분류 없음...
    elif src == '이비인후과': return src
    elif src == '재활의학과': return src
    elif src == '정신건강의학과': return u'정신과/신경정신과'
    elif src == '정형외과': return src
    elif src == '직업환경의학과': return u'기타/직업환경의학과'  # 분류 없음...
    elif src == '진단검사의학과': return u'기타/진단검사의학과'  # 분류 없음...
    elif src == '피부과': return src
    elif src == '핵의학과': return u'기타/핵의학과'  # 분류 없음...
    elif src == '흉부외과': return u'외과/흉부외과/신경외과'

    return u'기타/일반의'


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
