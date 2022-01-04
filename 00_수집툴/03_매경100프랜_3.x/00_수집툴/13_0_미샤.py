import requests
import codecs
import sys
import json

def main():

    outfile=codecs.open('13_미샤.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    page = 1
    while True:
        store_list = getStoreInfo(page)
        print(page)
        if store_list == [] : break
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['xcord'])
            outfile.write(u'%s\n' % store['ycord'])
        page += 1
    outfile.close()

def getStoreInfo(intPageNo):
    url = "https://www.mynunc.com/vender/shop/search-shop-list"
    data = {
        'areaMainCd': '',
        'areaCd': '',
        'shopBrndCd': '',
        'shopNm': '',
        # 'pageNum': '2',
    }
    data['pageNum'] = intPageNo
    pageString = requests.post(url, data = data).text
    jsonstring = json.loads(pageString)
    entitylist = jsonstring['content']
    result = []
    for info in entitylist:
        try:
            name = info['shopBrndNm']
            branch = info['shopNm']
            addr = info['baseAddr']
            tell = info['telNo']
            xcord = info['lon']
            ycord = info['lat']
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()



