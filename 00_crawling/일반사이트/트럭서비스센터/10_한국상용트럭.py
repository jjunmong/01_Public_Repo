import sys
import codecs
import requests
import bs4
import random
import time
import json

def main():

    outfile = codecs.open('10_한국상용트럭.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL|XCORD|YCORD\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['branch'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])
    time.sleep(random.uniform(0.3, 0.9))

    outfile.close()

def getStoreInfo():
    url = 'https://kctruck.co.kr/%EC%98%81%EC%97%85-%EB%B0%8F-%EC%84%9C%EB%B9%84%EC%8A%A4'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko,en;q=0.9,ko-KR;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ci_userlang=korean; ci_kisession=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22f3c6186e64082e07c7ae6283e081e9a3%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%22112.169.33.67%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A114%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F86.0.4240.75+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1603068635%3B%7Db3c31aa308529bd274fead5618287361',
        'Host': 'kctruck.co.kr',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    }
    pageString = requests.get(url, headers = headers).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    div = bsObj.find_all('div',{"class":"row"})
    result = []
    for info in div :
        try:
            name = '한국상용트럭'
            branch = info.find('span',{"class":"fsize25"}).text.replace('■','').replace('(주)','').replace('\xa0','')
            if branch == '호남 판매본부-본사':pass
            if branch == '수도권 판매본부': pass
            if branch == '충청권 판매본부': pass
            if branch == '대구, 경북 판매본부': pass
            if branch == '부산, 경남판매본부': pass
            if branch == '제주지점': pass
            try:
                info2 = str(info.find('p')).split('<br/>')
                addr = str(info2[1]).replace('</p>','').replace('</strong>','').replace('<span class="fsize15">','').replace('</span>','').replace('<span class="fsize17">','').replace(',','').replace('<span class="fsize25">','').replace('\xa0','').replace('<span class="fsize15">','').replace('</span></p>','').lstrip().rstrip()
                if addr == '' :addr = str(info2[2]).replace('</p>','').replace('</strong>','').replace('</span>','').replace('<span class="fsize17">','').replace(',','').replace('<span class="fsize25">','').replace('\xa0','').replace('<span class="fsize15">','').replace('</span></p>','').lstrip().rstrip()
                tell = str(info2[0]).replace('<span class="fsize25">','').replace('<p data-edit="true" data-selector="p">','').replace('<p class="" data-edit="true" data-selector="p">','').replace('<strong>','').replace('<span class="fsize17">','').replace('</span>','').replace('</strong>','').replace('Tel.','')
            except:
                info2 = str(info.find('p').text)
                addr = info2
                if addr.startswith('연락처') == True : addr = ''
                tell = info2.replace('연락처 : ','')
            try:
                try:
                    cord = str(info.find('div',{"class":"google-map"})['data-url']).split('!3d')
                    cord2 = str(cord[1]).split('!4d')
                    xcord = cord2[1]
                    ycord = cord2[0]
                except:
                    cord = str(info.find('div', {"class": "google-map"})['data-url']).replace(".replace(',17z/data=!3m1!4b1','').","")
                    cord = cord.split('@')
                    cord2 = str(cord[1]).split(',')
                    xcord = cord2[1]
                    ycord = cord2[0]
            except:
                xcord= ''
                ycord = ''
        except: pass
        else:
            result.append({'name':name,'branch':branch,'addr':addr,'tell':tell,'xcord':xcord,'ycord':ycord})
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()

