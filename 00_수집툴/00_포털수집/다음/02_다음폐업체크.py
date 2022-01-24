import requests
import json
import codecs
import sys
def main():

    outfile = codecs.open('다음폐업확인결과.txt', 'w', 'utf-8')
    outfile.write("INPUTNAME|NAME|OLDADDR|NEWADDR|TELL|CAT|URL\n")
    inputNames = getInputName()

    for input in inputNames:

        result = getStoreInfo(input)
        print(input)
        for results in result:
            outfile.write(u'%s|' % results['inputName'])
            outfile.write(u'%s|' % results['name'])
            outfile.write(u'%s|' % results['oldaddr'])
            outfile.write(u'%s|' % results['newaddr'])
            outfile.write(u'%s|' % results['tell'])
            outfile.write(u'%s|' % results['cat'])
            outfile.write(u'%s\n' % results['url'])
        # time.sleep(random.uniform(2,3))
    outfile.close()

def getInputName():
    with open('폐업check리스트.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    return SearchList

def getStoreInfo(searchName):
    url = 'https://search.map.kakao.com/mapsearch/map.daum'
    headers = {
        'Referer': 'https://map.kakao.com/', # Referer 헤더값 없으면 호출 요청 에러
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }
    data = {
        'callback': 'jQuery181018657064011065705_1634690332690',
        'msFlag': 'A',
        'sort': '0'
    }
    data['q'] =searchName
    result = []
    try:
        urlopen = requests.get(url ,params = data, headers = headers).text
    except:
        print('Error calling the API')
    try:
        ss = urlopen.replace('/**/jQuery181018657064011065705_1634690332690(','').replace(');','')
        response = json.loads(ss)
    except :
        result.append({'inputName': searchName, 'name': '찾을 수 없음', 'oldaddr': '', 'newaddr': '', 'tell': '', 'cat': '','url': ''})
    data_info = response['place'][0]
    name = data_info['name']
    oldaddr = data_info['address']
    newaddr = data_info['new_address']
    tell = data_info['tel']
    cat = data_info['cate_name_depth1']+'/'+data_info['cate_name_depth2']+'/'+data_info['cate_name_depth3']+'/'+data_info['cate_name_depth4']
    url = data_info['homepage']
    if url == 'https://search.map.daum.net/mapsearch/map.daum' : url = ''
    result.append({'inputName':searchName, 'name':name, 'oldaddr':oldaddr, 'newaddr':newaddr,'tell':tell,'cat':cat,'url':url})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()