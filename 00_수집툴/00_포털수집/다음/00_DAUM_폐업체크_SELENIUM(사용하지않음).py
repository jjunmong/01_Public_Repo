from selenium import webdriver
import bs4
import time
import codecs
import time
import random
start = time.time()

outfile = codecs.open('Daum_result.txt', 'w', 'utf-8')
outfile.write("INPUTNAME|NAME|NEWADDR|OLDADDR|CAT|TELL|URL\n")

with open('daum_input.txt') as data:
    lines = data.read().splitlines()

addr_list = lines

chromedriver_dir = r'C:\chromedriver.exe'
driver = webdriver.Chrome(chromedriver_dir)
driver.get('https://map.kakao.com/')
time.sleep(1)

click2 = driver.find_element_by_xpath('/html/body/h2[1]')
driver.execute_script("arguments[0].click();", click2)
click3 = driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button')
driver.execute_script("arguments[0].click();", click3)
time.sleep(1)

idInput = driver.find_element_by_xpath('//*[@id="id_email_2"]')
idInput.clear()
idInput.send_keys("본인아이디")
time.sleep(1)

passInput = driver.find_element_by_xpath('//*[@id="id_password_3"]')
passInput.clear()
passInput.send_keys("본인 비번")
time.sleep(1)

click4 = driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button')
driver.execute_script("arguments[0].click();", click4)

def checkList(inputname):
    list = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')
    list.send_keys(inputname)
    list.send_keys('\n')
    time.sleep(0.2)
    listAll = []
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    soup2 = soup.find("ul",{"class":"placelist"})
    soup3 = soup2.find("li")
    try :
        match = soup3.select('span')[0].text.rstrip().lstrip()
        newaddr = soup3.select('p')[0].text.rstrip().lstrip()
        oldaddr = soup3.select('p')[1].text.rstrip().lstrip()
        cat = soup3.select('span')[3].text.rstrip().lstrip()
        tell = soup3.select('span')[11].text.rstrip().lstrip()
        url_all = soup3.select("a")[5]
        url = url_all.attrs['href']
    except TypeError:
        listAll.append({"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None,"url": None})
    except AttributeError:
        listAll.append({"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None, "url": None})
    except IndexError:
        listAll.append({"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None, "url": None})
    else:
        listAll.append({"inputname":inputname,"name":match,"newaddr":newaddr,"oldaddr":oldaddr,"cat":cat,"tell":tell,"url":url})
    return listAll
    print(inputname)
timedelay = random.random()

result = []
for get in addr_list:
    time.sleep(0.5)
    driver.refresh()
    time.sleep(0.6)
    result = result + checkList(get)

for ssd in result:
    print(ssd)

for results in result:
    outfile.write(u'%s|' % results['inputname'])
    outfile.write(u'%s|' % results['name'])
    outfile.write(u'%s|' % results['newaddr'])
    outfile.write(u'%s|' % results['oldaddr'])
    outfile.write(u'%s|' % results['cat'])
    outfile.write(u'%s|' % results['tell'])
    outfile.write(u'%s|\n' % results['url'])
outfile.close()
driver.close()
print("time :", time.time() - start)