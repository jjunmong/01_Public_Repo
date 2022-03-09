import bs4
import requests
import codecs
import sys

def main():

    outfile=codecs.open('17_다비치안경.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|ADDR|TELL\n")

    num_list = getStoreList_all()
    for idx in num_list:
        store_list = getStoreInfo(idx)
        print(idx)
        for store in store_list:
            outfile.write(u'%s|' % store['name'])
            outfile.write(u'%s|' % store['branch'])
            outfile.write(u'%s|' % store['addr'])
            outfile.write(u'%s\n' % store['tell'])
    outfile.close()

def getStoreList(intPageNo, sido):
    url = "https://www.davich.com/04_market/01_find.php"
    data = {}
    data['pg']= intPageNo
    data['sido']= sido
    pageString = requests.post(url, data = data).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    li = bsObj.find_all('li',{"class":"pay_left_s"})
    result = []
    for info in li:
        try:
            a = info.find('img')['onclick']
            a = str(a).replace("','','left=50,top=50,width=1024,height=700,scrollbars=1')",'').split('=')[1]
        except : pass
        else:
            result.append(a)
    return result

def getStoreList_all():
    sido_list = ['서울특별시', '경기', '강원', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '인천광역시', '대전광역시', '울산광역시', '광주광역시', '대구광역시', '부산광역시', '세종특별자치시', '제주']
    result = []
    for sido in sido_list:
        page = 1
        while True:
            result = result + getStoreList(page, sido)
            if getStoreList(page, sido) == []: break
            print(sido, page)
            page += 1
    return result

def getStoreInfo(codeNo):
    url = "https://www.davich.com/04_market/02_shop.php?str_code={}".format(codeNo)
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    tbody = bsObj.find_all("table")
    data = []
    for list in tbody:
        try:
            name = "다비치안경"
            branch = list.find("td",{"class":"top"}).text.replace(" ","").rstrip().lstrip()
            addr = list.select('td')[3].text.replace("\xa0","")
            tell = list.select('td')[1].text
        except : pass
        else:
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return data

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()