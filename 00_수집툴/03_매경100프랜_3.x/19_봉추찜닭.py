import bs4
import requests
import codecs

######사이트 접속이 불가능한 상태###############

outfile=codecs.open('19_봉추찜닭.txt', 'w', 'utf-8')
outfile.write("NAME|BRANCH|ADDR|TELL\n")

def crawl(url):
    data = requests.get(url)
    return data.content

def parse(pageString):
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find_all("tr")
    data = []
    for list in tbody:
        try:
            name = "봉추찜닭"
            branch = list.find("a").text.replace(" ","").rstrip().lstrip().upper()
            addr = list.find("td", {"class": "m_no"}).text.rstrip().lstrip().upper()
            tell = list.select('td')[3].text.rstrip().lstrip().upper()
        except AttributeError :
            pass
        else :
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return data

def getInfo(pageNo):
    url = "http://bongchu.com/kr/index.php?mid=chains&page={}".format(pageNo)
    pageString = crawl(url)
    info = parse(pageString)
    return info

result = []
for pageNo in range(1,20):
    result = result + getInfo(pageNo)

results = set()
new_results = []
for list in result:
    lists = tuple(list.items())
    if lists not in results:
        results.add(lists)
        new_results.append(list)

for ss in new_results:
    print(ss)

for result_list in new_results:
    outfile.write(u'%s|' % result_list['name'])
    outfile.write(u'%s|' % result_list['branch'])
    outfile.write(u'%s|' % result_list['addr'])
    outfile.write(u'%s|\n' % result_list['tell'])
outfile.close()

