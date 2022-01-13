import sys
import requests
import bs4
import codecs
import time
import random
import json

def main():

    outfile = codecs.open('72_두끼.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    url_list = getStoreInfo_url_list()
    for url in url_list:
        storeList = getStoreInfo(url)
        for store in storeList:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo_url(intPageNo):
    url = 'http://xn--299ayy032bcuap7u2xa.com/ajax/get_map_list.cm'
    data = {
        'board_code': 'b201811285bfe357fcebb7',
        'search': '',
        'search_mod': 'all',
        # 'page': '3',
        'sort': 'TIME',
        'status': '',
    }
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '81',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'COCOASESSID=462qr5tt5fiqr1lpp59hs6bmorqn2mvcuhasa3tjfd0hscsdjqd7uimo0127no4in450467aoc4vh7qftmc3aofhm95k09kv0mgbhk1; SITE_STAT_SID=202007015efc32f613ec90.37176112; SITE_STAT_SID_m201811285bfe357d9ac7e=202007015efc32f613eec5.34028266; SITE_STAT_SID_m201811285bfe357d9af3d=202007015efc32f90bfd59.46735249',
        'Host': 'xn--299ayy032bcuap7u2xa.com',
        'Origin': 'http://xn--299ayy032bcuap7u2xa.com',
        'Pragma': 'no-cache',
        'Referer': 'http://xn--299ayy032bcuap7u2xa.com/29/?sort=TIME&keyword_type=all&page=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data['page'] = intPageNo
    pageString = requests.post(url, headers = headers,data = data).text
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    print(url, intPageNo)
    div = bsObj.find_all('div',{"data-bcode":"b201811285bfe357fcebb7"})
    result = []
    for info in div:
        ids = info['id']
        ids = str(ids).replace('list_','')
        result.append(ids)
    return result

def getStoreInfo(url_list):
    url = 'http://xn--299ayy032bcuap7u2xa.com/ajax/get_map_post_data.cm'
    data = {
        # 'idx': '124781',
        'board_code': 'b201811285bfe357fcebb7',
    }
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '81',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'COCOASESSID=462qr5tt5fiqr1lpp59hs6bmorqn2mvcuhasa3tjfd0hscsdjqd7uimo0127no4in450467aoc4vh7qftmc3aofhm95k09kv0mgbhk1; SITE_STAT_SID=202007015efc32f613ec90.37176112; SITE_STAT_SID_m201811285bfe357d9ac7e=202007015efc32f613eec5.34028266; SITE_STAT_SID_m201811285bfe357d9af3d=202007015efc32f90bfd59.46735249',
        'Host': 'xn--299ayy032bcuap7u2xa.com',
        'Origin': 'http://xn--299ayy032bcuap7u2xa.com',
        'Pragma': 'no-cache',
        'Referer': 'http://xn--299ayy032bcuap7u2xa.com/29/?sort=TIME&keyword_type=all&page=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data['idx'] = url_list
    pageString = requests.post(url, headers = headers,data = data).text
    jsondata = json.loads(pageString)
    entityData = jsondata['post_data']
    print(url , url_list)
    result = []
    name = '생고기제작소'
    branch = entityData['subject']
    addr = entityData['address']
    tell = entityData['phone_number']
    xcord = entityData['pos_x']
    ycord = entityData['pos_y']
    result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def getStoreInfo_url_list():
    result = []
    for num in range(getPage()):
        result = result + getStoreInfo_url(num)
    time.sleep(random.uniform(0.3, 0.9))

    results = list(set(result))
    return results

def getPage():
    url = 'http://xn--299ayy032bcuap7u2xa.com/29'
    pageString = requests.post(url).text
    bsObj = bs4.BeautifulSoup(pageString,'html.parser')
    page = bsObj.select('#map_list_fold_b201811285bfe357fcebb7 > div.map-list > div.map-toolbar > div.toolbar_top.map-inner > div.head_wrap.clearfix > div.tit > span')
    page = str(page).replace('<span class="text-brand" style="vertical-align: middle">','').replace('</span>','').replace('[','').replace(']','')
    page = int(int(page)/10+1)
    return page

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()