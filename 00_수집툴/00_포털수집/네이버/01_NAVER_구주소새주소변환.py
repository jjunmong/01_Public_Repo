import time
import codecs
import requests
import json
import random
start = time.time()

outfile = codecs.open('NEWADDR_CONVERT.txt', 'w', 'utf-8')
outfile.write("INPUTNAME|NEWADDR\n")

def getInfo(inputName):
    url ="https://map.naver.com/v5/api/search?caller=pcweb&query={} 도로명 주소&type=all&searchCoord=127.02064275741579;37.48851429249171&page=1&displayCount=20&isPlaceRecommendationReplace=true&lang=ko".format(inputName)
    req = requests.get(url).text
    print(req)
    data = json.loads(req)
    list = []
    try:
        data_all = data['result']['address']['jibunsAddress']['list']
    except TypeError:
        list.append({"inputName": inputName, "newaddr": "이미새주소"})
    else:
        for ss in data_all:
            try:
                newaddr = ss['mappedAddress']['fullAddress']
            except TypeError:
                list.append({"inputName": inputName, "newaddr": None})
            else:
                list.append({"inputName":inputName,"newaddr":newaddr})
    return list

with open('new_addr_list.txt') as data:
   lines = data.read().splitlines()

input_list = lines

timedelay = random.random()

result = []
for get in input_list:
    time.sleep(timedelay)
    result = result + getInfo(get)

for ssd in result:
    print(ssd)

for result_list in result:
    outfile.write(u'%s|' % result_list['inputName'])
    outfile.write(u'%s|\n' % result_list['newaddr'])
outfile.close()

print("time :", time.time() - start)