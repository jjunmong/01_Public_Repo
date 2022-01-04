import bs4
import requests
import codecs
import json

def main():
    outfile = codecs.open('수집결과\\35_CU.txt', 'w', 'utf-8')
    dict_keys1 = getStoreInfo()[1]
    dict_keys2 = str(dict_keys1).replace('dict_keys','').replace('[','').replace(']','').replace('(','').replace(')','').replace(',','|').replace("'","").replace(' ','')
    outfile.write("%s\n" % dict_keys2)

    key_list = []
    for key in dict_keys1:
        key_list.append(key)

    store_list = getStoreInfo()[0]
    for store in store_list:
        column_num = 0
        while True:
            if column_num == len(key_list) : break
            elif column_num == len(key_list)-1 :
                outfile.write(u'%s\n' % store['%s' % key_list[column_num]])
            else:
                outfile.write(u'%s|' % store['%s' % key_list[column_num]])
            column_num +=1
    outfile.close()

def getStoreInfo():
    url = 'http://121.140.152.151:8003/BgfRestApi/jc/jcmd.do?method=selStoreInfo'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': '121.140.152.151:8003',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    jsonString = json.loads(pageString)
    storeList = jsonString['data']
    data = []
    dict_key=''
    for info in storeList:
        TEL_NO = info['TEL_NO']
        COFFEE = info['COFFEE']
        LNG = info['LNG']
        RESERVATION = info['RESERVATION']
        POST = info['POST']
        FRIED_FOOD = info['FRIED_FOOD']
        DELIVERY =info['DELIVERY']
        POS_ATM=info['POS_ATM']
        TOTO=info['TOTO']
        WINE_SHOP=info['WINE_SHOP']
        MEDICAL_SUPPLIES=info['MEDICAL_SUPPLIES']
        WALKING_PICKUP=info['WALKING_PICKUP']
        STORE_CD=info['STORE_CD']
        BATTERY=info['BATTERY']
        PRE_STORE_CD=info['PRE_STORE_CD']
        PRINTER=info['PRINTER']
        ROAD_ADDRESS=info['ROAD_ADDRESS']
        BAKERY=info['BAKERY']
        CAR_PICKUP=info['CAR_PICKUP']
        ADDRESS=info['ADDRESS']
        HOUR24=info['HOUR24']
        LOTTO=info['LOTTO']
        ATM=info['ATM']
        TIME_DISCOUNT=info['TIME_DISCOUNT']
        STORE_NM=info['STORE_NM']
        LAT=info['LAT']
        data_dict={'TEL_NO':TEL_NO,'COFFEE':COFFEE,'LNG':LNG,'RESERVATION':RESERVATION,'POST':POST,'FRIED_FOOD':FRIED_FOOD,'DELIVERY':DELIVERY,'POS_ATM':POS_ATM,
                   'TOTO':TOTO,'WINE_SHOP':WINE_SHOP,'MEDICAL_SUPPLIES':MEDICAL_SUPPLIES,'WALKING_PICKUP':WALKING_PICKUP,'STORE_CD':STORE_CD,'BATTERY':BATTERY,
                   'PRE_STORE_CD':PRE_STORE_CD,'PRINTER':PRINTER,'ROAD_ADDRESS':ROAD_ADDRESS,'BAKERY':BAKERY,'CAR_PICKUP':CAR_PICKUP,'ADDRESS':ADDRESS,'HOUR24':HOUR24,
                   'LOTTO':LOTTO,'ATM':ATM,'TIME_DISCOUNT':TIME_DISCOUNT,'STORE_NM':STORE_NM,'LAT':LAT}
        dict_key = data_dict.keys()
        data.append(data_dict)
    return data, dict_key

main()