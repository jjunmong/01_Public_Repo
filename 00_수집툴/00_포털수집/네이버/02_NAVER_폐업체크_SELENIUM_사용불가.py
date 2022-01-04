from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
from selenium import webdriver
import bs4
import time
import codecs
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
start = time.time()

outfile = codecs.open('Naver_result.txt', 'w', 'utf-8')
outfile.write("INPUTNAME|NAME|NEWADDR|OLDADDR|CAT|TELL|URL\n")

with open('Naver_input.txt') as data:
    lines = data.read().splitlines()

def copy_input(xpath, input):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(1)

id = 'soelyh1005'
pw = 'Wnsdud87!'

driver = webdriver.Chrome(r'C:\chromedriver.exe')
driver.get('https://v4.map.naver.com/')
driver.implicitly_wait(3)
driver.find_element_by_xpath('//*[@id="dday_popup"]/div[2]/button').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="gnb_login_button"]').click()
time.sleep(1)
copy_input('//*[@id="id"]', id)
time.sleep(1)
copy_input('//*[@id="pw"]', pw)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="dday_popup"]/div[2]/button').click()
time.sleep(1)

def checkList(inputname):
    list = driver.find_element_by_xpath('//*[@id="search-input"]')
    list.send_keys(inputname)
    list.send_keys('\n')
    time.sleep(0.2)
    listAll = []
    try:
        search_result = driver.find_element_by_xpath('//*[@id="panel"]/div[2]/div[1]/div[2]/div[2]/h3').text
    except UnexpectedAlertPresentException:
        listAll.append(
            {"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None,
             "url": None})
    except NoSuchElementException:
        listAll.append(
            {"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None,
             "url": None})
    else:
        if search_result == "검색 결과없음":
            listAll.append(
                {"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None,
                 "url": None})
        else:
            try:
                contents_box = driver.find_element_by_xpath('//*[@id="panel"]/div[2]/div[1]/div[2]/div[2]/ul/li[1]')
                contents_box.click()
            except UnexpectedAlertPresentException:
                listAll.append(
                    {"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None,
                     "url": None})
            except NoSuchElementException:
                listAll.append(
                    {"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None,
                     "url": None})
            else:
                try:
                    html = driver.page_source
                    soup = bs4.BeautifulSoup(html, 'html.parser')
                    soup2 = soup.find("div", {"class": "_infowindow_content"})
                    print(soup2)
                    match = soup2.select('a')[1].text.rstrip().lstrip()
                    newaddr = soup2.find('dt', {"class": "addr"}).text.rstrip().lstrip()
                    oldaddr = soup2.find('dd', {"class": "info_road"}).text.replace("지번주소", "").rstrip().lstrip()
                    cat = soup2.find('span', {"class": "cate"}).text.rstrip().lstrip()
                    tell = soup2.find('span', {"class": "tel"}).text.rstrip().lstrip()
                    url_all = soup2.find('div', {"class": "spotly_btnset"})
                    url_all2 = url_all.find("a")
                    url = url_all2.attrs['href'].replace("//v4", "//v5")
                except AttributeError:
                    listAll.append(
                        {"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None,
                         "url": None})
                except IndexError:
                    listAll.append(
                        {"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None,
                         "url": None})
                except IndexError:
                    listAll.append(
                        {"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None,
                         "url": None})
                except KeyError:
                    listAll.append(
                        {"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None, "tell": None,
                         "url": None})
                except UnexpectedAlertPresentException:
                    listAll.append(
                        {"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None,
                         "tell": None,
                         "url": None})
                except NoSuchElementException:
                    listAll.append(
                        {"inputname": inputname, "name": None, "newaddr": None, "oldaddr": None, "cat": None,
                         "tell": None,
                         "url": None})
                else:
                    listAll.append({"inputname": inputname, "name": match, "newaddr": newaddr, "oldaddr": oldaddr, "cat": cat,
                                    "tell": tell, "url": url})
    return listAll
addr_list = lines

result = []
for get in addr_list:
    time.sleep(0.4)
    driver.refresh()
    time.sleep(0.4)
    driver.find_element_by_xpath('//*[@id="dday_popup"]/div[2]/button').click()
    time.sleep(0.5)
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