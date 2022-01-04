# -*- coding: utf-8 -*-
import cx_Oracle
import psycopg2
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
import os
import webbrowser
import csv
from shapely.geometry import mapping, Polygon
import fiona
import codecs
import requests
from pyproj import Proj, transform, CRS, Transformer
import json
import cx_Oracle
import psycopg2
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
import os
import webbrowser
import csv
from shapely.geometry import mapping, Polygon
import fiona
import codecs
import datetime
from fiona import _shim, schema
import io
import re
import time
from shapely import wkt
t_host = "192.168.11.61"  # either "localhost", a domain name, or an IP address.
t_port = "5432"  # default postgres port
t_dbname = "postgres"
t_user = "postgres"
t_pw = "rjator"
conn = psycopg2.connect(host=t_host, port=t_port, database=t_dbname, user=t_user, password=t_pw,options="-c search_path=cmms")
csv_file = open("도로개통정보.csv", "w",encoding='utf-8')
writer = csv.writer(csv_file, lineterminator="\n", delimiter='}', quoting=csv.QUOTE_NONE, escapechar='\\')
csv_file.write("TEXT}NID}TYPE}ROAD_WORK}TIME_ID}COMPLETE_DATE}LIMIT_DATE}NET_DATE\n")
query = "select text, nid, type, road_work,time_id, complete_date,limit_date,net_date from cmms_list where type not in ('아파트','시설') and net_cat = '완료' and del_flag ='0' order by complete_date"
cursor = conn.cursor()
cursor.execute(query)
row = cursor.fetchall()
for r in row:
    writer.writerow(r)
csv_file.close()
