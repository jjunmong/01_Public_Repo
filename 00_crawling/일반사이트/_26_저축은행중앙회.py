import sys
import time
import codecs
import requests
import random
import json
import bs4

def main():

    outfile = codecs.open('26_저축은행중앙회.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ID|TELL|OLDADDR|NEWADDR\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        if store_list ==[] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['id'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['oldaddr'])
            outfile.write(u'%s\n' % store['newaddr'])
        page += 5
        time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getStoreInfo(page):
    url = 'https://www.fsb.or.kr/sabfindquic_0100.jct'
    data = {
        "AREA":"",
        "IBANK":"",
        "MBANK":"",
        "PLOAN":"",
        "N_FUNDS":"",
        "CD":"",
        "CDP":"",
        "ATM":"",
        # "END_NUM":"135",
        # "START_NUM":"131",
        "STR_SORT":"SEQ DESC",
        "ADDR":"",
        "SEARCHTEXT":"",
        "SEARCHVAL":"1"
    }
    data['START_NUM'] = page
    data['END_NUM'] = page + 4
    pageString = requests.post(url , data = data).text
    print(page)
    jsonString = json.loads(pageString)
    entityList  = jsonString['REC']
    result =[]
    for info in entityList:
        name = info['BANK_NAME'] + '저축은행'
        branch = info['BRANCH_NAME']
        if branch.startswith('(출)'): branch = branch[3:].lstrip() + '출장소'
        elif branch.endswith('영업부'): pass
        elif branch.endswith('출장소'): pass
        elif branch.endswith('센터'): pass
        elif not branch.endswith('점'): branch += '지점'
        id = info['SEQ']
        try :
            tell = info['TEL']
        except :
            try :
                tell = info['DTEL']
            except:
                tell = info['CTEL']
        oldaddr = info['NAVER_MAP_ADDR']
        newaddr = info['ADDRESS']
        result.append({"name":name,"branch":branch,"id":id,"tell":tell,"oldaddr":oldaddr,"newaddr":newaddr})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()