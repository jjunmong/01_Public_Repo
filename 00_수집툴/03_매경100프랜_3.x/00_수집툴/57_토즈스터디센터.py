from selenium import webdriver
import sys
import time
import codecs
import requests
import random
import json
import bs4


def main():

    outfile = codecs.open('57_토즈스터디센터.txt', 'w', 'utf-8')
    outfile.write("NAME|ADDR|TELL|XCORD|YCORD\n")

    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['addr'])
        outfile.write(u'%s|' % store['tell'])
        outfile.write(u'%s|' % store['xcord'])
        outfile.write(u'%s\n' % store['ycord'])

    outfile.close()


def getStoreInfo():
    chromedriver_dir = r'C:\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)
    driver.get("https://www.toz.co.kr/branchSearch")
    time.sleep(1)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, "html.parser")
    branchList = soup.find("ul", {"class": "branchList"})
    li = branchList.findAll("li")
    result = []
    no = soup.find('b',{"class":"color_red totalCnt"}).text
    no = int(no) / 5 + 1
    no = int(no)
    print(no)
    for page in range (1, no):
        for lis in li:
            name = lis.find("strong",{"class":"name branchNameWrap"}).text.replace('\xa0',' ')
            addr = lis.find("p",{"class":"addr addressWrap"}).text
            tell = lis.find("span", {"class": "tel"}).text
            ycord = lis.find('a')['data-latitude']
            xcord = lis.find('a')['data-longitude']
            result.append({"name":name,"addr":addr,"tell":tell,"xcord":xcord,"ycord":ycord})

        driver.find_element_by_css_selector('#content > div > div > div.list > div.in_paging > a.next').click()
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
    driver.close()
    return result

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
