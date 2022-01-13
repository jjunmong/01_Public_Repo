import sys
from PyQt5 import QtWidgets
# from PySide2 import QtWidgets
# from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import subprocess

from PyQt5.QtWidgets import QMainWindow
from qt_material import apply_stylesheet, QtStyleTools



class RuntimeStylesheets(QMainWindow, QtStyleTools):

    def __init__(self):
        super().__init__()
        self.main = QtCore.QObject.QtUiTools.QUiLoader().load('main_window.ui', self)

        self.add_menu_theme(self.main, self.main.menuStyles)
# run
