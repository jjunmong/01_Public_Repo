import requests
import bs4
import json
import codecs
import sys

def main():
    outfile = codecs.open('05_DBinsurance.txt', 'w', 'utf-8')
    outfile.write("##NAME|BRANCH|ADDR|TELL\n")
    sido_list = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "강원", "경기", "충북", "충남", "전북", "전남", "경북", "경남", "제주", "세종"]

    result = []
    for get in sido_list:
        result = result + getInfo(get)

    for ssd in result:
        print(ssd)

    for results in result:
        outfile.write(u'%s|' % results['name'])
        outfile.write(u'%s|' % results['branch'])
        outfile.write(u'%s|' % results['addr'])
        outfile.write(u'%s|\n' % results['tell'])
    outfile.close()

def getInfo(region):
    url = "https://m.idblife.com/ajaxSMOSI01101M.mvc"
    data = {
        'ORG_TYPE':'8',
        'ORGFULL':'서울'
    }
    data['ORGFULL'] = region
    req = requests.post(url, data =data).text
    print(req)
    data_all = json.loads(req)
    print(data_all)
    data_list = data_all['agency']
    datalist = []
    for list in data_list :
        name  = "DB생명"
        addr = list['ADDR_NEW'].rstrip().lstrip()
        tell = list['OTEL'].rstrip().lstrip()
        branch = list['ORGFULL'].rstrip().lstrip()
        datalist.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return datalist

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
