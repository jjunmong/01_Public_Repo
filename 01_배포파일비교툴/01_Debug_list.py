from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QProgressBar
import os
import codecs
import chardet
import openpyxl
import time
import csv
import pandas as pd
from dbfread import DBF
from detect_delimiter import detect
import xlrd
from openpyxl.styles import PatternFill, Font
from openpyxl.formatting.rule import  FormulaRule

def stand_list_save(dirname):
    dirname_fix = r'{}'.format(dirname)
    outfile = codecs.open('기준_파일리스트.txt', 'a')
    file_list = []
    filenames = os.listdir(dirname_fix)
    for filename in filenames:
        full_filename = os.path.join(dirname_fix, filename)
        if os.path.isdir(full_filename):
            stand_list_save(full_filename)
        else:
            # ext = os.path.splitext(full_filename)[-1]
            # if ext == '.csv':
            print(full_filename)
            fullname_fix = full_filename.upper()
            fullname = full_filename + '\n'
            if fullname_fix.endswith('.BMP') or fullname_fix.endswith('.MAX') or fullname_fix.endswith(
                    '.PVR') or fullname_fix.endswith('.TBM') or fullname_fix.endswith('.JPG') or fullname_fix.endswith(
                '.PNG') or fullname_fix.endswith('.POD') or fullname_fix.endswith('THUMBS.DB') or fullname_fix.endswith \
                ('.SHX' )== True:
                pass
            else:
                outfile.write(fullname)
                file_list.append(full_filename)
                # QApplication.processEvents()
    outfile.close()
    return file_list

def compare_list_save(dirname):
    dirname_fix = r'{}'.format(dirname)
    outfile = codecs.open('비교_파일리스트.txt', 'a')
    file_list = []
    filenames = os.listdir(dirname_fix)
    for filename in filenames:
        full_filename = os.path.join(dirname_fix, filename)
        if os.path.isdir(full_filename):
            compare_list_save(full_filename)
        else:
            # ext = os.path.splitext(full_filename)[-1]
            # if ext == '.csv':
            print(full_filename)
            fullname_fix = full_filename.upper()
            fullname = full_filename + '\n'
            if fullname_fix.endswith('.BMP') or fullname_fix.endswith('.MAX') or fullname_fix.endswith(
                    '.PVR') or fullname_fix.endswith('.TBM') or fullname_fix.endswith('.JPG') or fullname_fix.endswith(
                '.PNG') or fullname_fix.endswith('.POD') or fullname_fix.endswith('THUMBS.DB') or fullname_fix.endswith \
                ('.SHX') == True:
                pass
            else:
                outfile.write(fullname)
                file_list.append(full_filename)
                # QApplication.processEvents()
    outfile.close()
    return file_list

stand_list_save(r'\\ddss_nas05\MAPPLAN\MAPPLAN_3\01.외부_배포데이터\2021년\01.KT\20211125')
compare_list_save(r'\\ddss_nas05\MAPPLAN\MAPPLAN_3\01.외부_배포데이터\2021년\01.KT\20211202')