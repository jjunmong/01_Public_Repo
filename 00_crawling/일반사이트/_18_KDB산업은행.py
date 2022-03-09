import codecs
import time
import bs4
from selenium import webdriver
import re, sys
driver = webdriver.Chrome(r'C:\chromedriver.exe')
driver.get('https://www.nextround.kr/CBBIBI02N01.act')
def main():
    outfile = codecs.open('18_KDB산업은행.txt', 'w', 'utf-8')
    outfile.write("NAME|BRANCH|OLD_ADDR|NEW_ADDR|TELL|FAX|DETAIL\n")

    result = []
    for num in range(1, pageNo()):
        time.sleep(1)
        result = result + getStores()

    for results in result:
        print(results)

    for result_list in result:
        outfile.write(u'%s|' % result_list['name'])
        outfile.write(u'%s|' % result_list['branch'])
        outfile.write(u'%s|' % result_list['old_addr'])
        outfile.write(u'%s|' % result_list['new_addr'])
        outfile.write(u'%s|' % result_list['tell'])
        outfile.write(u'%s|' % result_list['fax'])
        outfile.write(u'%s\n' % result_list['detail'])

    outfile.close()


def getStores():
    html = driver.page_source
    bsObj = bs4.BeautifulSoup(html,"html.parser")
    inner = bsObj.find('div',{"class":"inner"})
    li_all = inner.find_all('a')
    data = []
    for list in li_all:
        try:
            name = "KDB산업은행"
            branch_all = list.find('div',{"class":"branch"}).text.rstrip().lstrip().upper().replace(' ','')
            hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
            branch = hangul.sub('', branch_all)
            if branch == '' : branch = 'DIGITALSQUARE'  #한글 제외 모든 문자 사라지게 했더니 디지털 스퀘어 1개 지점의 이름이 사라져서 1개만 예외 처리.
            old_addr = list.select('p')[1].text.rstrip().lstrip().upper()
            old_addr = old_addr[13:]
            old_addr = re.sub(r'\([^)]*\)', '', old_addr).rstrip().lstrip().upper()
            print(old_addr)
            new_addr = list.select('p')[0].text.rstrip().lstrip().upper()
            new_addr = new_addr[14:]
            new_addr = re.sub(r'\([^)]*\)', '', new_addr).rstrip().lstrip().upper()
            print(new_addr)
            tell = list.select('li')[0].text.rstrip().lstrip().upper().replace('TEL : ','')
            fax = list.select('li')[1].text.rstrip().lstrip().upper().replace('FAX : ','')
            detail = list.find('div',{"class":"badgeList"}).text.rstrip().lstrip().upper().replace("대여금고","대여금고/").replace("PB업무", "PB업무/").replace("ATM", "ATM/").replace('365코너','365코너/')
        except AttributeError:
            pass
        except IndexError:
            pass
        except TypeError:
            pass
        else:
            data.append({'name':name,'branch':branch,'old_addr':old_addr,'new_addr':new_addr,'tell':tell,'fax':fax,'detail':detail})
    time.sleep(1)
    try:
        click_list = driver.find_element_by_xpath('//*[@id="pagination"]/button[3]')
        driver.execute_script("arguments[0].click();", click_list)
    except :
        pass
    return data

def pageNo():
    pageNo1 = driver.find_element_by_xpath('//*[@id="current"]').text.replace('1 / ','')
    return int(pageNo1)

def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()


