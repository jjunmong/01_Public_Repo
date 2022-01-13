
from datetime import datetime, timedelta, date
a = datetime.now().weekday()
print(date.today())

today_day = date.today().day
today_month = date.today().month
today_year = date.today().year


def is_even(num):
  return num % 2 == 0

def get_date(y, m, d):
  '''y: year(4 digits)
   m: month(2 digits)
   d: day(2 digits'''
  s = f'{y:04d}-{m:02d}-{d:02d}'
  return datetime.strptime(s, '%Y-%m-%d')

def getWeekNo(y, m, d):
    target = get_date(y, m, d)
    firstday = target.replace(day=1)
    if firstday.weekday() == 6:
        origin = firstday
    elif firstday.weekday() < 3:
        origin = firstday - timedelta(days=firstday.weekday() + 1)
    else:
        origin = firstday + timedelta(days=6-firstday.weekday())
    return (target - origin).days // 7 + 1

weekNum = getWeekNo(today_year, today_month, today_day)


dateDict = {0: '월요일', 1:'화요일', 2:'수요일', 3:'목요일', 4:'금요일', 5:'토요일', 6:'일요일'}
date = date.today()
datetime_date = datetime.strptime(str(date), '%Y-%m-%d')
today_date = dateDict[date.weekday()]

print(today_date)