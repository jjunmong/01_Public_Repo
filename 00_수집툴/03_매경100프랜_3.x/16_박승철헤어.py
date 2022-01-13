import json
from urllib.request import urlopen
import codecs
import bs4
import sys

def main():
    outfile=codecs.open('16_박승철헤어.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s\n' % store['tell'])
    outfile.close()

def getStoreInfo():
    url = 'http://m.pschair.co.kr/apis/store.search.list.asp?addr=&addr1=&addr2=&mode=L'
    req = urlopen(url)
    response = req.read()
    response_json = json.loads(response)
    entity_list = response_json['result']
    store_list = []
    for i in range(len(entity_list)):
        name ="박승철헤어"
        branch = entity_list[i]['name'].replace(" ","").rstrip().lstrip()
        addr = entity_list[i]['addr1']
        tell = entity_list[i]['tel']
        store_list.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return store_list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()