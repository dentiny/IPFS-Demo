# -*- coding: utf-8 -*-

import os;
import json;
from PyQt5.QtGui import *;  #QIcon,QFont,QPalette
from PyQt5.QtCore import *; #QCoreApplication,QSize,Qt
from PyQt5.QtWidgets import *;  #QApplication,QWidget,QPushButton,QLabel,QMessageBox,QRadioButton,QMessageBox,QLineEdit

class ViewHistory(QDialog):
    def __init__(self,channel):
        super().__init__();
        self.channel=channel;
        self.historyText=QTextEdit(self);
        self.initUI();
        self.showHistoryLog();
    
    def checkHistoryLog(self):
        if(not os.path.exists("history.json")):
            with open("history.json",'w',encoding="utf-8") as f:
                json.dump({},f);
    
    def showHistoryLog(self):
        self.checkHistoryLog();
        with open("history.json",'r',encoding="utf-8") as f:
            history=json.load(f).get(self.channel,[]);
            for line in history:
                self.historyText.append(line);
    
    def initUI(self):
        # set window
        self.setFixedSize(QSize(640,480)); # width, height
        self.setWindowTitle("History Log");
        self.setWindowIcon(QIcon("IPFS.png"));
        
        # text edit
        self.historyText.move(20,20);
        self.historyText.resize(600,440);
        
        # show window
        self.show();