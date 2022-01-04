from selenium import webdriver

driver = webdriver.Chrome(r'C:\chromedriver.exe')
driver.get('https://www.nextround.kr/CBBIBI02N01.act')
click_list = driver.find_element_by_xpath('//*[@id="pagination"]/button[3]')
driver.execute_script("arguments[0].click();", click_list)