# -*- coding: utf-8 -*-

import os;
import sqlite3;
from PyQt5.QtGui import *;  #QIcon,QFont,QPalette
from PyQt5.QtCore import *; #QCoreApplication,QSize,Qt
from PyQt5.QtWidgets import *;  #QApplication,QWidget,QPushButton,QLabel,QMessageBox,QRadioButton,QMessageBox,QLineEdit
from Signup import SignupForm;

class Mainframe(QDialog):
    signal=pyqtSignal(int);
    user=pyqtSignal(str);
    channel=pyqtSignal(str);
    
    def __init__(self):
        super().__init__();
        self.loginSuccess=False;
        self.channelText=QLineEdit(self);
        self.idText=QLineEdit(self);
        self.pwdText=QLineEdit(self);
        self.initUI();
    
    def closeWindow(self):
        if(self.loginSuccess):
            self.signal.emit(1);
            self.user.emit(self.idText.text());
            self.channel.emit(self.channelText.text());
        else:
            self.signal.emit(0);
        self.close();
    
    def signup(self):
        form=SignupForm();
        form.initUI();
        form.exec_();
    
    def checkDb(self):
        if(not os.path.exists("infor.db")):
            connect=sqlite3.connect("infor.db");
            c=connect.cursor();
            c.execute('''
                      CREATE TABLE INFOR
                      (ID CHAR(50) PRIMARY NOT NULL,
                      PASSWORD CHAR(50) NOT NULL);
                      ''');
            connect.commit();
            connect.close();
    
    def login(self):
        self.checkDb();
        connect=sqlite3.connect("infor.db");
        c=connect.cursor();
        cursor=c.execute("SELECT * FROM INFOR WHERE ID=? AND PASSWORD=?",(self.idText.text(),self.pwdText.text()));
        result=[row for row in cursor];
        if(len(result)==0):
            QMessageBox.information(self,"Error","User id or password must be wrong.",QMessageBox.Ok,QMessageBox.Ok);
        else:
            connect.close();
            self.loginSuccess=True;
            self.closeWindow();
        
    def initUI(self):
        # set window
        self.setFixedSize(QSize(640,360)); # width, height
        self.setWindowTitle("IPFS Communication Program");
        self.setWindowIcon(QIcon("IPFS.png"));
        
        # set background image
        self.setWindowOpacity(0.95);
        palette=QPalette();
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap("bg_meitu_1.jpg")));
        self.setPalette(palette);
        
        # label
        lb1=QLabel(self);
        lb1.move(100,55);
        lb1.setText("Channel");
        lb1.setStyleSheet("color:#ffc05a;");

        lb2=QLabel(self);
        lb2.move(100,135);
        lb2.setText("User ID");
        lb2.setStyleSheet("color:#ffc05a;");

        lb3=QLabel(self);
        lb3.move(100,215);
        lb3.setText("Password");
        lb3.setStyleSheet("color:#000000;");
        
        # line edit
        self.channelText.move(170,40);
        self.channelText.resize(320,40);
        self.channelText.setStyleSheet("color:#ffc05a;border :1px ;background-color:rgba(50,50,50,0.3)")
        
        self.idText.move(170,120); 
        self.idText.resize(320,40);
        self.idText.setStyleSheet("color:#ffc05a;border :1px ;background-color:rgba(50,50,50,0.3)");
        
        self.pwdText.move(170,200);
        self.pwdText.resize(320,40);
        self.pwdText.setEchoMode(QLineEdit.Password);
        self.pwdText.setStyleSheet("color:#ffc05a;border :1px ;background-color:rgba(50,50,50,0.3)");
        
        # button
        loginBtn=QPushButton(self);
        loginBtn.setText("Log in");
        loginBtn.move(220,280);
        loginBtn.resize(100,40);
        loginBtn.setStyleSheet("color:#ffc05a;background-color:rgba(50,50,50,0.7)");
        loginBtn.clicked.connect(self.login);
        
        signupBtn=QPushButton(self);
        signupBtn.setText("Sign up");
        signupBtn.move(360,280);
        signupBtn.resize(100,40);
        signupBtn.setStyleSheet("color:#ffc05a;background-color:rgba(50,50,50,0.7)");
        signupBtn.clicked.connect(self.signup);
        
        quitBtn=QPushButton(self);
        quitBtn.setText("Quit");
        quitBtn.move(500,280);
        quitBtn.resize(100,40);
        quitBtn.setStyleSheet("color:#ffc05a;background-color:rgba(50,50,50,0.7)");
        quitBtn.clicked.connect(self.closeWindow);
        
        # show window
        self.show();