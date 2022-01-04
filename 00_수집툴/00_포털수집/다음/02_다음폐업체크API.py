import requests
import json
import codecs

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
    url = 'https://search.map.daum.net/mapsearch/map.daum'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'HM_CU=5BeqkwBaldY; SLEVEL=1; webid=6452e45117e04f0e916f6cf1906b22ef; PROF=0603012032024064024192UiQPJk7X-6w0mlxoempuua9xJx.tnadvun2eF_6hqavgKuZP3z7wEl2bxriNh5SdkQ00LYYSA9A1_cGNLCyhCzrwOgyiAbNDcmXxh2w41oSjfO2GJnBHNMEzaCuyn1ZLzpPZfIauQlo8OTLcCscrxJX8Uw00cFQ7_86aN.l6LmAlEdKYTrNoXVAnUnIqjfmWiGn9LMSj__Chfu5NCxD-RP63Y8_4QeFwveJ.YJ-o23ZpZSEfwRRkij-5YpUmK.5nNr4F5h3BPoofgFROPsnmMheLHsjhK_QNysMOO5LC7gOE7gjwahEqlf86C9kHSiOjHiFBz3YHhFPgUmDWuuAxeTCDTaWa; ALCT=HH33WvWcJggxzQBo8emmuh-wSev7WY8LEJr1Twu9c_E; AGEN=7vEWAnOLmC89qzSrLrHaGAam8GIgivb5M_Z4_u-7R3Q; TIARA=Vlp9XTDCvTRwmyxWLS1W3-PX.QWSta5qN-w.x8gjPI_HLh8t6YGdgXb.eFybv.FGbwQVcRSMc5KkZ.HqR3MT-LP57pyMbZA1; webid_sync=1579047407478; TS=1579047670; HTS=niSZIMK5poWkKjGKhiofYw00; ALID=tGtJj7PfjX_-V0V3pCeOrWzsp9IJGZYSQxkSlD82kA8_gISEDEnIN5oszMeiixP2w999UI; LSID=9f9765d8-9e81-487e-827f-566e07bbfdc41579047670122; ssab=',
        'Host': 'search.map.daum.net',
        'Referer': 'https://map.kakao.com/',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }
    data = {
        'callback': 'jQuery18106614589704115768_1579047502403',
        'msFlag': 'A',
        'sort': '0',
    }
    data['q'] = searchName
    result = []
    try:
        urlopen = requests.post(url, data=data, headers=headers).text
        pageString = urlopen.replace('jQuery18106614589704115768_1579047502403 (', '').replace('(', '').replace(')', '')
        response = json.loads(pageString)
        data_info = response['place'][0]
    except : result.append({'inputName':searchName, 'name':'찾을수없음', 'oldaddr':'', 'newaddr':'','tell':'','cat':'','url':''})
    else:
        name = data_info['name']
        oldaddr = data_info['address']
        newaddr = data_info['new_address']
        tell = data_info['tel']
        cat = data_info['cate_name_depth1']+'/'+data_info['cate_name_depth2']+'/'+data_info['cate_name_depth3']+'/'+data_info['cate_name_depth4']
        url = data_info['homepage']
        if url == 'https://search.map.daum.net/mapsearch/map.daum' : url = ''
        result.append({'inputName':searchName, 'name':name, 'oldaddr':oldaddr, 'newaddr':newaddr,'tell':tell,'cat':cat,'url':url})
    return result

main()