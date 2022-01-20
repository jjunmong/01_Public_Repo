import smtplib
from email.mime.text import MIMEText
import cx_Oracle
import csv
import psycopg2
import datetime
import time
import schedule
import os
import sys
import openpyxl
import codecs
import traceback

smtpName = "smtp.naver.com"
smtpPort = 587
sendEmail = "soelyh1005@naver.com"
password = "Wnsdud87!"
# recvEmail = 'sykim@mappers.kr','kskim@mappers.kr','tkyoon@mappers.kr'
recvEmail = 'jyseol@mappers.kr'
title = "[알림] CMMS DB Daily Update Alert"
content = """
#{} CMMS DB 동기화가 정상적으로 완료 되었습니다.#\n
""".format(datetime.date.today())
msg = MIMEText(content)
msg['From'] = sendEmail
msg['To'] = recvEmail
msg['Subject'] = title

s = smtplib.SMTP(smtpName, smtpPort)
s.starttls()
s.login(sendEmail, password)
s.sendmail(sendEmail, recvEmail, msg.as_string())
s.close()