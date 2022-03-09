import requests
import codecs
import bs4
import json
import sys

def main():
    outfile = codecs.open('12_StarBucks.txt', 'w', 'utf-8')
    outfile.write("##NAME|BRANCH|OLD_ADDR|NEW_ADDR|TELL|XCORD|YCORD\n")
    sidoCode = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17']

    result = []
    for number in sidoCode:
        result = result + getInfo(number)

    for ssd in result:
        print(ssd)

    for results in result:
        outfile.write(u'%s|' % results['name'])
        outfile.write(u'%s|' % results['branch'])
        outfile.write(u'%s|' % results['old_addr'])
        outfile.write(u'%s|' % results['new_addr'])
        outfile.write(u'%s|' % results['tell'])
        outfile.write(u'%s|' % results['xcord'])
        outfile.write(u'%s|\n' % results['ycord'])
    outfile.close()

def getInfo(sidoCode):
    url = 'https://www.istarbucks.co.kr/store/getStore.do?r=ZGXIYNMBF8' # r 이후 부분이 주기적으로 변하는 값이기에 수동으로 바꿔줘야함
    data  ={
        'in_biz_cds': '0',
        'in_scodes': '0',
        'ins_lat': '37.4931456',
        'ins_lng': '127.029248',
        'search_text': '',
        'p_gugun_cd': '',
        'isError': 'true',
        'in_distance': '0',
        'in_biz_cd': '',
        'iend': '1000',
        'searchType': 'C',
        'set_date': '',
        'rndCod': 'O8TOD0ETWK',
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '193',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=ollMwsuJefvau8SVymDCzePAcgCHpzqmhLJiuyxJUVzA9oNM4d5gDxfbaLrSKWtI.aHBfZG9tYWluL2tpd2kwOA==; _ga=GA1.3.1756256394.1589419312; _gid=GA1.3.829699011.1589419312; _gat=1; PCID=15894193117877645784073; RC_RESOLUTION=1920*1080; RC_COLOR=24; _xm_webid_1_=-762326691',
        'Host': 'www.starbucks.co.kr',
        'Origin': 'https://www.starbucks.co.kr',
        'Pragma': 'no-cache',
        'Referer': 'https://www.starbucks.co.kr/store/store_map.do',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data['p_sido_cd'] = sidoCode
    jsonData = requests.post(url, data=data, headers = headers).text
    response = json.loads(jsonData)
    list_all = response['list']
    dataAll = []
    for ss in list_all :
        try :
            name = "스타벅스"
            branch = ss['s_name'].rstrip().lstrip().upper()
            old_addr = ss['addr'].rstrip().lstrip().upper()
            new_addr = ss['doro_address'].rstrip().lstrip().upper()
            tell = ss['tel'].rstrip().lstrip().upper()
            xcord =  ss['lat'].rstrip().lstrip().upper()
            ycord = ss['lot'].rstrip().lstrip().upper()
        except AttributeError :
            pass
        except TypeError:
            pass
        else:
            dataAll.append({"name": name, "branch": branch, "old_addr": old_addr,"new_addr": new_addr, "tell": tell, "xcord": xcord, "ycord": ycord})
    return dataAll

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
