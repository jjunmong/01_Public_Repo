import bs4
import requests
import codecs
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

outfile = codecs.open('07_BMW_MINI_SERVICE.txt', 'w', 'utf-8')
outfile.write("NAME|BRANCH|ADDR|TELL|OT\n")

def crawl(url):
    data = requests.get(url, verify = False)
    return data.content

def parse(pageString):
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tr = bsObj.find_all("td",{"class":"left tableTd"})
    data = []
    for list in tr:
        try:
            name = "BMW미니"
            branch = list.find("h1").text.replace(" ","").rstrip().lstrip().replace("SERVICECENTER","서비스센터").replace("(","").replace(")","")
            addr = list.select('td')[0].text.rstrip().lstrip()
            tell = list.select('td')[1].text.rstrip().lstrip()
            time = list.select('td')[2].text.rstrip().lstrip()
        except AttributeError :
            pass
        except TypeError:
            pass
        except IndexError:
            pass
        else:
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell,"time":time})
    return data

def getInfo():
    url = "https://kr.mini.co.kr/map/serviceCenter"
    pageString = crawl(url)
    info = parse(pageString)
    return info

result = []
result = result + getInfo()

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
    outfile.write(u'%s|' % result_list['tell'])
    outfile.write(u'%s|\n' % result_list['time'])
outfile.close()