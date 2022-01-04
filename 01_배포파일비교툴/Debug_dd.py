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

def stand_list():
    with open('기준_파일리스트.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    return SearchList

def compare_list():
    with open('비교_파일리스트.txt') as data:
        lines = data.read().splitlines()
    SearchList = lines
    return SearchList

def list_compare():
    # 폴더 비교를 위해 경로명의 서로 다른 부분을 없애고 공통 부분을 추출하도록 정제 하는 과정
    A_list_fix_name = stand_list()[0].split('\\')[:6]
    if '01.외부_배포데이터' in A_list_fix_name : A_list_fix_name = stand_list()[0].split('\\')[:9]
    A_list_fix_name = '\\'.join(A_list_fix_name)

    B_list_fix_name = compare_list()[0].split('\\')[:6]
    if '01.외부_배포데이터' in B_list_fix_name: B_list_fix_name = compare_list()[0].split('\\')[:9]
    B_list_fix_name = '\\'.join(B_list_fix_name)

    A_list_fix = []
    for i in stand_list():
        s = i.split('\\')[6:]
        if '01.외부_배포데이터' in i: s = i.split('\\')[9:]
        print(s)
        s = '\\'.join(s)
        A_list_fix.append(s)

    B_list_fix = []
    for i in compare_list():
        s = i.split('\\')[6:]
        if '01.외부_배포데이터' in i: s = i.split('\\')[9:]
        s = '\\'.join(s)
        B_list_fix.append(s)

    # 두리스트 간의 차집합 리스트 추출
    A_list = set(A_list_fix)
    B_list = set(B_list_fix)

    A_only = A_list - B_list
    A_only_list = []
    for i in A_only:
        s = (A_list_fix_name + '\\' + i)
        A_only_list.append(s)

    B_only = B_list - A_list
    B_only_list = []
    for i in B_only:
        s = (B_list_fix_name + '\\' + i)
        B_only_list.append(s)

    # 두 리스트 간의 교집합 추출
    Intersection = A_list & B_list
    Intersection_list = []
    for i in Intersection:
        a = (A_list_fix_name + '\\' + i)
        b = (B_list_fix_name + '\\' + i)
        Intersection_list.append({'a': a, 'b': b})
    return A_only_list, B_only_list, Intersection_list


print(list_compare())