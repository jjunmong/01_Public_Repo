import requests
import bs4
import json
import codecs
import datetime
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
def aa():
    date_list = []
    n = 1
    while True:
        if n == 7 : break
        dateInfo = str(datetime.now() + relativedelta(months=n)).split(' ')[0]
        year = dateInfo.split('-')[0]
        month = int(dateInfo.split('-')[1])
        date_list.append({'year':year,'month':month})
        n+=1
    return date_list

print(aa()[0]['year'])