import requests
import bs4

def main():
    url = 'https://www.mk.co.kr/news/business/new-corporation/'
    pageString = requests.get(url).text
    bsObj = bs4.BeautifulSoup(pageString,"html.parser")
    dl = bsObj.find('dl',{"class":"article_list pt0"})
    source_url = dl.find('a')['href']

    url = source_url
    pageString = requests.get(url)
    bsObj = bs4.BeautifulSoup(pageString.content,"html.parser")
    div = bsObj.find('div',{"id":"article_body"})
    down_url = div.find('a')['href']
    file_text = div.find('b').text.replace(' ','')+'.xls'
    url = down_url
    filename = file_text
    with open('수집결과\\'+filename, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    print('신설법인 다운로드 완료')

main()







