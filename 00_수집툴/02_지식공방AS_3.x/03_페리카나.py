import requests
import codecs
import bs4
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

outfile = codecs.open('03_pelicana_utf8.txt', 'w', 'utf-8')
outfile.write("NAME|BRANCH|ADDR|TELL\n")

def crawl(url):
    data = requests.get(url, verify = False)
    return data.content

def parse(pageString):
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    tbody = bsObj.find_all("tr")
    data = []
    for list in tbody:
        try:
            name = "페리카나"
            branch = list.select("td")[0].text.replace(" ","").rstrip().lstrip()
            addr = list.select("td")[1].text.rstrip().lstrip()
            tell = list.select("td")[2].text.rstrip().lstrip()
        except AttributeError :
            pass
        except TypeError:
            pass
        except IndexError:
            pass
        else:
            data.append({"name":name,"branch":branch,"addr":addr,"tell":tell})
    return data

def getInfo(codeNo):
    url = "https://pelicana.co.kr/store/stroe_search.html?page={}&branch_name=&gu=&si=".format(codeNo)

    pageString = crawl(url)
    info = parse(pageString)
    return info

result = []
for codeNo in range(1,120):
    result = result + getInfo(codeNo)

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