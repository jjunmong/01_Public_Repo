import json
import requests
import codecs
from datetime import datetime
import traceback
import os, sys

today = str(datetime.today()).split(' ')[0].replace('-', '')
if os.path.exists('수집결과\\07_4_하이파킹\\') == False : os.makedirs('수집결과\\07_4_하이파킹\\')
outfilename = '수집결과\\07_4_하이파킹\\하이파킹_{}.txt'.format(today)
outfilename_true = '수집결과\\07_4_하이파킹\\하이파킹_{}.log_성공.txt'.format(today)
outfilename_false = '수집결과\\07_4_하이파킹\\하이파킹_{}.log_실패.txt'.format(today)

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
    url = 'http://pestore.hiparking.co.kr:33333/api/v1/park/list'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    pageString = requests.get(url, headers = headers).text
    jsosnString = json.loads(pageString)
    data = []
    dict_key = ''
    for info in jsosnString:
            nm = info['nm']
            addr = info['addr']
            tel =['tel']
            lat = info['lat']
            lon = info['lon']
            data_dict={'nm':nm,'tel':tel,'addr':addr,'lat':lat,'lon':lon}
            dict_key = data_dict.keys()
            data.append(data_dict)
    return data, dict_key

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()