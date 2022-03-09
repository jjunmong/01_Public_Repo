import bs4
import requests
import codecs
from datetime import datetime
import codecs
from datetime import datetime
import traceback
import os, sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\21_1_도공_화물차라운지\\') == False : os.makedirs('수집결과\\21_1_도공_화물차라운지\\')
outfilename = '수집결과\\21_1_도공_화물차라운지\\도공_화물차라운지_{}.txt'.format(today)
outfilename_true = '수집결과\\21_1_도공_화물차라운지\\도공_화물차라운지_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\21_1_도공_화물차라운지\\도공_화물차라운지_{}.log_실패.txt'.format(today)

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
    dict_keys1 = getStoreInfo('001')[1]
    dict_keys2 = str(dict_keys1).replace('dict_keys','').replace('[','').replace(']','').replace('(','').replace(')','').replace(',','|').replace("'","").replace(' ','')
    outfile.write("%s\n" % dict_keys2)

    key_list = []
    for key in dict_keys1:
        key_list.append(key)

    id_list = route_name()
    for id in id_list:
        print(id)
        store_list = getStoreInfo(id)[0]
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

def route_name():
    url = 'https://www.ex.co.kr/portal/usefee/selectZoneHugae2.do'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    list = bsObj.find('select',{"id":"searchKeyword2"})
    list_all = list.find_all('option')
    result = []
    for info in list_all:
        route_nm = info.text
        route_id = str(info['value'])
        if route_id  == '' : pass
        else : result.append(route_id)
    return result

def getStoreInfo(route_id):
    url = 'https://www.ex.co.kr/portal/usefee/selectZoneHugae2.do'
    data={}
    data['searchKeyword2'] = route_id
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    pageString = requests.post(url,data =data, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbdoy= bsObj.find('tbody')
    tr = tbdoy.find_all('tr')
    data = []
    dict_key = ''
    for info in tr:
        try:
            name = info.find('a').text.replace('\r','').replace('\n','').replace('\t','')
            tell = info.find('td',{"class":"cen"}).text
            rest_convenient = []
            td = info.select('td')[1]
            li = td.find_all('li')
            for s in li:
                text = s.text
                rest_convenient.append(text)

            station_convenient = []
            td = info.select('td')[2]
            li = td.find_all('li')
            for s in li:
                text = s.text
                station_convenient.append(text)

            wash = info.select('td')[4]
            wash = wash.text
            repair = info.select('td')[5]
            repair = repair.text
            truck_rounge = info.select('td')[6]
            truck_rounge = truck_rounge.text
            data_dict={'name':name,'tell':tell,'rest_convenient':rest_convenient,'station_convenient':station_convenient,'wash':wash,'repair':repair,'truck_rounge':truck_rounge}
            dict_key = data_dict.keys()
            data.append(data_dict)
        except : pass
    return data, dict_key

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()