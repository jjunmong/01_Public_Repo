import requests
import bs4
import json
import codecs
import sys

def main():
    outfile=codecs.open('18_본도시락.txt', 'w', 'utf-8')
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
        json_url = "https://www.bonif.co.kr/store/listAjax"
        data = {
            'addr': '',
            'strIdx': '',
            'brdCd': 'BF104',
            'lat': '',
            'lng': '',
            'distance': '3',
            'selDiv': 'NOORDER',
            'schKey': '',
            'sido': '',
            'gugun': '',
            'strNm': '점',
        }
        json_string = requests.get(json_url, data = data).text
        data_list = json.loads(json_string)
        entity_list = data_list['data']
        store_list = []
        for i in range(len(entity_list)):
            name = "본도시락"
            branch = entity_list[i]['strNm'].replace(" ", "").rstrip().lstrip().replace("본도시락", "").replace("(구)","")
            addr = entity_list[i]['addr']
            tell = entity_list[i]['telRep']
            xcord = entity_list[i]['lng']
            ycord = entity_list[i]['lat']
            store_list.append({"name": name, "branch": branch, "addr": addr, "tell": tell,'xcord':xcord,'ycord':ycord})
        return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
