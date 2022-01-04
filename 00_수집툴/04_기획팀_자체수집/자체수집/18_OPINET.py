import codecs
import requests
import bs4

def main():
    outfile = codecs.open('18_OPINET.txt', 'w', 'utf-8')
    outfile.write("unino|poll|gpoll|name|oldaddr|newaddr|tel|gisxcord|gisycord|maint_yn|cvs_yn|wash_yn|self_yn|sel24_yn|lpg_yn|clo_yn|mdfy_dt\n")
    store_list = getStoreInfo()
    for store in store_list:
        outfile.write(u'%s|' % store['unino'])
        outfile.write(u'%s|' % store['poll'])
        outfile.write(u'%s|' % store['gpoll'])
        outfile.write(u'%s|' % store['name'])
        outfile.write(u'%s|' % store['oldaddr'])
        outfile.write(u'%s|' % store['newaddr'])
        outfile.write(u'%s|' % store['tel'])
        outfile.write(u'%s|' % store['gisxcord'])
        outfile.write(u'%s|' % store['gisycord'])
        outfile.write(u'%s|' % store['maint_yn'])
        outfile.write(u'%s|' % store['cvs_yn'])
        outfile.write(u'%s|' % store['wash_yn'])
        outfile.write(u'%s|' % store['self_yn'])
        outfile.write(u'%s|' % store['sel24_yn'])
        outfile.write(u'%s|' % store['lpg_yn'])
        outfile.write(u'%s|' % store['clo_yn'])
        outfile.write(u'%s\n' % store['mdfy_dt'])
    outfile.close()

def getStoreInfo():
    url ='http://www.opinet.co.kr/cp/stationMappersAll.do'
    response = requests.get(url).text
    response = str(response).replace('<![CDATA[','').replace(']]>','')
    bsObj = bs4.BeautifulSoup(response,'lxml')
    item = bsObj.find_all('item')
    data = []
    for info in item:
        try:unino = info.find('unino').text.rstrip().lstrip().upper()
        except: unino= ''
        try:gpoll = info.find('gpoll').text.rstrip().lstrip().upper()
        except: gpoll= ''
        try:poll = info.find('poll').text.rstrip().lstrip().upper()
        except: poll= ''
        try:name = info.find('osnm').text.rstrip().lstrip().upper()
        except:name = ''
        try:oldaddr = info.find('adr').text.rstrip().lstrip().upper()
        except: oldaddr= ''
        try:newaddr = info.find('newadr').text.rstrip().lstrip().upper()
        except: newaddr= ''
        try:tel = info.find('tel').text.rstrip().lstrip().upper()
        except:tel= ''
        try:gisxcord = info.find('gisxcoor').text.rstrip().lstrip().upper()
        except: gisxcord= ''
        try:gisycord = info.find('gisycoor').text.rstrip().lstrip().upper()
        except: gisycord= ''
        try:maint_yn = info.find('maint_yn').text.rstrip().lstrip().upper()
        except: maint_yn= ''
        try:cvs_yn = info.find('cvs_yn').text.rstrip().lstrip().upper()
        except:cvs_yn = ''
        try:wash_yn = info.find('wash_yn').text.rstrip().lstrip().upper()
        except: wash_yn= ''
        try:self_yn = info.find('self_yn').text.rstrip().lstrip().upper()
        except: self_yn= ''
        try:sel24_yn = info.find('sel24_yn').text.rstrip().lstrip().upper()
        except: sel24_yn= ''
        try:lpg_yn = info.find('lpg_yn').text.rstrip().lstrip().upper()
        except: lpg_yn= ''
        try:clo_yn = info.find('clo_yn').text.rstrip().lstrip().upper()
        except: clo_yn= ''
        try:mdfy_dt = info.find('mdfy_dt').text.rstrip().lstrip().upper()
        except: mdfy_dt= ''
        data.append({'unino':unino,'poll':poll,'gpoll':gpoll,'name':name,'oldaddr':oldaddr,'newaddr':newaddr,'tel':tel,
                     'gisxcord':gisxcord,'gisycord':gisycord,'maint_yn':maint_yn,'cvs_yn':cvs_yn,'wash_yn':wash_yn,
                     'self_yn':self_yn,'sel24_yn':sel24_yn,'lpg_yn':lpg_yn,'clo_yn':clo_yn,'mdfy_dt':mdfy_dt})
    return data
main()