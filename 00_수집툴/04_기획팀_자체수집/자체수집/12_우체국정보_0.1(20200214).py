import time
import codecs
import requests
import random
import bs4

def main():

    outfile = codecs.open('12_우체국정보.txt', 'w', 'utf-8')
    outfile.write("postid|postdiv|postnm|postnmen|posttel|postfax|postaddr|postaddren|post365yn|posttime|postfinancetime"
                  "|postlat|postlon|postsubway|postoffiid|fundsaleyn\n")

    code_list = ['se','gi','bs','jj','jb','jn','kw','kb','cc']

    for code_num in code_list:
        page = 1
        while True:
            store_list = getinfo(page, code_num)
            if store_list == []: break;
            for store in store_list:
                outfile.write(u'%s|' % store['postid'])
                outfile.write(u'%s|' % store['postdiv'])
                outfile.write(u'%s|' % store['postnm'])
                outfile.write(u'%s|' % store['postnmen'])
                outfile.write(u'%s|' % store['posttel'])
                outfile.write(u'%s|' % store['postfax'])
                outfile.write(u'%s|' % store['postaddr'])
                outfile.write(u'%s|' % store['postaddren'])
                outfile.write(u'%s|' % store['post365yn'])
                outfile.write(u'%s|' % store['posttime'])
                outfile.write(u'%s|' % store['postfinancetime'])
                outfile.write(u'%s|' % store['postlat'])
                outfile.write(u'%s|' % store['postlon'])
                outfile.write(u'%s|' % store['postsubway'])
                outfile.write(u'%s|' % store['postoffiid'])
                outfile.write(u'%s\n' % store['fundsaleyn'])
            page += 1
            if page == 100: break
            time.sleep(random.uniform(0.3,0.6))

    outfile.close()

def getinfo(intPageNo, code):
    url = 'http://www.koreapost.go.kr/koreapost/openapi/searchPostSearchList.do?serviceKey=z8190426177ek76645gd146474142' \
          '&nowPage={}&pageCount=50&postTopId={}'.format(intPageNo, code)
    pageString = requests.get(url)
    print(url)
    pageString = pageString.text
    soup = bs4.BeautifulSoup(pageString, 'lxml')
    entityList = soup.find_all('postitem')
    data = []
    for info in entityList:
        postid = info.find("postid").text.rstrip().lstrip().upper()
        postdiv = info.find("postdiv").text.rstrip().lstrip().upper()
        postnm = info.find("postnm").text.rstrip().lstrip().upper()
        postnmen = info.find("postnmen").text.rstrip().lstrip().upper()
        posttel = info.find("posttel").text.rstrip().lstrip().upper()
        postfax = info.find("postfax").text.rstrip().lstrip().upper()
        postaddr = info.find("postaddr").text.rstrip().lstrip().upper()
        postaddren = info.find("postaddren").text.rstrip().lstrip().upper()
        post365yn = info.find("post365yn").text.rstrip().lstrip().upper()
        posttime = info.find("posttime").text.rstrip().lstrip().upper()
        postfinancetime = info.find("postfinancetime").text.rstrip().lstrip().upper()
        postlat = info.find("postlat").text.rstrip().lstrip().upper()
        postlon = info.find("postlon").text.rstrip().lstrip().upper()
        postsubway = info.find("postsubway").text.rstrip().lstrip().upper()
        postoffiid = info.find("postoffiid").text.rstrip().lstrip().upper()
        fundsaleyn = info.find("fundsaleyn").text.rstrip().lstrip().upper()
        data.append(
            {"postid": postid, "postdiv": postdiv, "postnm": postnm, "postnmen": postnmen, "posttel": posttel,
             "postfax": postfax
                , "postaddr": postaddr, "postaddren": postaddren, "post365yn": post365yn, "posttime": posttime,
             "postfinancetime": postfinancetime
                , "postlat": postlat, "postlon": postlon, "postsubway": postsubway, "postoffiid": postoffiid,
             "fundsaleyn": fundsaleyn})
    return data

main()