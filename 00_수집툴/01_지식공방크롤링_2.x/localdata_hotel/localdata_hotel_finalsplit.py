# -*- coding: utf-8 -*-

'''
Created on 1 Nov 2016

@author: jskyun
'''

import sys
import codecs
import urllib
import urllib2,cookielib
import json
import time
import random
import Tkinter
import tkFileDialog

from lxml import html

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    Tkinter.Tk().withdraw()  # Close the root window

    opts = {}
    opts['filetypes'] = [('txt files', '.txt'), ('all files', '.*')]
    opts['initialfile'] = 'all_out.txt'
    opts['title'] = 'select input file'

    infilename = tkFileDialog.askopenfilename(**opts)
    if infilename == '': errExit('no input file')

    infile = open(infilename, 'r')      # ANSI file open
    #infile = codecs.open(infilename, 'r', 'utf-8')
    #outfile = open(outfilename, 'w')

    # ANSI 인쇄용
    outfile1 = open(u'70201_모텔.txt', 'w')
    outfile2 = open(u'70202_여관.txt', 'w')
    outfile3 = open(u'70203_여인숙.txt', 'w')
    outfile4 = open(u'70204_펜션.txt', 'w')
    outfile5 = open(u'70205_고시원.txt', 'w')
    outfile6 = open(u'70206_게스트하우스.txt', 'w')
    outfile_etc = open(u'702_숙박.txt', 'w')

    # utf-8 인쇄용:
    #outfile1 = codecs.open(u'70201_모텔.txt', 'w', 'utf-8')
    #outfile2 = codecs.open(u'70202_여관.txt', 'w', 'utf-8')
    #outfile3 = codecs.open(u'70203_여인숙.txt', 'w', 'utf-8')
    #outfile4 = codecs.open(u'70204_펜션.txt', 'w', 'utf-8')
    #outfile5 = codecs.open(u'70205_고시원.txt', 'w', 'utf-8')
    #outfile6 = codecs.open(u'70206_게스트하우스.txt', 'w', 'utf-8')
    #outfile_etc = codecs.open(u'702_숙박.txt', 'w', 'utf-8')

    while True:
        line_ansi = infile.readline()
        if not line_ansi: break;

        # convert ANSI to UTF-8
        #line = unicode(line_ansi, "cp949").encode("utf-8")     # cp949 입력
        line = line_ansi    # utf8 입력
        line = line.replace('\r', '').replace('\t', '').replace('\n', '')

        curr_list = line.split('|')
        mappers_type = curr_list[4]

        #if mappers_type == '모텔': outfile1.write('%s' % line_ansi)
        #elif mappers_type == '여관': outfile2.write('%s' % line_ansi)
        #elif mappers_type == '여인숙/민박/산장': outfile3.write('%s' % line_ansi)
        #elif mappers_type == '펜션(관광지)': outfile4.write('%s' % line_ansi)
        #elif mappers_type == '고시원/원룸텔': outfile5.write('%s' % line_ansi)
        #elif mappers_type == '게스트하우스': outfile6.write('%s' % line_ansi)
        #else: outfile_etc.write('%s' % line_ansi)

        if line.startswith('##'): continue
        elif line.startswith('NAME|'): continue

        line = line.encode('cp949')

        if mappers_type == '모텔': outfile1.write('%s70201\n' % line)
        elif mappers_type == '여관': outfile2.write('%s70202\n' % line)
        elif mappers_type == '여인숙/민박/산장': outfile3.write('%s70203\n' % line)
        elif mappers_type == '펜션(관광지)': outfile4.write('%s70204\n' % line)
        elif mappers_type == '고시원/원룸텔': outfile5.write('%s70205\n' % line)
        elif mappers_type == '게스트하우스': outfile6.write('%s70206\n' % line)
        else: outfile_etc.write('%s702\n' % line)


    outfile1.close()
    outfile2.close()
    outfile3.close()
    outfile4.close()
    outfile5.close()
    outfile5.close()
    outfile_etc.close()


def errExit(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
