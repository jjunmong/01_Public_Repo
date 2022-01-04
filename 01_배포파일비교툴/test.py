a= r'C:\00_DEV\01_배포파일비교툴\COVID-19_screening_center.txt'



str1 = r'\\ddss_nas05\MAPPLAN\MAPPLAN_1\01.DATA\98.기획팀수집툴배포\21_GSTHEFRESH'
str2 = '\\'
c = str1.count('\\')
print(c)

a = str1.find(str2)

while str1[a+1:].find(str2) != -1:
    a = str1[a+1:].find(str2) + a + 1
    print (a)