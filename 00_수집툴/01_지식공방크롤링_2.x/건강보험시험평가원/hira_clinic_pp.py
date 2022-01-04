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

    a, b, c, d = myutil.postprocess_name(u'연세林(림)치과의원')
    #msbj, osbj = get_clinic_info('JDQ4MTg4MSM1MSMkMSMkMCMkOTkkMzgxMzUxIzIxIyQxIyQ1IyQ5OSQzNjEwMDIjNDEjJDEjJDgjJDgz')
    a, b, c = myutil.pp_address(u'경상남도 창원시 마산회원구 양덕동 38 (양덕동, 대한산업보건센터)')

    Tkinter.Tk().withdraw()  # Close the root window

    opts = {}
    opts['filetypes'] = [('txt files', '.txt'), ('all files', '.*')]
    opts['initialfile'] = 'input.txt'
    opts['title'] = 'select input file'

    infilename = tkFileDialog.askopenfilename(**opts)
    if infilename == '': errExit('no input file')
    #print infilename

    #infile = open(infilename, 'r')
    infile = codecs.open(infilename, 'r', 'utf-8')

    name_idx = 0;   newaddr_idx = 4;    type1_idx = 5;  type2_idx = 6;      key_idx = 7
    orgname_idx = 1;    etcname_idx = 2
    info_len = 8

    source_info = ''

    # 중복 제거
    key_dict = {}
    duplication_count = 0
    tempfile = codecs.open('tempfile.txt', 'w', 'utf-8')

    while True:
        line = infile.readline()
        if not line: break;

        # convert ANSI to UTF-8
        #line = unicode(line, "cp949").encode("utf-8")
        line = line.replace('\r', '').replace('\t', '').replace('\n', '')
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
                if word_item == 'KEY': key_idx = i

            tempfile.write('%s\n' % line)
            continue

        word_list = line.split('|')
        if len(word_list) < info_len: continue      # 불량 데이터

        word_key = ''
        if key_idx != -1:
            word_key = word_list[key_idx].lstrip().rstrip()

        if word_key == '':
            print('no key : %s' % line)
            tempfile.write('%s\n' % line)
        elif key_dict.get(word_key):
            duplication_count += 1
            print('%d duplication : %s' % (duplication_count, line))
        else:
            tempfile.write('%s\n' % line)
            key_dict[word_key] = 1

    tempfile.close()
    #errExit('merge completed!')

    opts['initialfile'] = 'output_clinic.txt'
    opts['title'] = 'select output file'
    outfilename = tkFileDialog.asksaveasfilename(**opts)
    if outfilename == '': errExit('no output file')
    #print outfilename

    infile = codecs.open('tempfile.txt', 'r', 'utf-8')
    #outfile = open(outfilename, 'w')
    outfile = codecs.open(outfilename, 'w', 'utf-8')

    #    0    1       2       3      4       5    6    7
    # '##NAME|ORGNAME|ETCNAME|TELNUM|NEWADDR|TYPE|FEAT|KEY@@일반병원'
    outfile.write('##NAME|ORGNAME|ETCNAME|TELNUM|NEWADDR|TYPE|FEAT|KEY|SUBNAME|ALTNAME|MTYPE@@HIRA\n')

    # post processing
    while True:
        line = infile.readline()
        if not line: break;

        # convert ANSI to UTF-8
        #line = unicode(line, "cp949").encode("utf-8")
        line = line.replace('\r', '').replace('\t', '').replace('\n', '')
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
                elif word_item == 'ORGNAME': orgname_idx = i
                elif word_item == 'ETCNAME': etcname_idx = i
                elif word_item == 'NEWADDR': newaddr_idx = i
                elif word_item == 'TYPE': type1_idx = i
                elif word_item == 'FEAT': type2_idx = i
                elif word_item == 'KEY': key_idx = i

            continue

        word_list = line.split('|')
        if len(word_list) < info_len: continue      # 불량 데이터

        store_name = word_list[name_idx].replace('/', ' ').lstrip().rstrip()
        store_orgname = word_list[orgname_idx].lstrip().rstrip()
        store_etcname = word_list[etcname_idx].lstrip().rstrip()

        name, etcname = myutil.pp_hira_name(store_orgname)
        if name != store_name:
            store_name = name
            store_etcname = etcname
            print('%s : %s : %s' % (store_name, name, store_orgname))

        name, subname, altname, etcname = myutil.postprocess_name(store_name)

        store_nm = name
        if subname != '':
            print('agency %s : %s' % (name, subname))
        if altname != '':
            print('altname %s : %s : %s' % (store_name, name, altname))
        if etcname != '':
            if store_etcname != '': store_etcname += ';'
            store_etcname += etcname
            print('etcname %s : %s : %s' % (store_name, name, etcname))

        word_list[name_idx] = store_nm.lstrip().rstrip().replace(' ', '/')
        word_list[etcname_idx] = store_etcname.lstrip().rstrip()

        store_cdnm = word_list[type2_idx].lstrip().rstrip().replace('?', '').replace('/', '')   # 노이즈 문자도 제거
        store_newaddr = word_list[newaddr_idx].lstrip().rstrip()
        store_key = word_list[key_idx].lstrip().rstrip()

        store_type2 = get_hospital_type(store_name, store_cdnm)
        if store_type2 == '의원':
            store_type2 = get_clinic_type(store_name)

        #if store_type2 == '': store_type2 = 'NONE'
        if store_type2 == '':
            print('%s : %s' % (store_orgname, store_cdnm))
            time.sleep(random.uniform(0.1, 0.2))
            msbj, osbj = get_clinic_info(store_key)
            if msbj != '':
                store_cdnm += ';'
                store_cdnm += msbj
            if osbj != '':
                store_cdnm += ';'
                store_cdnm += osbj
            word_list[type2_idx] = store_cdnm
            store_type2 = get_clinic_type_from_hiratype(msbj)

        word_list.append(subname)  # 지점명
        word_list.append(altname)  # 별칭
        word_list.append(store_type2)  # 상세유형정보

        for i in range(len(word_list)):
            if i != 0: outfile.write('|')
            outfile.write('%s' % word_list[i])

        outfile.write('\n')

    outfile.close()

def is_jibun(src):
    idx = src.find(',')
    if idx != -1: src = src[:idx]   # '203,2층' 이렇게 쓴 경우에 대비해서...

    if src.startswith('지하') or src.startswith('공중'): src = src[2:]
    elif src.startswith('산'): src = src[1:]

    if src.endswith('번지'): src = src[:-2]
    elif src.endswith('번') or src.endswith('호'): src = src[:-1]     # 번지를 101번, 101호 와 같이 기술한 경우도 있어서...

    src = src.replace('-', '')
    if src == '': return False
    elif src.isdigit(): return True
    else: return False


def get_hospital_type(store_nm, store_cdnm):
    if store_cdnm == '종합병원' or store_cdnm == '상급종합':
        if store_nm.find('대학') != -1: return '대학병원'
        else: return "종합병원"
    elif store_cdnm == '보건소' or store_cdnm == '보건지소' or store_cdnm == '보건진료소': return '보건소'
    elif store_cdnm == '요양병원': return '요양원'
    elif store_cdnm == '병원':  # to do : '전문병원'의 구분???
        if store_nm.find('여성') != -1: return '전문병원'
        elif store_nm.find('아동') != -1: return '전문병원'
        elif store_nm.find('전문') != -1: return '전문병원'
        elif store_nm.find('재활') != -1: return '전문병원'
        elif store_nm.find('어린이') != -1: return '전문병원'
        elif store_nm.find('키즈') != -1: return '전문병원'
        elif store_nm.find('미즈') != -1: return '전문병원'
        elif store_nm.find('아이들') != -1: return '전문병원'

        strtemp = get_clinic_type(store_nm)
        if strtemp == '': return '일반병원'
        else: return '전문병원'

    elif store_cdnm == '의원': return '의원'    # to do : 추가 분류 필요!!
    elif store_cdnm == '치과병원': return '전문병원'  # '치과' ???
    elif store_cdnm == '치과의원': return '치과'
    elif store_cdnm == '한방병원': return '대형한방병원'
    elif store_cdnm == '한의원': return '한의원'
    elif store_cdnm == '약국':  # to do : 추가 분류 필요!!
        if store_nm.endswith('한약국'):
            #if len(store_nm) <= 4:  return "일반약국"
            if store_nm.endswith('대한약국'): return "일반약국"
            elif store_nm.endswith('선한약국'): return "일반약국"
            elif store_nm.endswith('새한약국'): return "일반약국"
            elif store_nm.endswith('순한약국'): return "일반약국"
            elif store_nm.endswith('신한약국'): return "일반약국"
            elif store_nm.endswith('요한약국'): return "일반약국"
            elif store_nm.endswith('용한약국'): return "일반약국"
            elif store_nm.endswith('유한약국'): return "일반약국"
            elif store_nm.endswith('편한약국'):  return "일반약국"
            elif store_nm.endswith('착한약국'):  return "일반약국"
            elif store_nm.endswith('참한약국'):  return "일반약국"
            elif store_nm.endswith('친한약국'):  return "일반약국"
            elif store_nm.endswith('건강한약국'): return "일반약국"    # '노원건강한약국', '새건강한약국' ???
            elif store_nm.endswith('가득한약국'): return "일반약국"
            elif store_nm.endswith('가득한약국'): return "일반약국"
            elif store_nm.endswith('다정한약국'): return "일반약국"
            elif store_nm.endswith('든든한약국'): return "일반약국"
            elif store_nm.endswith('따뜻한약국'): return "일반약국"
            elif store_nm.endswith('상쾌한약국'): return "일반약국"
            elif store_nm.endswith('소중한약국'): return "일반약국"
            elif store_nm.endswith('수려한약국'): return "일반약국"
            elif store_nm.endswith('시원한약국'): return "일반약국"
            elif store_nm.endswith('신기한약국'): return "일반약국"
            elif store_nm.endswith('신통한약국'): return "일반약국"
            elif store_nm.endswith('신기한약국'): return "일반약국"
            elif store_nm.endswith('알뜰한약국'): return "일반약국"
            elif store_nm.endswith('온유한약국'): return "일반약국"
            elif store_nm.endswith('유명한약국'): return "일반약국"
            elif store_nm.endswith('유쾌한약국'): return "일반약국"
            elif store_nm.endswith('정직한약국'): return "일반약국"
            elif store_nm.endswith('튼튼한약국'): return "일반약국"
            elif store_nm.endswith('친절한약국'): return "일반약국"
            elif store_nm.endswith('편안한약국'): return "일반약국"
            elif store_nm.endswith('화목한약국'): return "일반약국"
            elif store_nm.endswith('화창한약국'): return "일반약국"
            elif store_nm.endswith('행복한약국'): return "일반약국"    # '경희행복한약국' ???
            elif store_nm.endswith('훈훈한약국'): return "일반약국"
            else: return '한약국/한약방'
        else: return '일반약국'
    else: return '기타'   # '지역의원->기타' 분류


def get_clinic_type(src):
    name = src.replace(' ', '').upper()

    if name.find('정형외과') != -1: return u'정형외과'
    elif name.find('성형외과') != -1: return u'성형외과'
    elif name.find('흉부외과') != -1: return u'외과/흉부외과/신경외과'
    elif name.find('신경외과') != -1 or name.find('신경과') != -1: return u'외과/흉부외과/신경외과'   # 신경과는 따로 분류를 만드는 것이 좋겠음
    elif name.find('정신건강의학과') != -1 or name.find('정신과') != -1: return u'정신과/신경정신과'
    elif name.find('피부과') != -1: return u'피부과'
    elif name.find('가정의학') != -1 or name.endswith('가정의원') or name.endswith('가정병원'): return u'가정의학과'
    elif name.find('재활의학') != -1: return u'재활의학과'
    elif name.find('방사선과') != -1: return u'방사선과'
    elif name.find('이비인후') != -1: return u'이비인후과'
    elif name.find('산부인과') != -1 or name.find('부인과') != -1 or name.endswith('여성의원') or name.endswith('여성병원'): return u'산부인과'
    elif name.find('소아과') != -1 or name.find('소아청소년과') != -1: return u'소아과'
    elif name.find('비뇨기') != -1 or name.find('비뇨의학과') != -1 or name.endswith('남성의원') or name.endswith('남성병원'): return u'비뇨기과'
    elif name.endswith('안과') or name.endswith('안과의원') or name.endswith('안과병원'): return u'안과'
    elif name.endswith('내과') or name.endswith('내과의원') or name.endswith('내과병원'): return u'내과'
    elif name.endswith('외과') or name.endswith('외과의원') or name.endswith('외과병원'): return u'외과/흉부외과/신경외과'
    elif name.find('마취통증의학과') != -1 or name.find('통증의학과') != -1  or name.find('마취과') != -1: return u'기타/마취과'
    elif name.find('영상의학과') != -1: return u'기타/영상의학과'

    return ''

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
    elif src == '소아청소년과': return 'u소아과'
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
    elif src == '핵의학과': return 'u기타/핵의학과'  # 분류 없음...
    elif src == '흉부외과': return u'외과/흉부외과/신경외과'

    return u'기타/일반의'

def get_clinic_info(clinic_key):
    url = 'https://www.hira.or.kr'
    #api = '/rd/hosp/hospAjax.do'           # 병원기본정보 (좌표정보 있으나, 세부진료 정보 없이 '일반의'라고만 표시된 경우 많음 ㅠㅠ
    api = '/rd/hosp/hospInfoAjax.do'    # 병원상세정보 (세부진료과 정보 있음), 진료시간 등등의 데이터는 다른 api에... (좌표정보 여기에도 있음)

    data = {
    }
    data['ykiho'] = clinic_key

    params = urllib.urlencode(data)
    #print(params)

    storeList = []

    try:
        #result = urllib.urlopen(url + api, params)
        urls = url + api + '?' + params;
        print(urls)     # for debugging
        result = urllib.urlopen(urls)
    except:
        print('Error calling the API');     return '', ''

    code = result.getcode()
    if code != 200:
        print('HTTP request error (status %d)' % code);     return '', ''

    response = result.read()
    if response.find('접속 오류') != -1 or response.find('<h3 class="error-title">') != -1:
        print('접속 오류')
        return '', ''
    #print(response)         # for debugging
    response_json = json.loads(response)

    if response_json.get('data') == None: return '', ''

    subject_list = response_json['data']['medicalSubjectList']      # medicalSubjectList2 도 있는데 medicalSubjectList 정보가 맞다고 판단됨

    main_subject = ''
    other_subjetcts = ''
    for i in range(len(subject_list)):
        if i == 0: main_subject = subject_list[i]['dgsbjtCdNm']
        else:
            if other_subjetcts != '': other_subjetcts += ';'
            other_subjetcts += subject_list[i]['dgsbjtCdNm']

    return main_subject, other_subjetcts


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
