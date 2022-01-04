import json
import sys
import time
import codecs
import requests
import random
import bs4

def main():

    outfile = codecs.open('16_홈플러스정보(휴무일).txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|CLOSE_DATE|CLOSE_INFO\n")

    url_list = getUrl()
    for ss in url_list:
        print(ss)
    for url in url_list:
        store_List = getInfo(url)
        for store in store_List:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s|' % store['tell'])
            outfile.write(u'%s|' % store['close_date'])
            outfile.write(u'%s\n' % store['close_info'])

    time.sleep(random.uniform(0.3,0.6))
    outfile.close()

def getUrl():
    url = 'https://corporate.homeplus.co.kr/store/hypermarket.aspx?ctl00%24ContentPlaceHolder1%24Region_Code=&ctl00%24ContentPlaceHolder1%24srch_name=&ctl00%24ContentPlaceHolder1%24Button1=&ctl00%24ContentPlaceHolder1%24storetype1=on'
    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '',
        'ctl00$ContentPlaceHolder1$Region_Code': '',
        'ctl00$ContentPlaceHolder1$srch_name': '',
        'ctl00$ContentPlaceHolder1$Button1': '',
        'ctl00$ContentPlaceHolder1$storetype1': 'on',
        'ctl00$ContentPlaceHolder1$storetype2': 'on',
        'ctl00$ContentPlaceHolder1$storetype3': 'on',
    }
    htmlString = requests.post(url, data = data).text
    print(url)
    html = bs4.BeautifulSoup(htmlString, "html.parser")
    # ul = html.find('ul',{"class":"result_list"})
    li = html.find_all('li',{"class":"clearfix"})
    print(len(li))
    data= []
    for list in li:
        default_url = 'http://corporate.homeplus.co.kr'
        detail_url = list.find('a')['href']
        detail_url2 = str(detail_url)
        url = default_url+detail_url2
        data.append(url)
    return data

def getInfo(url):
    url = url
    htmlString = requests.get(url).text
    print(url)
    html = bs4.BeautifulSoup(htmlString, "html.parser")
    data =[]
    try :
        if url[-7:] == 'EXPRESS' :
            name = "홈플러스 익스프레스"
            branch = html.find("span",{"class":"name"}).text.replace('\r','').replace('\n','').replace('\t','').replace(' ','').upper().rstrip().lstrip()
            addr = html.select('#store_detail01 > table > tbody > tr:nth-child(1) > td')[0].text.upper().rstrip().lstrip()
            tell = html.select('#store_detail01 > table > tbody > tr:nth-child(3) > td')[0].text.upper().rstrip().lstrip()
            close_date = html.select('#store_detail01 > table > tbody > tr:nth-child(2) > td')[0].text.replace('\r','').replace('\n','').replace('\t','').replace('\xa0','').upper().rstrip().lstrip()
            close_info = html.select('#store_detail01 > table > tbody > tr:nth-child(4) > td')[0].text.replace('\r','').replace('\n','').replace('\t','').upper().rstrip().lstrip()
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"close_date":close_date,"close_info":close_info})
        elif url[-8:] == 'HOMEPLUS' :
            name = "홈플러스"
            branch = html.find("span",{"class":"name"}).text.replace('\r','').replace('\n','').replace('\t','').replace(' ','').upper().rstrip().lstrip()
            addr = html.select('#store_detail01 > table > tbody > tr:nth-child(1) > td')[0].text.upper().rstrip().lstrip()
            tell = html.select('#store_detail01 > table > tbody > tr:nth-child(3) > td')[0].text.upper().rstrip().lstrip()
            close_date = html.select('#store_detail01 > table > tbody > tr:nth-child(2) > td')[0].text.replace('\r','').replace('\n','').replace('\t','').replace('\xa0','').upper().rstrip().lstrip()
            close_info = html.select('#store_detail01 > table > tbody > tr:nth-child(4) > td')[0].text.replace('\r','').replace('\n','').replace('\t','').upper().rstrip().lstrip()
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"close_date":close_date,"close_info":close_info})
        elif url[-7:] == '365PLUS' :
            name = "홈플러스 365PLUS"
            branch = html.select('#content > div > div > div > div.store_detail > div > table > tbody > tr:nth-child(1) > td')[0].text.replace('\r','').replace('\n','').replace('\t','').replace(' ','').upper().rstrip().lstrip()
            addr = html.select('#content > div > div > div > div.store_detail > div > table > tbody > tr:nth-child(2) > td')[0].text.upper().rstrip().lstrip()
            data.append({"name":name,"branch":branch,"addr":addr,"tell":None,"close_date":None,"close_info":None})
    except :
        data.append({"name": "홈페이지의잘못된URL","branch":url,"addr":None,"tell":None,"close_date":None,"close_info":None})
    return data
main()