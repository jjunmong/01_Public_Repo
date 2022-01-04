import time
import codecs
import requests
import json
import random
start = time.time()

outfile = codecs.open('가구인테리어전체_input1_RESULT.txt', 'w', 'utf-8')
outfile.write("INPUTNAME|NAME|OLDADDR|NEWADDR|TELL|CAT\n")

with open('가구인테리어전체_input1.txt') as data:
   lines = data.read().splitlines()

input_list = lines

def getInfo(inputName):
    list = []
    url ="https://map.naver.com/v5/api/search?caller=pcweb&query={}&type=place&searchCoord=127.02064275741569;37.48851429249171&page=1&displayCount=20&isPlaceRecommendationReplace=true&lang=ko".format(inputName)
    hdr = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    req = requests.get(url, headers=hdr)
    print(req, inputName)
    time.sleep(0.3)
    req_data = req.text
    try:
        data = json.loads(req_data)
        data_all = data['result']['place']['list']
        print(data_all)
    except json.decoder.JSONDecodeError :
        print("연결 끊김")
    except TypeError:
        list.append({"inputName": inputName, "name": None, "oldaddr": None, "newaddr": None, "tell": None, "cat": None})
    except KeyError:
        list.append({"inputName": inputName, "name": None, "oldaddr": None, "newaddr": None, "tell": None, "cat": None})
    else:
        try:
            name = data_all[0]['name']
            oldaddr = data_all[0]['address']
            newaddr = data_all[0]['roadAddress']
            tell = data_all[0]['tel']
            cat = data_all[0]['category']
        except IndexError :
            list.append({"inputName": inputName, "name": None, "oldaddr":None, "newaddr": None, "tell": None, "cat": None})
        except AttributeError:
            list.append({"inputName": inputName, "name": None, "oldaddr": None, "newaddr": None, "tell": None, "cat": None})
        else:
            list.append({"inputName":inputName,"name":name,"oldaddr":oldaddr,"newaddr":newaddr,"tell":tell,"cat":cat})
    return list

result = []
for get in input_list:
    time.sleep(1.5)
    result = result + getInfo(get)

for ssd in result:
    print(ssd)

for results in result:
    outfile.write(u'%s|' % results['inputName'])
    outfile.write(u'%s|' % results['name'])
    outfile.write(u'%s|' % results['oldaddr'])
    outfile.write(u'%s|' % results['newaddr'])
    outfile.write(u'%s|' % results['tell'])
    outfile.write(u'%s|\n' % results['cat'])
outfile.close()

print("time :", time.time() - start)