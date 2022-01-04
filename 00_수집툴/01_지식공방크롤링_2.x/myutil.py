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
import hanja
from hanja import hangul


from lxml import html

def simple_pp_name(org_name):
    strtemp = org_name.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('/(', '(').replace(' (', '(')
    strtemp = strtemp.replace(', ', ' ').replace('. ', ' ').replace('· ', ' ').replace('「', ' ').replace('」', ' ').replace(';', ' ').replace('  ', ' ').replace('  ', ' ') \
        .replace('ㆍ', '/').replace('·', '/').replace('＆', '&').replace('[', '(').replace(']', ')') \
        .replace('<', '(').replace('>', ')').replace(',', '/').replace('( ', '(').replace(' )', ')').replace('& ', '&').replace(' &', '&') \
        .replace('`', '\'').replace('’', '\'').lstrip().rstrip()

    # 맨 앞, 맨 뒤의 (주) 처리
    if strtemp.startswith('주)'):
        strtemp = strtemp[2:].lstrip()
    elif strtemp.startswith('(주)'):
        strtemp = strtemp[3:].lstrip()
    elif strtemp.endswith('(주)'):
        strtemp = strtemp[:-3].rstrip()

    strtemp = strtemp.replace('(주)', '').replace('㈜', '').replace('(유)', '').replace('(재)', '').replace('(사)', ' ') \
        .replace('(자)', '').replace('(합)', '').replace('( ', '(').replace(' )', ')').lstrip().rstrip()

    return strtemp

def postprocess_oldname(org_name):
    pp_name = ''
    alt_name = ''

    idx = org_name.find('(구)')
    if idx > 0:
        pp_name = org_name[:idx].rstrip()
        alt_name = org_name[idx+3:].lstrip()
        return pp_name, alt_name

    idx = org_name.find('((구 ')     # '고운달작은도서관((구 신월1동 도서방))' 이와 같은 경우도 있어서... ㅠㅠ
    if idx != -1 and org_name.endswith('))'):
        pp_name = org_name[:idx].rstrip()
        alt_name = org_name[idx+4:-2].lstrip().rstrip()
        return pp_name, alt_name

    idx = org_name.find('(구 ')
    if idx != -1 and org_name.endswith(')'):
        pp_name = org_name[:idx].rstrip()
        alt_name = org_name[idx+3:-1].lstrip().rstrip()
        return pp_name, alt_name

    idx = org_name.find('(구,')
    if idx != -1 and org_name.endswith(')'):
        pp_name = org_name[:idx].rstrip()
        alt_name = org_name[idx+3:-1].lstrip().rstrip()
        return pp_name, alt_name

    idx = org_name.find('(구.')
    if idx != -1 and org_name.endswith(')'):
        pp_name = org_name[:idx].rstrip()
        alt_name = org_name[idx+3:-1].lstrip().rstrip()
        return pp_name, alt_name

    idx = org_name.find('(전 ')      # '스카디아(전 퀸스케어텔)'와 같은 이름 처리
    if idx != -1 and org_name.endswith(')'):
        pp_name = org_name[:idx].rstrip()
        alt_name = org_name[idx+3:-1].lstrip().rstrip()
        return pp_name, alt_name


    return org_name, ''

def postprocess_name(org_name):
    strtemp = org_name.replace('\'s', '|s').replace('\'S', '|s').replace('\'스', '|스').replace('\'', ' ').replace('|s', '\'s').replace('|스', '\'스')    # 's, '스 의 경우를 제외한 나머지 ' 문자 제거
    strtemp = strtemp.replace(', ', ' ').replace('. ', ' ').replace('· ', ' ').replace('「', ' ').replace('」', ' ').replace(';', ' ').replace('  ', ' ').replace('  ', ' ') \
        .replace('ㆍ', '/').replace('·', '/').replace('＆', '&').replace('[', '(').replace(']', ')') \
        .replace('<', '(').replace('>', ')').replace(',', '/').replace('( ', '(').replace(' )', ')').replace('& ', '&').replace(' &', '&') \
        .replace('`', '\'').replace('’', '\'').lstrip().rstrip()

    # 부동산 데이터 처리 (임시 코드)
    #strtemp = strtemp.replace('(합동)', '').replace('(단지)', '').replace('(단지내)', '').replace('(단지입구)', '').rstrip().lstrip()

    # '((', '))' 처리 <= 괄호가 이중으로 있는 경우 중 일부 처리
    idx = strtemp.find('((')
    if idx != -1:
        strtemp = strtemp[:idx] + strtemp[idx+1:]
        idx = strtemp.rfind(')')
        if idx != -1: strtemp = strtemp[:idx] + strtemp[idx + 1:]

    idx = strtemp.find('))')
    if idx != -1:
        strtemp = strtemp[:idx] + strtemp[idx+1:]
        idx = strtemp.find('(')
        if idx != -1: strtemp = strtemp[:idx] + strtemp[idx + 1:]

    pp_name = ''
    pp_subname = ''
    etc_name = ''
    alt_name = ''

    # 맨 앞, 맨 뒤의 (주) 처리
    if strtemp.startswith('주)'): strtemp = strtemp[2:].lstrip()
    elif strtemp.startswith('(주)'): strtemp = strtemp[3:].lstrip()
    elif strtemp.startswith('주식회사'): strtemp = strtemp[4:].lstrip()
    elif strtemp.endswith('(주)'): strtemp = strtemp[:-3].rstrip()
    elif strtemp.endswith('주식회사'): strtemp = strtemp[:-4].rstrip()

    strtemp = strtemp.replace('주식회사', '(주)')
    idx = strtemp.find('(주)')
    if idx > 0:
        idx2 = strtemp.find('휴게소')
        if idx2 > idx: # '서창산업(주)옥계(속초방향)휴게소'의 패턴 처리 <= (주) 앞의 부분 버림
            etc_name = strtemp[:idx].rstrip()
            #strtemp = strtemp[idx+len('(주)'):].lstrip()
            strtemp = strtemp[idx+3:].lstrip()
            if etc_name.startswith('('): etc_name = etc_name[1:].lstrip()   # '(농업회사법인이음(주))철정휴게소' 이런 경우가 있어서...
            if strtemp.startswith(')'): strtemp = strtemp[1:].lstrip()      # '(농업회사법인이음(주))철정휴게소' 이런 경우가 있어서...
        elif strtemp.endswith('시스템'):      # '갓포삿뽀로 앤 구이랩 트리플스트리트점(주)엔타스시스템' 이런 이름들 처리...
            etc_name = strtemp[idx+3:].lstrip()
            strtemp = strtemp[:idx].rstrip()
        else:
            str_tail = strtemp[idx+3:].lstrip()
            if str_tail == '엔타스' or str_tail == '사가르':      # 기타 회사 이름들 예외 처리...
                etc_name = strtemp[idx + 3:].lstrip()
                strtemp = strtemp[:idx].rstrip()
            else:
                strtemp = strtemp.replace('(주)', ' ')

    strtemp = strtemp.replace('㈜', ' ').replace('(유)', ' ').replace('유한회사', '').replace('(사)', ' ') \
        .replace('(재)', '').replace('(자)', '').replace('(합)', '').replace('( ', '(').replace(' )', ')').lstrip().rstrip()

    # 기타 처리곤란 단어들 처리
    strtemp = strtemp.replace('앤(&)', '&').replace('카페(cafe)', '카페 ').replace('스토리(story)', '스토리 ').replace('푸드(food)', '푸드 ').lstrip().rstrip()
    # 나중에 처리할 수도 있음 ㅎㅎㅎ (brand 사전으로 처리 가능하도록 고쳐둠 ㅎㅎㅎ)
    strtemp = strtemp.replace('지에스리테일지에스', 'GS').replace('지에스리테일 지에스', 'GS').replace('지에스리테일GS', 'GS').replace('지에스리테일 GS', 'GS')
    strtemp = strtemp.replace('씨제이푸드빌빕스', 'VIPS').replace('씨제이푸드빌 빕스', 'VIPS').replace('커피빈코리아', '커피빈').replace('오구(59)쌀피자', '오구쌀피자')\
        .replace('59(오구)쌀피자', '오구쌀피자')
    strtemp = strtemp.replace('롯데쇼핑 롯데슈퍼', '롯데슈퍼').replace('인(人)삼(三)', '인삼(人三)').replace('고(Go)', 'Go ')

    idx = strtemp.find('(')
    if idx != -1:
        idx2 = strtemp.find(')')
        if idx2 > idx:
            str_head = strtemp[:idx].rstrip()
            str_mid = strtemp[idx+1:idx2].lstrip().rstrip()
            str_tail = strtemp[idx2+1:].lstrip()

            if str_head == '' and str_mid.endswith('점') and str_tail != '':     # '(노원하계점)/하남돼지집'과 같은 경우 처리
                str_head = str_tail
                str_tail = ''
                strtemp = str_head + '(' + str_mid + ')'    # 순서 재구성...

            flag1 = is_english_name(str_mid)
            flag2 = is_english_name(str_head)
            if is_english_name(str_mid) and not is_english_name(str_head):
                str_mid_korean = get_korean_name(str_mid)
                if str_head.endswith(str_mid_korean):   # '365엠씨(mc)의원'과 같은 경우
                    alt_name = str_head[:-len(str_mid_korean)] + str_mid
                else:
                    alt_name = str_mid
                if str_tail != '': alt_name += ' '; alt_name += str_tail
                strtemp = str_head
                if str_tail != '': strtemp += ' ';  strtemp += str_tail
            elif is_english_name(str_head) and not is_english_name(str_mid) and not str_mid.endswith('점'):  # 한글 이름이 공식명칭, 영어 이름은 별칭...
                str_head_korean = get_korean_name(str_head)
                if str_mid.endswith('전문'):      # ''Math Mecca (수학전문) 학원'와 같은 경우
                    alt_name = str_head + ' ' + str_mid     # 별칭에 'Math Mecca 수학전문 학원' 이렇게 기록...
                    strtemp = str_head
                elif str_head_korean.endswith(str_mid):   # '365mc(엠씨)의원'과 같은 경우
                    alt_name = str_head
                    strtemp = str_head_korean
                else:
                    alt_name = str_head
                    strtemp = str_mid
                if str_tail != '': alt_name += ' '; alt_name += str_tail
                if str_tail != '': strtemp += ' ';  strtemp += str_tail
            elif get_korean_number(str_mid) == str_head and str_head != '':        # '구(9)카페', '칠삼(73)'과 같은 경우 처리
                alt_name = str_mid
                if str_tail != '': alt_name += ' '; alt_name += str_tail
                strtemp = str_head
                if str_tail != '': strtemp += ' ';  strtemp += str_tail
            elif (get_korean_number(str_mid) == str_head or get_korean_number(str_head) == str_mid) and str_tail == '':     # '589(오팔구)'와 같은 경우 처리
                alt_name = str_mid
                strtemp = str_head
            elif is_hanja_name(str_mid) and str_tail == "":     # '도곡미주리(味酒里)'와 같이 한자가 포함된 이름 처리
                alt_name = str_mid
                strtemp = str_head
            elif is_hanja_name(str_head) and str_tail == "":     # '味酒里(미주리)'와 같은 경우, '솥뚜껑生(생)/삼겹살'과 같은 경우 처리
            # 한글자라도 한자가 포함되면if is_hanja_name(str_head) 조건이 True가 되므로, '솥뚜껑生(생)/삼겹살'과 같은 경우의 처리로직도 여기에 추가
                #alt_name = str_head
                #strtemp = str_mid
                str_head_translated = get_hanja_name(str_head)
                if str_mid == str_head_translated:
                    strtemp = str_mid + ' ' + str_tail      # 한자 부분 삭제
                    alt_name = str_head + ' ' + str_tail
                elif get_hanja_name(str_head[-len(str_mid):]) == str_mid:       # '솥뚜껑生(생)/삼겹살'과 같은 경우 처리
                    strtemp = str_head[:-len(str_mid)] + ' ' + str_mid
                    alt_name = str_head
                else:
                    strtemp = str_head_translated + ' ' + str_mid         # 한자 부분 한글로 치환
                    alt_name = str_head + '(' + str_mid + ')'
            elif is_similar_name(str_head, str_mid):    # '이놈세끼(E놈3끼)'와 같은 경우 처리
                alt_name = str_mid
                if str_tail != '': alt_name += ' '; alt_name += str_tail
                strtemp = str_head
                if str_tail != '': strtemp += ' ';  strtemp += str_tail
            elif is_hanja_name(str_mid):    # '대(大)장군돼지부속', '스시(海)해'와 같은 경우 처리
                str_mid_translated = get_hanja_name(str_mid)
                if str_head == str_mid_translated or str_tail == str_mid_translated:
                    strtemp = str_head + ' ' + str_tail      # 한자 부분 삭제
                    if str_head == str_mid_translated: alt_name = str_mid + ' ' + str_tail
                    else: alt_name = str_head + ' ' + str_mid
                elif str_head[-len(str_mid):] == str_mid_translated:    # '기찻길호(好)삼겹'와 같은 경우 처리
                    strtemp = str_head + ' ' + str_tail  # 한자 부분 삭제, 별칭 추가는 별칭 이름이 복잡해지므로 하지 않음
                else:
                    strtemp = str_head + '(' + str_mid_translated + ')' + str_tail    # 한자 부분 한글로 치환
                    alt_name = str_head + '(' + str_mid + ')' + str_tail
            elif is_hanja_name(str_head):    # '大(대)장군돼지부속'과 같은 경우 처리
                str_head_translated = get_hanja_name(str_head)
                if str_mid == str_head_translated:
                    strtemp = str_mid + ' ' + str_tail      # 한자 부분 삭제
                    alt_name = str_head + ' ' + str_tail
                #elif get_hanja_name(str_head[-len(str_mid):]) == str_mid:       # '솥뚜껑生(생)/삼겹살'과 같은 경우 처리<= 한글자라도 한자가 포함되면 앞의 if is_hanja_name(str_head) 조건이 True가 되므로 앞에서 처리하는 로직 추가했음
                elif str_head_translated[-len(str_mid):] == str_mid:
                    strtemp = str_head[:-len(str_mid)] + ' ' + str_mid + ' ' + str_tail
                    alt_name = str_head + ' ' + str_tail
                else:
                    strtemp = str_head_translated + '(' + str_mid + ')' + str_tail    # 한자 부분 한글로 치환
                    alt_name = str_head + '(' + str_mid + ')' + str_tail
            elif is_hanja_name(str_head[-len(str_mid):]): # '솥뚜껑生(생)/삼겹살'과 같은 경우 처리 <= 한글자라도 한자가 포함되면 앞의 if is_hanja_name(str_head) 조건이 True가 되므로 앞에서 처리하는 로직 추가했음
                if get_hanja_name(str_head[-len(str_mid):]) == str_mid:
                    strtemp = str_head[:-len(str_mid)] + ' ' + str_mid + ' ' + str_tail
                    alt_name = str_head + ' ' + str_tail
            else:
                #if idx2 == len(strtemp) - 1:  # str_tail == ""인 경우 <= '(노원하계점)하남돼지집'과 같은 경우 '하남돼지집(노원하계점)'과 같이 문자열의 순서 변경했음, 이로 인해 조건 체크 방법 변경해야 함 (str_tail == '' 조건으로)

                # to do : 아래와 같은 이름들 처리...
                # '정철어학원Jr.(주니어)용봉학원'

                if str_tail =='':
                    if __name__ == '__main__':
                        if get_korean_name(str_mid) == str_head or get_korean_name(str_head) == str_mid:    # '지에스25강릉대박점(GS25강릉대박점)'와 같은 경우
                            if str_mid != str_head and len(str_head) > 4:
                                alt_name = str_mid
                                strtemp = str_head
                        elif is_subname(str_mid):
                            pp_subname = str_mid
                            strtemp = str_head
                        elif str_mid[-2:] == str_head[-2:]:     # '이판사판철판(2pan4pan철판)'와 같은 경우 처리
                            alt_name = str_mid
                            strtemp = str_head
                    else:
                        if get_korean_name(str_mid) == str_head or get_korean_name(str_head) == str_mid:    # '지에스25강릉대박점(GS25강릉대박점)'와 같은 경우
                            if str_mid != str_head and len(str_head) > 4:
                                alt_name = str_mid
                                strtemp = str_head
                        elif is_subname(str_mid):
                            pp_subname = str_mid
                            strtemp = str_head
                        elif str_mid[-2:] == str_head[-2:]:     # '이판사판철판(2pan4pan철판)'와 같은 경우 처리
                            alt_name = str_mid
                            strtemp = str_head

                        #else:   # 맨 뒤의 괄호는 etc_name으로 넣을까???
                        #    if etc_name != '': etc_name += ';'
                        #    etc_name = str_mid
                        #    strtemp = str_head


    # 나머지 한자어 처리...
    if is_hanja_name(strtemp):
        if alt_name != '':  alt_name += ';'
        alt_name += strtemp
        strtemp = get_hanja_name(strtemp)

    strtemp = strtemp.replace('(', ' (').replace(')', ') ').replace('( (', '((').replace(') )', '))') \
        .replace('"', ' ').replace('  ', ' ').replace('  ', ' ').lstrip().rstrip()

    token_list = strtemp.split(' ')

    token_list_length = len(token_list)
    if token_list_length > 1:
        head_token = token_list[0]
        if head_token == "비알코리아":   # 버려야 하는 회사이름 check (to do : 사전 만들어 체크할 것!) <= 체크하는 위치 어디가 가장 좋을까???
            if etc_name != '': etc_name += ';'
            etc_name += head_token
            token_list.pop(0)

    token_list_length = len(token_list)
    if token_list_length > 1 and pp_subname == '':
        # to do : 여기서 브랜드 이름도 처리... (일부 패턴은 뒤쪽에서 처리하도록 수정함...)
        # 'CU 양구 정중앙점', '(주)캘리스코 사보텐 롯데프리미엄 아울렛 파주점' 이런 이름 어려움 ㅠㅠ
        tail_token = token_list[token_list_length-1]
        if is_subname(tail_token):
            pp_subname = tail_token
            token_list.pop(token_list_length-1)
        elif is_etcname(tail_token):
            if tail_token.startswith('(') and tail_token.endswith(')'): tail_token = tail_token[1:-1]

            if etc_name != '': etc_name += ';'
            etc_name += tail_token
            token_list.pop(token_list_length - 1)

    for i in range(len(token_list)):
        if i != 0: pp_name += ' '
        pp_name += token_list[i]

    if alt_name != '':
        if is_hanja_name(alt_name) and len(alt_name) >= 2:     # 한글자짜리 한자어는 한글로 변환한 별칭 추가하지 않음...
            alt_name_translated = get_hanja_name(alt_name)
            if alt_name_translated != pp_name:
                alt_name += ';' + alt_name_translated

    # 불필요한 공백 문자 마지막으로 제거...
    pp_name = pp_name.replace(' -', '-').replace('- ', '-')
    alt_name = alt_name.replace(' -', '-').replace('- ', '-')

    # 예외 처리
    if pp_name == '구' and pp_subname != '':
        pp_name = pp_name + ' ' + pp_subname
        pp_subname = ''


    return pp_name, pp_subname, alt_name, etc_name


def is_english_name(name):
    strtemp = name.replace('&', '').replace('-', '').replace('\'', '').replace('.', '').replace(',', '').replace('/', '').replace('!', '')\
        .replace('*', '').replace('+', '').replace('°', '').replace('℃', '').replace(' ', '').upper()
    if strtemp.isdigit(): return False
    # else: return strtemp.isalnum()      # utf-8에서는 동작안함 ㅠㅠ

    for i in range(len(strtemp)):
        ch = strtemp[i]
        if ch >= '0' and ch <= '9': continue
        elif ch >= 'A' and ch <= 'Z': continue
        else: return False

    return True

def is_korean_name(name):
    strtemp = name.replace('&', '').replace('-', '').replace('\'', '').replace('.', '').replace(',', '').replace('/', '').replace('!', '')\
        .replace('*', '').replace('+', '').replace('°', '').replace('℃', '').replace(' ', '').upper()

    if strtemp.isdigit(): return False
    # else: return strtemp.isalnum()      # utf-8에서는 동작안함 ㅠㅠ

    for i in range(len(strtemp)):
        ch = strtemp[i]
        if ch >= '0' and ch <= '9': return False
        elif ch >= 'A' and ch <= 'Z': return False

    return True

def is_subname(name):
    if name == "본점": return True
    elif len(name) > 2 and name.endswith('점'):
        if name.endswith('전문점'): return False
        elif name.endswith('편의점'): return False
        elif name.endswith('음식점'): return False
        elif name.endswith('커피점'): return False
        else: return True
    else: return False

def is_etcname(name):
    if len(name) < 2: return False
    if name.startswith('(') and name.endswith(')'): name = name[1:-1]

    name_tail = name[-1:]
    if name_tail != '호' and name_tail != '층' and name_tail != 'F': return False
    name_head = name[:-1]
    if name_head.startswith('지하'): name_head = name_head[2:]
    elif name_head.startswith('B'): name_head = name_head[1:]

    if name_head == '': return False
    else: return name_head.isdigit()

def split_newaddr(newaddr):
    str_head = ''
    str_tail = ''
    temp_list = newaddr.split(' ')

    for i in range(len(temp_list)):
        token = temp_list[i]

        if is_jibun(token):
            if token.endswith(','): token = token[:-1]
            str_head += ' '
            str_head += token

            for j in range(i+1, len(temp_list), 1):
                str_tail += ' '
                str_tail += temp_list[j]

            break
        else:
            str_head += ' '
            str_head += token

    return str_head.lstrip(), str_tail.lstrip()

def is_jibun_added_token(token):
    idx = token.rfind('길')
    if idx >= 2:
        if is_jibun(token[idx+1:]): return True, token[:idx+1], token[idx+1:]

    idx = token.rfind('로')
    if idx >= 2:
        if is_jibun(token[idx+1:]): return True, token[:idx+1], token[idx+1:]

    idx = token.rfind('리')
    if idx >= 2:
        if is_jibun(token[idx+1:]): return True, token[:idx+1], token[idx+1:]

    idx = token.rfind('읍')
    if idx >= 2:
        if is_jibun(token[idx+1:]): return True, token[:idx+1], token[idx+1:]

    idx = token.rfind('면')
    if idx >= 2:
        if is_jibun(token[idx+1:]): return True, token[:idx+1], token[idx+1:]

    idx = token.rfind('동')
    if idx >= 2:
        if is_jibun(token[idx+1:]): return True, token[:idx+1], token[idx+1:]

    return False, token, ''

def is_jibun(token):
    strtemp = token
    if strtemp.endswith(','): strtemp = strtemp[:-1]
    if strtemp.endswith('.'): strtemp = strtemp[:-1]
    if strtemp.endswith('번지'): strtemp = strtemp[:-2]
    if strtemp.startswith('산'): strtemp = strtemp[1:]
    if strtemp.startswith('지하'): strtemp = strtemp[2:]
    if strtemp.startswith('공중'): strtemp = strtemp[2:]
    if strtemp == "":
        return False

    strtemp = strtemp.replace('-', '')
    if strtemp == "":
        return False

    return strtemp.isdigit()

def is_hanja_name(src):    # 한글자라도 한자가 있으면 True 반환
    for i in range(len(src)):
        if hanja.is_hanja(src[i]): return True

    return False

def get_hanja_name(name):
    str_result = hanja.translate(name, 'substitution')
    return str_result.replace('李', '이').replace('老', '노').replace('劉', '유').replace('串', '관').replace('利', '이').replace('金', '금')\
        .replace('梨', '이').replace('料', '요').replace('炙', '적').replace('樂', '락').replace('樂', '락').replace('茶', '차').replace('龍', '용')\
        .replace('兩', '양').replace('六', '육')    # 발음이 두가지 이상인 한자의 임시 처리 ㅠㅠ

def is_similar_name(src1, src2):    # 약식 비교 함수...
    # 몽스, 몽's 와 같은 경우 처리
    if src2.endswith('\'s') and src1.endswith('스'):
        if src2[:-2] == src1[:-1]: return True
        else: return False
    elif src1.endswith('\'s') and src2.endswith('스'):
        if src1[:-2] == src2[:-1]: return True
        else: return False

    if len(src1) != len(src2): return False
    elif is_korean_name(src1) and is_korean_name(src2): return False    # 둘 다 한국어이면 비교하지 않음
    elif len(src1) < 4: return False    # 일단 4글자 이상인 경우만 비교

    word_len = len(src1)
    same_ch_count = 0
    for i in range(word_len):
        if src1[i] == src2[i]:
            same_ch_count += 1

    if same_ch_count*2 >= word_len: return True
    else: return False

def get_korean_name(name):
    src = name.upper()
    target = ''
    for i in range(len(src)):
        ch = src[i]
        if ch == 'A': target += u'에이'
        elif ch == 'B': target += u'비'
        elif ch == 'C': target += u'씨'
        elif ch == 'D': target += u'디'
        elif ch == 'E': target += u'이'
        elif ch == 'F': target += u'에프'
        elif ch == 'G': target += u'지'
        elif ch == 'H': target += u'에이치'
        elif ch == 'I': target += u'아이'
        elif ch == 'J': target += u'제이'
        elif ch == 'K': target += u'케이'
        elif ch == 'L': target += u'엘'
        elif ch == 'M': target += u'엠'
        elif ch == 'N': target += u'엔'
        elif ch == 'O': target += u'오'
        elif ch == 'P': target += u'피'
        elif ch == 'Q': target += u'큐'
        elif ch == 'R': target += u'알'
        elif ch == 'S': target += u'에스'
        elif ch == 'T': target += u'티'
        elif ch == 'U': target += u'유'
        elif ch == 'V': target += u'브이'
        elif ch == 'W': target += u'더블유'
        elif ch == 'X': target += u'엑스'
        elif ch == 'Y': target += u'와이'
        elif ch == 'Z': target += u'지'
        else: target += ch

    return target

def get_korean_number(src):
    target = ''
    for i in range(len(src)):
        ch = src[i]
        if not ch.isdigit(): return ''
        elif ch == '0': target += u'공'   # '영' or '공' ???
        elif ch == '1': target += u'일'
        elif ch == '2': target += u'이'
        elif ch == '3': target += u'삼'
        elif ch == '4': target += u'사'
        elif ch == '5': target += u'오'
        elif ch == '6': target += u'육'
        elif ch == '7': target += u'칠'
        elif ch == '8': target += u'팔'
        elif ch == '9': target += u'구'
        else: return ''

    return target

def pp_address(src):
    stem=''; jibun=''
    road_addr = ''
    jibun_addr = ''
    etc_addr = ''

    strtemp = src.replace('도로명주소', '').replace('상세정보주소', '').replace('새주소', '').replace('구주소', '').replace('지번', '').replace('주소', '') \
        .replace('대한민국', '').replace('<br>', ' ').replace('?', ' ').replace('\\', ' ').replace('직할시', '광역시')\
        .replace('[', '(').replace(']', ')').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ') \
        .replace(' 산 ', ' 산').replace(' 지하 ', ' 지하').replace(' 공중 ', ' 공중').lstrip().rstrip()
    strtemp = strtemp.replace('(', ' (').replace(',', ' , ').replace('  ', ' ').replace('  ', ' ').lstrip().rstrip()
    strtemp = strtemp.replace('&nbsp;', ' ').lstrip().rstrip()

    if strtemp.startswith(':'): strtemp = strtemp[1:].lstrip()
    if strtemp.startswith('('):
        idx = strtemp.find(')')
        if idx != -1: strtemp = strtemp[idx+1:].lstrip()

    emd_flag = False;   ri_flag = False;    road_addr_flag = False
    word_list = strtemp.split(' ')

    # to do : '도산대로31'과 같이 붙여 쓴 경우 '도산대로 31'과 같이 분리...
    strtemp = ''
    for i in range(len(word_list)):
        token = word_list[i]
        flag, head, tail = is_jibun_added_token(token)
        if flag == True: strtemp += ' ' + head + ' ' + tail
        else: strtemp += ' ' + head

    strtemp = strtemp.lstrip().rstrip()
    word_list = strtemp.split(' ')

    for i in range(len(word_list)):
        token = word_list[i]
        if is_jibun(token):
            idx = token.find(',')
            if idx != -1:   # '203,2층' 이렇게 쓴 경우에 대비해서...
                etc_addr = token[idx+1:]
                token = token[:idx]

            jibun = token

            if token.startswith('산'):
                road_addr_flag = False

            for j in range(i+1,len(word_list),1):
                if etc_addr != '': etc_addr += ' '
                etc_addr += word_list[j]

            break
        elif is_road_name(token): road_addr_flag = True
        elif is_emd_name(token): emd_flag = True
        elif is_ri_name(token): ri_flag = True

        if stem != '':  stem += ' '
        stem += token

    if road_addr_flag:
        road_addr = stem + ' ' + jibun
    elif emd_flag or ri_flag:
        jibun_addr = stem + ' ' + jibun

    etc_addr = etc_addr.replace(' , ', ',').replace(' ,', ',').replace(', ', ',')

    if etc_addr.startswith('번지'): etc_addr = etc_addr[2:].lstrip()
    if etc_addr.startswith(','): etc_addr = etc_addr[1:].lstrip()

    if road_addr.endswith('번지'): road_addr = road_addr[:-2].rstrip()
    if jibun_addr.endswith('번지'): jibun_addr = jibun_addr[:-2].rstrip()

    return road_addr, jibun_addr, etc_addr

def pp_address_jibun(src):
    pp_result = ''
    word_list = src.split(' ')

    for i in range(len(word_list)):
        if i == len(word_list) -1:
            pp_result += ' ' + word_list[i]
            break
        elif i >= len(word_list): break      # word_list.pop(i+1)의 여파로 체크 필요

        token = word_list[i]
        next_token = word_list[i+1]

        if token.endswith('번지') and token[:-2].isdigit() and next_token.endswith('호') and next_token[:-1].isdigit():
            pp_result += ' ' + token[:-2] + '-' + next_token[:-1]
            word_list.pop(i+1)
        else:
            pp_result += ' ' + word_list[i]

    return pp_result

def is_road_name(src):
    #if len(src) < 3: return False
    if len(src) < 2: return False # '내영산 1길'과 같이 도로이름을 분리해 쓴 경우가 많어서...
    # 세종로, 시장북로 <= '로'로 끝나는 행법정동 이름 (행법정동 '남성로'는 없어진 듯...)
    elif src == '세종로' or src == '시장북로': return False
    elif src.endswith('로') or src.endswith('길'): return True
    elif src == '계변고개': return True
    else: return False

def is_emd_name(src):
    if len(src) < 2: return False
    # 세종로, 시장북로 <= '로'로 끝나는 행법정동 이름 (행법정동 '남성로'는 없어진 듯...)
    elif src.endswith('읍') or src.endswith('면') or src.endswith('동') or src.endswith('가'): return True
    elif src == '세종로' or src == '시장북로': return True
    else: return False

def is_ri_name(src):
    if len(src) < 2: return False
    elif src.endswith('리'): return True
    else: return False

def pp_hira_name(store_nm):
    store_etcname = ''

    # 이름 전처리
    if store_nm.startswith('('):
        idx = store_nm.find(')')
        if idx != -1 and idx <= 5:
            store_nm = store_nm[idx + 1:].lstrip()
        else:
            store_nm = store_nm[1:idx] + ' ' + store_nm[idx + 1:]

    if store_nm.endswith(')'):
        idx = store_nm.rfind('(')
        store_etcname = store_nm[idx + 1:-1]
        store_nm = store_nm[:idx].rstrip()

    idx = store_nm.find(')')
    if idx != -1 and idx <= 1: store_nm = store_nm[idx + 1:]  # '사)', '재)'와 같은 것들 처리

    store_nm = store_nm.replace('사단법인', '').replace('의료재단법인', '').replace('재단법인', '').replace('의료법인', '').replace('사회복지법인', '')
    store_nm = store_nm.replace('비영리특수법인', '').replace('학교법인', '')
    store_nm = store_nm.replace('(사)', ' ').replace('(재)', ' ').replace('주식회사', '(주)').replace('㈜', '(주)').replace('(주)', ' ').replace('  ', ' ').replace('  ', ' ').lstrip().rstrip()

    if store_nm.startswith(')'): store_nm = store_nm[1:].lstrip()

    if store_nm.find('학원부설') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('학원부설')
        if idx + 8 <= len(store_nm):  # '학원부설' 뒤의 이름이 최소 4자
            strtail = store_nm[idx + 4:].lstrip()
            if not strtail.startswith('치과') and not strtail.startswith('요양'):
                if store_etcname != '': store_etcname += ';'
                store_etcname += store_nm[:idx + 4]
                store_nm = strtail
    elif store_nm.find('부설') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('부설')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            strtail = store_nm[idx+2:].lstrip()
            if not strtail.startswith('치과') and not strtail.startswith('요양'):
                if store_etcname != '': store_etcname += ';'
                store_etcname += store_nm[:idx + 2]
                store_nm = strtail
    elif store_nm.find('부속') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('부속')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            strtail = store_nm[idx+2:].lstrip()
            if not strtail.startswith('치과') and not strtail.startswith('요양'):
                if store_etcname != '': store_etcname += ';'
                store_etcname += store_nm[:idx + 2]
                store_nm = strtail
    elif store_nm.find('학원') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('학원')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 2]
            store_nm = store_nm[idx + 2:].lstrip()
    elif store_nm.find('재단') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('재단')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 2]
            store_nm = store_nm[idx + 2:].lstrip()
    elif store_nm.find('지회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('지회')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 2]
            store_nm = store_nm[idx + 2:].lstrip()
    elif store_nm.find('지부') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('지부')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 2]
            store_nm = store_nm[idx + 2:].lstrip()
    elif store_nm.find('협회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('협회')
        if idx + 6 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 2]
            store_nm = store_nm[idx + 2:].lstrip()
    elif store_nm.find('원불교') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('원불교')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('관음종') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('관음종')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('수녀회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('수녀회')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('수도회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('수도회')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('선교회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('선교회')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('연합회') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('연합회')
        if idx + 7 <= len(store_nm):  # 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 3]
            store_nm = store_nm[idx + 3:].lstrip()
    elif store_nm.find('의료공단') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('의료공단')
        if idx + 8 <= len(store_nm):  # '의료공단' 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 4]
            store_nm = store_nm[idx + 4:].lstrip()
    elif store_nm.find('협동조합') != -1 and (store_nm.endswith('병원') or store_nm.endswith('의원')):
        idx = store_nm.find('협동조합')
        if idx + 8 <= len(store_nm):  # '협동조합' 뒤의 이름이 최소 4자
            if store_etcname != '': store_etcname += ';'
            store_etcname += store_nm[:idx + 4]
            store_nm = store_nm[idx + 4:].lstrip()

    return store_nm, store_etcname

