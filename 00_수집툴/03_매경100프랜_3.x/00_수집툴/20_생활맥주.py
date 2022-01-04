import json
import requests
import codecs
import sys

def main():
    outfile=codecs.open('20_생활맥주.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])
    outfile.close()

def getStoreInfo():
    url = "https://dailybeer.co.kr/board/view3_map_google/resource/place_find.php"
    data = {
        'board': 'map_01',
        'sca': 'all',
        'skin': 'map_google',
        'search': '',
        'select': '',
        'geolocation': 'true',
    }
    pageString = requests.get(url, params = data).text
    jsonString = json.loads(pageString)
    entityList = jsonString['data']
    data = []
    for info in entityList:
        try:
            name = "생활맥주"
            branch = info['subject']
            addr = info['address']
            tell = str(info['phone']).replace(')','-')
            xcord = info['geocode']['lng']
            ycord = info['geocode']['lat']
        except :
            pass
        else :
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell,'xcord':xcord,'ycord':ycord})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()


