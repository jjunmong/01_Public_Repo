import codecs
import bs4
import time
import requests
import json
import sys

def main():
    outfile = codecs.open('10_KIAMOTORS.txt', 'w', 'utf-8')
    outfile.write("##NAME|BRANCH|ADDR|XCORD|YCORD|TELL\n")
    result = []
    for infos in range(0, 80):
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
    url = "https://www.kia.com/api/kia_korea/base/br01/branchInfo.selectBranchInfoList?pageNum={}&sc.searchKey%5B2%5D=&sc.searchType%5B2%5D=all&sortKey%5B0%5D=typeSort&sortKey%5B1%5D=branchNm&sortType%5B0%5D=A&sortType%5B1%5D=A".format(pageNo)
    jsonData = requests.get(url)
    req = jsonData.text
    print(req)
    response = json.loads(req)
    # print(response)
    list = []
    try:
        dataAll = response['dataInfo']
        print(dataAll)
    except KeyError:
        pass
    else:
        for listinfo in dataAll:
            name = '기아모터스'
            branch1 = listinfo['branchNm']
            branch2 = "지점"
            branch = branch1+branch2
            addr = listinfo['addr']
            xCord = listinfo['lng']
            yCord = listinfo['lat']
            tell = listinfo['tel']
            list.append ({"name":name, "branch":branch,"addr":addr,"xcord":xCord,"ycord":yCord,"tell":tell})
    return list
def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
