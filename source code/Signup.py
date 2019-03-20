# -*- coding: utf-8 -*-

import os;
import sqlite3;
from PyQt5.QtGui import *;  #QIcon,QFont,QPalette
from PyQt5.QtCore import *; #QCoreApplication,QSize,Qt
from PyQt5.QtWidgets import *;  #QApplication,QWidget,QPushButton,QLabel,QMessageBox,QRadioButton,QMessageBox,QLineEdit

class SignupForm(QDialog):
    def __init__(self):
        super().__init__();
        self.idText=QLineEdit(self);
        self.pwdText=QLineEdit(self);
        self.checkDb();
        self.initUI();       
    
    def checkDb(self):
        if(not os.path.exists("infor.db")):
            connect=sqlite3.connect("infor.db");
            c=connect.cursor();
            c.execute('''
                      CREATE TABLE INFOR
                      (ID CHAR(50) PRIMARY KEY NOT NULL,
                      PASSWORD CHAR(50) NOT NULL);
                      ''');
            connect.commit();
            connect.close();
    
    def checkVadation(self):
        # check repeated user id
        userId=self.idText.text();
        if(len(userId)<6):
            QMessageBox.information(self,"Error","User ID must exceed 5 charaters.",QMessageBox.Ok,QMessageBox.Ok);
            return False;
        elif(len(userId)>=50):
            QMessageBox.information(self,"Error","User ID must be within 50 charaters.",QMessageBox.Ok,QMessageBox.Ok);
            return False;
        
        connect=sqlite3.connect("infor.db");
        c=connect.cursor();
        cursor=c.execute("SELECT * FROM INFOR WHERE ID=?",(self.idText.text(),));
        result=[row for row in cursor];
        if(len(result)!=0):
            QMessageBox.information(self,"Error","User ID has been registered before.",QMessageBox.Ok,QMessageBox.Ok);
            connect.close();
            return False;
        
        # check valid password
        password=self.pwdText.text();
        if(len(password)<6):
            QMessageBox.information(self,"Error","Password must exceed 5 characters.",QMessageBox.Ok,QMessageBox.Ok);
            return False;
        elif(len(password)>=50):
            QMessageBox.information(self,"Error","Password must be within 50 characters.",QMessageBox.Ok,QMessageBox.Ok);
            return False;
        
        hasLowercase,hasUppercase,hasDigit=False,False,False;
        for s in password:
            if('a'<=s<='z'):
                hasLowercase=True;
            elif('A'<=s<='Z'):
                hasUppercase=True;
            elif('0'<=s<='9'):
                hasDigit=True;
        if(not hasLowercase):
            QMessageBox.information(self,"Error","Password must contain lowercase.",QMessageBox.Ok,QMessageBox.Ok);
            return False;
        elif(not hasUppercase):
            QMessageBox.information(self,"Error","Password must contain uppercase.",QMessageBox.Ok,QMessageBox.Ok);
            return False;
        elif(not hasDigit):
            QMessageBox.information(self,"Error","Password must contain digit.",QMessageBox.Ok,QMessageBox.Ok);
            return False;
        
        QMessageBox.information(self,"Success","Sign up success.",QMessageBox.Ok,QMessageBox.Ok);
        connect.close();
        return True;
    
    def submit(self):
        '''
        TABLE: INFOR
        ID: CHAR(50) PRIMARY KEY NOT NULL
        PASSWORD: CHAR(50) NOT NULL
        '''
        
        if(self.checkVadation()):
            connect=sqlite3.connect("infor.db");
            c=connect.cursor();
            c.execute('''
                      INSERT INTO INFOR
                      (ID,PASSWORD)
                      VALUES("{}","{}")
                      '''.format(self.idText.text(),self.pwdText.text()));
            connect.commit();
            connect.close();
            self.close();
        
    def initUI(self):
        # set window
        self.setFixedSize(QSize(480,320));
        self.setWindowTitle("Sign Up");
        self.setWindowIcon(QIcon("IPFS.png"));
        
        # set background image
        self.setWindowOpacity(0.95);
        palette=QPalette();
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("bg_meitu_1.jpg")));
        self.setPalette(palette);

        # label
        lb1=QLabel(self);
        lb1.move(80,95);
        lb1.setText("User name");
        lb1.setStyleSheet("color:#ffc05a;");

        lb2=QLabel(self);
        lb2.move(80,175);
        lb2.setText("Password");
        lb2.setStyleSheet("color:#000000;");

        # input line edit
        self.idText.move(160,80);
        self.idText.resize(240,40);
        self.idText.setStyleSheet("color:#ffc05a;border:1px ;background-color:rgba(50,50,50,0.3)");
        
        self.pwdText.move(160,160);
        self.pwdText.resize(240,40);
        self.pwdText.setEchoMode(QLineEdit.Password);
        self.pwdText.setStyleSheet("color:#ffc05a;border:1px ;background-color:rgba(50,50,50,0.3)");
        
        # push button
        submitBtn=QPushButton(self);
        submitBtn.move(200,240);
        submitBtn.resize(80,40);
        submitBtn.setText("Submit");
        submitBtn.setStyleSheet("color:#ffc05a;background-color:rgba(50,50,50,0.7)");
        submitBtn.clicked.connect(self.submit);
        
        # show window
        self.show();