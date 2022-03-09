import bs4
import codecs
import time
import requests
import sys
import json
import random

def main():
    outfile = codecs.open('22_구석구석맛집.txt', 'w', 'utf-8')
    outfile.write("NAME|CID|TEL|OLD_ADDR|NEW_ADDR|XCORD|YCOORD|RESTDATE|PARK\n")
    store_list = getStores_id_list()
    result = []
    for info in store_list:
        try:
            result = result + getStores_info(info)
        except:
            pass

    for store in result:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['cid'])
        outfile.write(u'%s|' % store['tel'])
        outfile.write(u'%s|' % store['old_addr'])
        outfile.write(u'%s|' % store['new_addr'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s|' % store['ycord'])
        outfile.write(u'%s|' % store['restdate'])
        outfile.write(u'%s\n' % store['park'])

    outfile.close()

def getStores_id(intpageNo):
    url = "https://korean.visitkorea.or.kr/json/jsp/search_json.jsp"
    data = {
        'query': '음식',
        'collection': 'ALL',
        'contentTypeNameValue': '',
        'contentSearchField': 'TITLE/100,DISPLAY_TITLE/70,AREA_NAME/50,SIGUGUN_NAME/30,TAG_NAME/50,BODY/50,SUB_NAME/50',
        'rankOption': 'rpkmo',
        'sort': 'RANK/DESC',
        'totalContentCount': '',
        'totalMediaCount': '',
        'totalNewsCount': '',
        'listCount': '',
    }
    data['startCount'] = intpageNo
    try :
        urlopen = requests.post(url , data = data)
        print(urlopen,url,data['startCount'])
    except :
        print('Error calling the API')
    urlopen.encoding = 'utf-8'
    html = urlopen.text
    html = html.replace('\\', ',')
    json_data = json.loads(html)
    data_list = json_data['Data'][0]['Result']
    data = []
    for id in data_list:
        COT_ID = id['COT_ID']
        data.append(COT_ID)
    return  data

def getStores_id_list():
    data = []
    for number in range(0 , 1000 , 10):
        data = data + getStores_id(number)
    return data

def getStores_info(cotid):
    url = "https://korean.visitkorea.or.kr/call"
    data = {
        "cmd": "TOUR_CONTENT_BODY_VIEW",
        "locationx": "",
        "locationy": "",
        "stampId": ""
    }
    data['cotid'] = cotid
    try :
        urlopen = requests.post(url , data = data)
        print(urlopen,url,data['cotid'])
    except :
        print('Error calling the API')
    urlopen.encoding = 'utf-8'
    json_info = urlopen.text
    try:
        json_data = json.loads(json_info)
        data_list = json_data['body']['article']
        print(data_list)
    except:
        pass
        print("body request error")
    else:
        data = []
        for info in data_list:
            try:
                name = info['title']
                cid = info['cid']
                # tagName = info['tagName']
                tel = info['telNo']
                old_addr = info['addr1']
                new_addr = info['addr2']
                xcord= info['mapX']
                ycord= info['mapY']
                # detailInfo = info['overView']
                # menu = info['treatMenu']
                restdate = info['restDate']
                # homepage = info['homepage']
                park = info['parking']
            except :
               pass
            else:
                data.append({"name":name,"cid":cid,"tel":tel,"old_addr":old_addr,"new_addr":new_addr,
                             "xcord":xcord,"ycord":ycord,"restdate":restdate,"park":park})
        return data

