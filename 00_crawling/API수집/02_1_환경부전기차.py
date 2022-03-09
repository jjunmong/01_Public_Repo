import bs4
import codecs
import requests
from datetime import datetime
import traceback
import os,sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\02_1_환경부EVC\\') == False : os.makedirs('수집결과\\02_1_환경부EVC\\')
outfilename = '수집결과\\02_1_환경부EVC\\환경부EVC_{}.txt'.format(today)
outfilename_true = '수집결과\\02_1_환경부EVC\\환경부EVC_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\02_1_환경부EVC\\환경부EVC_{}.log_실패.txt'.format(today)

def main():
    try:
        Crawl_run()
        outfile = codecs.open(outfilename_true, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '정상 수집 완료'
        outfile.write(write_text)
        outfile.close()
    except:
        if os.path.isfile(outfilename_true):
            os.remove(outfilename_true)
        outfile = codecs.open(outfilename_false, 'w', 'utf-8')
        write_text = str(datetime.today()) + '|' + '수집 실패' + '|' + str(traceback.format_exc())
        outfile.write(write_text)
        outfile.close()

def Crawl_run():
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    dict_keys1 = getStoreInfo(1)[1]
    dict_keys2 = str(dict_keys1).replace('dict_keys','').replace('[','').replace(']','').replace('(','').replace(')','').replace(',','|').replace("'","").replace(' ','')
    outfile.write("%s\n" % dict_keys2)

    key_list = []
    for key in dict_keys1:
        key_list.append(key)
    page = 1
    while True:
        store_list = getStoreInfo(page)[0]
        if store_list == [] : break
        print(page)
        for store in store_list:
            column_num = 0
            while True:
                if column_num == len(key_list) : break
                elif column_num == len(key_list)-1 :
                    outfile.write(u'%s\n' % store['%s' % key_list[column_num]])
                else:
                    outfile.write(u'%s|' % store['%s' % key_list[column_num]])
                column_num +=1
        page +=1
    outfile.close()

def getStoreInfo(intPageNo):
    url ='http://apis.data.go.kr/B552584/EvCharger/getChargerInfo?serviceKey=iA3RAOtRS80EKLLIXMNtk1I5m5CXRV3DzdRN1FTCKkFnK%2FWBP45sUYwPQMwQ0wuA3gVuP%2FAMvKtrbnvp2a%2BYkw%3D%3D&numOfRows=1000&pageNo={}'.format(intPageNo)
    response = requests.get(url).text
    bsObj = bs4.BeautifulSoup(response,'lxml')
    item = bsObj.find_all('item')
    data = []
    dict_key = ''
    for info in item:
        try:statNm = info.find('statnm').text.strip()
        except: statNm= ''
        try:statId = info.find('statid').text.strip()
        except: statId= ''
        try:chgerId = info.find('chgerid').text.strip()
        except:chgerId = ''
        try:chgerType = info.find('chgertype').text.strip()
        except: chgerType= ''
        try:addr = info.find('addr').text.strip()
        except: addr= ''
        try:location = info.find('location').text.strip()
        except:location= ''
        try:lat = info.find('lat').text.strip()
        except: lat= ''
        try:lng = info.find('lng').text.strip()
        except: lng= ''
        try:useTime = info.find('usetime').text.strip()
        except: useTime= ''
        try:busiId = info.find('busiid').text.strip()
        except:busiId = ''
        try:bnm = info.find('bnm').text.strip()
        except: bnm= ''
        try:busiNm = info.find('businm').text.strip()
        except: busiNm= ''
        try:busiCall = info.find('busicall').text.strip()
        except: busiCall= ''
        try:stat = info.find('stat').text.strip()
        except: stat= ''
        try:statUpdDt = info.find('statupddt').text.strip()
        except: statUpdDt= ''
        try:lastTsdt = info.find('lasttsdt').text.strip()
        except: lastTsdt= ''
        try:lastTedt = info.find('lasttedt').text.strip()
        except: lastTedt= ''
        try:nowTsdt = info.find('nowtsdt').text.strip()
        except: nowTsdt= ''
        try:powerType = info.find('powertype').text.strip()
        except: powerType= ''
        try:output = info.find('output').text.strip()
        except: output= ''
        try:method = info.find('method').text.strip()
        except: method= ''
        try:zcode = info.find('zcode').text.strip()
        except: zcode= ''
        try:parkingFree = info.find('parkingfree').text.strip()
        except: parkingFree= ''
        try:note = info.find('note').text.strip()
        except: note= ''
        try:limitYn = info.find('limityn').text.strip()
        except: limitYn= ''
        try:limitDetail = info.find('limitdetail').text.strip()
        except: limitDetail= ''
        try:delYn = info.find('delyn').text.strip()
        except: delYn= ''
        try:delDetail = info.find('deldetail').text.strip()
        except: delDetail= ''
        data_dict = {'statNm':statNm,'statId':statId,'chgerId':chgerId,'chgerType':chgerType,'addr':addr,'location':location,
                     'lat':lat,'lng':lng,'useTime':useTime,'busiId':busiId,'bnm':bnm,'busiNm':busiNm,'busiCall':busiCall,
                     'stat':stat,'statUpdDt':statUpdDt,'lastTsdt':lastTsdt,'lastTedt':lastTedt,'nowTsdt':nowTsdt, 'powerType':powerType,
                     'output':output, 'method':method, 'zcode':zcode, 'parkingFree':parkingFree, 'note':note, 'limitYn':limitYn,
                     'limitDetail':limitDetail,'delYn':delYn,'delDetail':delDetail}
        dict_key = data_dict.keys()
        data.append(data_dict)
    return data, dict_key

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()