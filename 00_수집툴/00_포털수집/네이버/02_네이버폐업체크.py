import codecs
import requests
import json
import sys

def main():

    outfile = codecs.open('네이버폐업확인결과.txt', 'w', 'utf-8')
    outfile.write("INPUTNAME|ID|NAME|OLDADDR|NEWADDR|TELL|CAT|XCORD|YCORD|URL\n")
    inputNames = getInputName()

    for input in inputNames:
        result = getStoreInfo(input)
        print(input)
        for results in result:
            outfile.write(u'%s|' % results['input'])
            outfile.write(u'%s|' % results['id'])
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
        lines2 = data.read().splitlines()
    inputName = lines2
    return inputName

def getStoreInfo(inputName):
    url ="https://map.naver.com/v5/api/search?caller=pcweb&query={}&type=all&searchCoord=127.10515475393677;37.50626&page=1&displayCount=300&isPlaceRecommendationReplace=true&lang=ko".format(inputName)
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'hide_intro_popup=true; NNB=VD5X4T5BDQQV4; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; _ga_4BKHBFKFK0=GS1.1.1580361926.2.1.1580361933.53; NID_AUT=6bqnglBl8K/JJM6ur+M6ylopCBabrGxNigGBE/cGfB84laPNz/wCgDxKygLfROG1; NID_JKL=7lAjKUH8tn2Mp97fW7sP6sCIO/RhU2roc/0b7kLeoco=; ASID=70a9214300000171a09755f300000052; NDARK=Y; MM_NEW=1; NFS=2; MM_NOW_COACH=1; _ga=GA1.1.596751893.1580201194; _ga_7VKFYR6RV1=GS1.1.1606871504.2.1.1606871547.17; nx_ssl=2; csrf_token=24470772533adf50377c7bbfdca6718d369ff68719c2f1d16301e5b95888b7a1cd86b5ff2c1da308609d23797dbc8a04dd788b4c15876785adfb85ca9615e7e5; BMR=s=1611878705093&r=https%3A%2F%2Fm.post.naver.com%2Fviewer%2FpostView.nhn%3FvolumeNo%3D30586710%26memberNo%3D45635427&r2=https%3A%2F%2Fsports.news.naver.com%2Fwfootball%2Findex.nhn; NID_SES=AAABp4u7WEXYdi0N9uEUoHrT/mznRf2J3kJ6z9MxHuLaVA6kcXrwgwLsptIvaS3PvdACcxxRypjJP7fuRoppJ0DV4COzx4YtKnJR2SazxfVvQze6PQeWCbcis6JH4TbnLEhYR2qp/Yxutcuy20jw161DkfZOralYbbdsknsxIMEqcbys+XjxmDmwtKgprYboqD4mD4sztpxIEmsHpXH1f8W3kqw5R1usVDqrkFNu5Ur6RkR9/OZx/yuwcn0RhQZTdwGM/SR4Uv+xa3D+BwXemh0ijE6qec6e7QoDVbI9hWMpkglOLGLrjeFQ0uzSbFMJ9MCN06GW8mTxa+3NGzcwxAIBjrSKtCFsp1pYNP9X/DnH+VPqEGWg/mupj0P8ouFA6BfwE9DIs0uvcn9IYWjo9gybZ3U8r1V0d7NBG9NAuXdvLmOOHUwDCTesB3Upr68GSBzBeFnCnYerJ2XXAzzjpWEa4qpoeRiRhryAZmX1tmwihvEDm8AJB9RXSju4XidoHFL84SqZHMkMit2YnhV+A2CAFUXF+TtVyWG5DMQwMlYHnSfWR0Dr1y5NELXzaXbsj3+JqA==; page_uid=0164907f-004f-461d-aeea-073d596ac7cc',
        'expires': 'Sat, 01 Jan 2000 00:00:00 GMT',
        'pragma': 'no-cache',
        'referer': 'https://map.naver.com/',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    }
    req = requests.get(url, headers = headers).text
    list = []
    try:
        data = json.loads(req)
        data_all = data['result']['place']['list'][0]
        print(data_all)
    except :
        list.append({"input": inputName, "id": '찾을수없음', "name": '', "oldaddr": '', "newaddr": '', "tell": '',
                     "cat": '', "xcord": '', "ycord": '', "url": ''})
    else:
        try: id = data_all['id']
        except : id = ''
        try: name = data_all['name']
        except : name = ''
        try: oldaddr = data_all['address']
        except : oldaddr = ''
        try: newaddr = data_all['roadAddress']
        except : newaddr = ''
        try : tell = data_all['tel']
        except : tell = ''
        try: cat = data_all['category']
        except : cat = ''
        try:xcord = data_all['x']
        except:xcord = ''
        try: ycord = data_all['y']
        except :ycord = ''
        try : url = data_all['homePage']
        except : url = ''
        try : car_ent =  data_all['entranceCoords']['car']
        except : car_ent = ''
        try: walk_ent = data_all['entranceCoords']['walk']
        except : walk_ent = ''
        try: menu = data_all['menuInfo']
        except: menu = ''
        try :time = data_all['bizhourInfo']
        except : time = ''
        list.append({"input":inputName,"id":id,"name":name,"oldaddr":oldaddr,"newaddr":newaddr,"tell":tell,"cat":cat,"xcord":xcord,"ycord":ycord,"url":url})
    return list

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
