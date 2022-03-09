import requests
import codecs
import bs4
import sys

def main():
    outfile = codecs.open('11_MacDO.txt', 'w', 'utf-8')
    outfile.write("##NAME|BRANCH|OLD_ADDR|NEW_ADDR|TELL|HOUR|ㅇ|DELIVERY|MORNING|SIGNATURE|PARK\n")
    result = []

    for number in range(1, 99):
        result = result + getInfo(number)
    for ssd in result:
        print(ssd)
    for results in result:
        outfile.write(u'%s|' % results['name'])
        outfile.write(u'%s|' % results['branch'])
        outfile.write(u'%s|' % results['old_addr'])
        outfile.write(u'%s|' % results['new_addr'])
        outfile.write(u'%s|' % results['tell'])
        outfile.write(u'%s|' % results['hour'])
        outfile.write(u'%s|' % results['drive'])
        outfile.write(u'%s|' % results['delivery'])
        outfile.write(u'%s|' % results['morning'])
        outfile.write(u'%s|' % results['signature'])
        outfile.write(u'%s|\n' % results['park'])
    outfile.close()


def getInfo(pageNo):
    url = 'https://www.mcdonalds.co.kr/kor/store/list.do'
    data  ={
     'lat':'NO',
     'lng':'NO',
     'searchWord':'',
    }
    data['page'] = pageNo
    res = requests.post(url , data = data).text
    bsObj = bs4.BeautifulSoup(res,"html.parser")
    # list_all = bsObj.find_all("div",{"class":"storeResult"})
    list_all = bsObj.find_all("tr")
    dataAll = []
    print(list_all)
    for ss in list_all:
        try:
            name = "맥도날드"
            branch = ss.find("a").text.rstrip().lstrip().upper().replace(" ","")
            old_addr = ss.find("dd").text.rstrip().lstrip().upper()
            new_addr = ss.find("dd",{"class":"road"}).text.rstrip().lstrip().upper()
            tell = ss.select("td")[1].text.rstrip().lstrip().upper()
            try :
                hour =  ss.find("span",{"class":"srvc1"}).text.rstrip().lstrip().upper()
            except :
                hour = ''
            try:
                drive = ss.find("span", {"class": "srvc2"}).text.rstrip().lstrip().upper()
            except:
                drive = ''
            try:
                delivery = ss.find("span", {"class": "srvc3"}).text.rstrip().lstrip().upper()
            except:
                delivery = ''
            try:
                morning = ss.find("span", {"class": "srvc4"}).text.rstrip().lstrip().upper()
            except:
                morning = ''
            try:
                signature = ss.find("span", {"class": "srvc5"}).text.rstrip().lstrip().upper()
            except :
                signature = ''
            try:
                park = ss.find("span", {"class": "srvc6"}).text.rstrip().lstrip().upper()
            except :
                park = ''
        except :
            pass
        else:
            dataAll.append({"name": name, "branch": branch, "old_addr": old_addr,"new_addr": new_addr, "tell": tell, "hour": hour,"drive":drive,"delivery":delivery,"morning":morning,"signature":signature,"park":park})
    return dataAll

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()