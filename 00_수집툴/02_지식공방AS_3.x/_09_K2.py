import codecs
import bs4
import time
import requests
import json
import sys
def main():
    outfile = codecs.open('09_K2.txt', 'w', 'utf-8')
    outfile.write("##NAME|BRANCH|ADDR|XCORD|YCORD|TELL\n")
    result = []
    for infos in range(0, 60):
        result = result + carwl(infos)

    for ss in result:
        print(ss)

    for results in result:
        outfile.write(u'%s|' % results['name'])
        outfile.write(u'%s|' % results['branch'])
        outfile.write(u'%s|' % results['addr'])
        outfile.write(u'%s|' % results['xcord'])
        outfile.write(u'%s|' % results['ycord'])
        outfile.write(u'%s|\n' % results['tell'])
    outfile.close()

def carwl(pageNo):
    url = "https://www.k2.co.kr/k2/ko/customercenter/ajaxStoreInfo"
    data = {
        'address1':'',
        'address2':'',
        'searchWord':'',
        'storeType':'ALL',
        'specialZone1':'',
        'specialZone2':'',
        'specialZone3':'',
        'showMode':'',
        'rec':'10'
    }
    data['page'] = pageNo
    jsonData = requests.post(url = url , data = data)
    req = jsonData.text
    # print(req)
    response = json.loads(req)
    # print(response)
    list = []
    try:
        dataAll = response['resultObj']['shopInfoList']
        print(dataAll)
    except KeyError:
        pass
    else:
        for listinfo in dataAll:
            name = 'K2'
            branch = listinfo['displayName']
            addr = listinfo['streetName']
            xCord = listinfo['longitude']
            yCord = listinfo['latitude']
            tell = listinfo['phone1']
            list.append ({"name":name, "branch":branch,"addr":addr,"xcord":xCord,"ycord":yCord,"tell":tell})
    return list
def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
