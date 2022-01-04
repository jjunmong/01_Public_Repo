import codecs
import requests
import json

sidolist = {
    '서울': {"강남구","강동구","강서구","관악구","광진구","구로구","금천구","노원구","도봉구","마포구","서대문구","서초구","성동구","성북구","송파구","양천구","영등포구","용산구","은평구"},
    '광주': {"광산구","남구","동구","북구","서구"},
    '대구': {'중구','동구','서구','남구','북구','수성구','달서구','달성군'},
    '대전': {'동구','중구','서구','유성구','대덕구'},
    '부산': {"강서구","금정구","기장군","남구","동구","동래구","부산진구","북구","사상구","사하구","서구","수영구","연제구","영도구","중구","해운대구"},
    '울산': {'중구','남구','동구','북구','울주군'},
    '인천': {'중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군','남구'},
    '경기도': {"가평군","고양시","광명시","광주시","구리시","군포시","김포시","남양주시","동두천시","부천시","성남시","수원시","시흥시","안산시","안성시","안양시","양주시","양평군","여주시","연천군","오산시","용인시","의왕시","의정부시","이천시","파주시","평택시","포천시","하남시","화성시"},
    '강원도': {"강릉시","고성군","동해시","삼척시","속초시","양구군","양양군","영월군","원주시","인제군","정선군","철원군","춘천시","태백시","평창군","홍천군","화천군","횡성군"},
    '경상남도': {"거제시","거창군","고성군","김해시","남해군","밀양시","사천시","산청군","양산시","의령군","진주시","창녕군","창원시","통영시","하동군","함안군","함양군","합천군"},
    '경상북도': {"경산시","경주시","고령군","구미시","군위군","김천시","문경시","봉화군","상주시","성주군","안동시","영덕군","영주시","영천시","예천군","울릉군","울진군","의성군","청도군","청송군","칠곡군","포항시"},
    '전라남도': {'목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무안군','함평군','영광군','장성군','완도군','진도군','신안군'},
    '전라북도': {'전주시','군산시','익산시','정읍시','남원시','김제시','완주군','진안군','무주군','장수군','임실군','순창군','고창군','부안군'},
    '충청남도': {'천안시','공주시','보령시','아산시','서산시','논산시','계룡시','금산군','연기군','부여군','서천군','청양군','홍성군','예산군','태안군','당진시'},
    '충청북도': {'청주시','충주시','제천시','청원군','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군'},
    '충북': {'영동군'},
    '제주': {'제주시','서귀포시'},
    '세종': {"금남구즉로","금남면","부강면","소정면","연기면","연동면","장군면","전동면","전의면","조치원읍"}
}

def main():

    outfile = codecs.open('18_유록스.txt', 'w', 'utf-8')
    outfile.write("ID|NAME|BRANCH|ADDRESS|TELL|EBD|PET|XCORD|YCORD|REGDATE|UPDATE\n")

    for sidoname in sorted(sidolist):
        gugunlist = sidolist[sidoname]
        for gugunname in sorted(gugunlist):
            storeList = getStoreInfo(sidoname, gugunname)
            for store in storeList:
                outfile.write(u'%s|' % store['id'])
                outfile.write(u'%s|' % store['name'])
                outfile.write(u'%s|' % store['branch'])
                outfile.write(u'%s|' % store['addr'])
                outfile.write(u'%s|' % store['tell'])
                outfile.write(u'%s|' % store['ebd'])
                outfile.write(u'%s|' % store['pet'])
                outfile.write(u'%s|' % store['xcord'])
                outfile.write(u'%s|' % store['ycord'])
                outfile.write(u'%s|' % store['regdate'])
                outfile.write(u'%s\n' % store['update'])

    outfile.close()

def getStoreInfo(sidoname, gugunname):
    url = 'https://www.eurox.co.kr/store/list.json'
    data = {
        # 'adr1': '강원도',
        # 'adr2': '강릉시',
        'adr3': '',
        'adr4': '',
        'ebd': 'Y',
        'pet': 'Y',
        'search': '',
    }
    data['adr1'] = sidoname
    data['adr2'] = gugunname
    jsonString = requests.post(url, data=data).text
    print(url , data)
    jsonData = json.loads(jsonString)
    entityList = jsonData['stationlist']
    result = []
    for info in entityList:
            id = info['id']
            name = info['name']
            brand = info['brand']
            addr = info['address']
            tell = info['phone']
            ebd = info['ebd']
            pet = info['pet']
            xcord = info['longitude']
            ycord = info['latitude']
            regdate = info['regdate']
            update = info['upddate']
            result.append({"id":id,"name":name,"branch":brand,"addr":addr,"tell":tell,"ebd":ebd,"pet":pet,"xcord":xcord,"ycord":ycord,"regdate":regdate,"update":update})
    return result

main()
