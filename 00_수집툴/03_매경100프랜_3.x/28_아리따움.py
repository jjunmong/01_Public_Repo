import json
import requests
import codecs
import time
import sys
import random

def main():

    outfile = codecs.open('28_아리따움.txt', 'w', 'utf-8')
    outfile.write("NAME|ID|BRANCH|NEW_ADDR|DEATAIL_ADDR|TELL|XCORD|YCORD\n")

    page = getStoreNum()
    for pageNo in range (page):
        store_list = getStoreInfo(pageNo)
        print(len(store_list), store_list)
        if store_list == [] : break;

        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['new_addr'])
            outfile.write(u'%s|' % store['detail_addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])

        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreNum():
    url = 'https://www.aritaum.com/promotion/st/promotion_st_store_find_json.do'
    params = {
        'i_sSearchType': '',
        'i_sLatitude': '37.5160832',
        'i_sLongitude': '127.1144448',
        'i_sLikeStoreSearch': '',
        'i_sLiveStoreYn': '',
        'i_sFlagLiveWeek': '',
        'i_iNowPageNo': '',
        'i_sSearchKeyword': '매장명 또는 주소명칭으로 검색.',
        'selectCity1': '',
        'selectCity2': '',
    }
    jsonData = requests.post(url, data=params).text
    print(url, params)
    jsonString = json.loads(jsonData)
    entityList_num = jsonString['object']['storeFindListCount']
    entityList_num = int((entityList_num/100) + 2)
    print(entityList_num)
    return  entityList_num

def getStoreInfo(intPageNo):
    url ='https://www.aritaum.com/promotion/st/promotion_st_store_find_json.do'
    params = {
        'i_sSearchType': '',
        'i_sLatitude': '37.5160832',
        'i_sLongitude': '127.1144448',
        'i_sLikeStoreSearch': '',
        'i_sLiveStoreYn': '',
        'i_sFlagLiveWeek':'',
        # 'i_iNowPageNo': '2',
        'i_sSearchKeyword': '매장명 또는 주소명칭으로 검색.',
        'selectCity1': '',
        'selectCity2':'',
    }
    params['i_iNowPageNo'] = intPageNo
    data=[]
    jsonData = requests.post(url, data = params).text
    print(url , params)
    jsonString = json.loads(jsonData)
    entityList = jsonString['object']['storeFindList']
    for infos in entityList:
        name = "아리따움"
        id = infos['stor_cd']
        branch = infos['stor_nm']
        new_addr = infos['addr']
        try:
            detail_addr = infos['addr2']
        except:
            detail_addr ='없음'
        try:
            tell = infos['tel_no']
        except :
            tell = '없음'
        try:
            xcord = infos['longitude']
        except :
            xcord = '없음'
        try:
            ycord = infos['latitude']
        except :
            ycord = '없음'
        data.append({'name':name, 'id':id, 'branch':branch,'new_addr':new_addr,'detail_addr':detail_addr,'tell':tell,'xcord':xcord,'ycord':ycord})

    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
