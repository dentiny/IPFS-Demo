# -*- coding: utf-8 -*-

from PyQt5.QtGui import *;  #QIcon,QFont,QPalette
from PyQt5.QtCore import *; #QCoreApplication,QSize,Qt
from PyQt5.QtWidgets import *;  #QApplication,QWidget,QPushButton,QLabel,QMessageBox,QRadioButton,QMessageBox,QLineEdit

class FriendDialog(QDialog):
    signal=pyqtSignal(int);    
    
    def __init__(self,api,mode):
        super().__init__();
        # change friend list
        self.mode=mode;
        self.ADD_MODE=0;
        self.DELETE_MODE=1;
        
        self.api=api;
        self.changeSuccess=False;
        self.friAddr=QLineEdit(self);
        self.initUI();
        
    def closeWindow(self):
        if(self.changeSuccess):
            self.signal.emit(1);
        else:
            self.signal.emit(0);
        self.close();
        
    def submit(self):
        try:
            if(self.mode==self.ADD_MODE):
                self.api.bootstrap_add(self.friAddr.text());
                QMessageBox.information(self,"Success","Add peer success.",QMessageBox.Ok,QMessageBox.Ok);
            elif(self.mode==self.DELETE_MODE):
                self.api.bootstrap_rm(self.friAddr.text());
                QMessageBox.information(self,"Success","Delete peer success.",QMessageBox.Ok,QMessageBox.Ok);
            self.changeSuccess=True;
            self.closeWindow();
        except:
            if(self.mode==0):
                QMessageBox.information(self,"Error","Add peer failure.",QMessageBox.Ok,QMessageBox.Ok);
            elif(self.mode==1):
                QMessageBox.information(self,"Error","Delete peer failure.",QMessageBox.Ok,QMessageBox.Ok);
        
    def initUI(self):
        # set window
        self.setFixedSize(QSize(700,200)); # width, height
        self.setWindowTitle("IPFS Add Friend");
        self.setWindowIcon(QIcon("IPFS.png"));
        
        # set background image
        self.setWindowOpacity(0.95);
        palette=QPalette();
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("Friend_bg.jpg")));
        self.setPalette(palette);
        
        # label
        lb1=QLabel(self);
        lb1.move(20,20);
        lb1.setText("Friend Address");
        lb1.setStyleSheet("font-size:17px; font-weight:500;color:#007a59;");
        
        # text edit
        self.friAddr.move(20,60);
        self.friAddr.resize(660,40);
        self.friAddr.setStyleSheet("font-size:17px; font-weight:500;color:#000000;border :1px ;""background-color:rgba(50,150,50,0.3)");
        self.friAddr.selectAll();
        
        # submit button
        submitBtn=QPushButton(self);
        submitBtn.setText("Submit");
        submitBtn.move(270,120);
        submitBtn.resize(160,40);
        submitBtn.setStyleSheet("font-size:20px; font-weight:500;color:#007a59;background-color:rgba(255,255,255,0.5)");
        submitBtn.clicked.connect(self.submit);
        
        # show window
        self.show();