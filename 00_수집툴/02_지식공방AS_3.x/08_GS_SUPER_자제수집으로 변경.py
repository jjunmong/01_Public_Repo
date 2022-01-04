import requests
import codecs
import time
import json

outfile = codecs.open('08_GSSUPER.txt', 'w', 'utf-8')
outfile.write("##NAME|BRANCH|ADDR|TELL\n")

def getInfo(pageNo):
    url = "http://gsthefresh.gsretail.com/thefresh/ko/market-info/find-storelist?searchType=&pageNum={}&listCnt=5&pagingCnt=10&pagingNowIdx=1&totlPageNum=1&stb1=&stb2=&searchShopName=&CSRFToken=365cd65c-df4f-494e-81d7-2bc934a212c5".format(pageNo)
    req = requests.get(url).text
    data = json.loads(req)
    data_all = data['results']
    list_all = []
    for ss in data_all :
        name = "GS수퍼마켓"
        branch = ss['shopName'].replace(" ","").rstrip().lstrip().upper()
        addr = ss['address'].rstrip().lstrip()
        tell = ss['phone'].rstrip().lstrip()
        list_all.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return list_all

result = []
for num in range(1,80):
    result = result + getInfo(num)

results = set()
new_results = []
for list in result:
    lists = tuple(list.items())
    if lists not in results:
        results.add(lists)
        new_results.append(list)

for ss in new_results:
    print(ss)

for result_list in new_results:
    outfile.write(u'%s|' % result_list['name'])
    outfile.write(u'%s|' % result_list['branch'])
    outfile.write(u'%s|' % result_list['addr'])
    outfile.write(u'%s|\n' % result_list['tell'])
outfile.close()