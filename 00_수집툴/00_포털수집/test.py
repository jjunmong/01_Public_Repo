from selenium import webdriver
from selenium.webdriver.chrome.options import Options

for i in range(3):
    chrome_options = Options()
    chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
    driver = webdriver.Chrome(executable_path='C:\chromedriver.exe', options=chrome_options)

    driver.get('https://ipv4.icanhazip.com')

    print(i)
