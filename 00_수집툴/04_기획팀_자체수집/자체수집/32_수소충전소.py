import codecs
import requests
import bs4
import json

def main():
    outfile = codecs.open('32_사단법인한국수소연합회.txt', 'w', 'utf-8')
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
    url ='http://www.h2.or.kr/map.html?query=list&page={}&table=LimBo&botype=LIS_B04_01&page_num=10'.format(intPageNo)
    response = requests.get(url)
    bsObj = bs4.BeautifulSoup(response.content,'html.parser')
    item = bsObj.find_all('tr')
    data = []
    dict_key = ''
    for info in item:
        try:num = str(info.select('td')[0]).replace('<td>','').replace('</td>','')
        except: num= ''
        try:region = str(info.select('td')[1]).replace('<td>','').replace('</td>','')
        except: region= ''
        try:name = str(info.select('td')[2]).replace('<td>','').replace('</td>','')
        except:name = ''
        try:addr = str(info.select('td')[3]).replace('<td>','').replace('</td>','')
        except: addr= ''
        try:price = str(info.select('td')[4]).replace('<td>','').replace('</td>','')
        except: price= ''
        try:payment = str(info.select('td')[5]).replace('<td>','').replace('</td>','')
        except:payment= ''
        try:time = str(info.select('td')[6]).replace('<td>','').replace('</td>','')
        except: time= ''
        try:tell = str(info.select('td')[7]).replace('<td class="rl_no">','').replace('</td>','')
        except: tell= ''
        if num == '' or len(num) > 10 : pass
        else:
            data_dict = {'num':num,'region':region,'name':name,'addr':addr,'price':price,'payment':payment,'time':time,'tell':tell}
            dict_key = data_dict.keys()
            data.append(data_dict)
    return data, dict_key


def main2():
    outfile = codecs.open('32_수소충전소위치정보시스템.txt', 'w', 'utf-8')
    dict_keys1 = getStoreInfo2()[1]
    dict_keys2 = str(dict_keys1).replace('dict_keys','').replace('[','').replace(']','').replace('(','').replace(')','').replace(',','|').replace("'","").replace(' ','')
    outfile.write("%s\n" % dict_keys2)

    key_list = []
    for key in dict_keys1:
        key_list.append(key)

    store_list = getStoreInfo2()[0]
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

def getStoreInfo2():
    url ='http://gis.h2korea.or.kr/cmm/api/get/detail.do'
    data = {
        'aaa':1
    }
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '11',
        'Content-Type': 'application/json',
        'Cookie': 'JSESSIONID=DA87E91D9E18E2FA3ABD42133D77297F',
        'h2k-api-key': 'null',
        'Host': 'gis.h2korea.or.kr',
        'Origin': 'http://gis.h2korea.or.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://gis.h2korea.or.kr/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.post(url, json.dumps(data), headers = headers).text
    jsonString = json.loads(response)
    item = jsonString['list']
    data = []
    dict_key = ''
    for info in item:
        avgVhcCnt = info['avgVhcCnt']
        chrgeAmt = info['chrgeAmt']
        chrgeCde = info['chrgeCde']
        chrgeCdeNm = info['chrgeCdeNm']
        firstIndex = info['firstIndex']
        geomX = info['geomX']
        geomY = info['geomY']
        group = info['group']
        hasPhoto = info['hasPhoto']
        hystnAddr = info['hystnAddr']
        hystnAdrDtl = info['hystnAdrDtl']
        hystnNm = info['hystnNm']
        hystnSn = info['hystnSn']
        hystnTel = info['hystnTel']
        keyword = info['keyword']
        lastIndex = info['lastIndex']
        legdCde = info['legdCde']
        operStt = info['operStt']
        operSttNm = info['operSttNm']
        operTmDtl = str(info['operTmDtl']).replace('\r','').replace('\n','')
        operTmGbn = str(info['operTmGbn']).replace('\r','').replace('\n','')
        pageIndex = info['pageIndex']
        pageSize = info['pageSize']
        pageUnit = info['pageUnit']
        paginationInfo = info['paginationInfo']
        payMthd = info['payMthd']
        payMthdNm = info['payMthdNm']
        recordCountPerPage = info['recordCountPerPage']
        remark = str(info['remark']).replace('\r','').replace('\n','')
        rnCde = info['rnCde']
        rowNum = info['rowNum']
        rownum = info['rownum']
        sessionUserId = info['sessionUserId']
        status = info['status']
        totalRecordCount = info['totalRecordCount']
        type = info['type']
        wkndStt = info['wkndStt']
        wkndSttNm = info['wkndSttNm']
        _act = info['_act']
        data_dict = {'avgVhcCnt':avgVhcCnt,'chrgeAmt':chrgeAmt,'chrgeCde':chrgeCde,'chrgeCdeNm':chrgeCdeNm,'firstIndex':firstIndex,'geomX':geomX,
                     'geomY':geomY,'group':group,'hasPhoto':hasPhoto,'hystnAddr':hystnAddr,'hystnAdrDtl':hystnAdrDtl,'hystnNm':hystnNm,'hystnSn':hystnSn,
                     'hystnTel':hystnTel,'keyword':keyword,'lastIndex':lastIndex,'legdCde':legdCde,'operStt':operStt,'operSttNm':operSttNm,'operTmDtl':operTmDtl,
                     'operTmGbn':operTmGbn,'pageIndex':pageIndex,'pageSize':pageSize,'pageUnit':pageUnit,'paginationInfo':paginationInfo,'payMthd':payMthd,
                     'payMthdNm':payMthdNm,'recordCountPerPage':recordCountPerPage,'remark':remark,'rnCde':rnCde,'rowNum':rowNum,'rownum':rownum,'sessionUserId':sessionUserId,
                     'status':status,'totalRecordCount':totalRecordCount,'type':type,'wkndStt':wkndStt,'wkndSttNm':wkndSttNm,'_act':_act}
        dict_key = data_dict.keys()
        data.append(data_dict)
    return data, dict_key

main()
main2()
