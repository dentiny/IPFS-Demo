# -*- coding: utf-8 -*-

import os;
import shutil;
from PyQt5.QtGui import *;  #QIcon,QFont,QPalette
from PyQt5.QtCore import *; #QCoreApplication,QSize,Qt
from PyQt5.QtWidgets import *;  #QApplication,QWidget,QPushButton,QLabel,QMessageBox,QRadioButton,QMessageBox,QLineEdit

class ImageLoader(QDialog):
    def __init__(self,path,title):
        super().__init__();
        self.path=path;
        self.title=title;
        self.label=QLabel(self);
        self.initUI();
    
    def saveImage(self):
        fileType="Bmp(*.bmp);;Jpg(*.jpg);;Jpeg(*.jpeg);;Png(*.png);;Gif(*.gif);;Icon(*.icon)";
        savePath=QFileDialog.getOpenFileName(self,"Save","./",fileType);
        if(os.path.exists(self.path)):
            shutil.move(self.path,savePath);    
        self.close();
    
    def deleteImage(self):
        if(os.path.exists(self.path)):
            os.remove(self.path);
        self.close();
    
    def initUI(self):
        # set window
        self.setFixedSize(QSize(640,520)); # width, height
        self.setWindowTitle(self.title);
        self.setWindowIcon(QIcon("IPFS.png"));
        
        # label to place image
        self.label.move(40,40);
        self.label.setFixedSize(560,400);
        
        # image
        img=QPixmap(self.path).scaled(self.label.width(),self.label.height());
        self.label.setPixmap(img);
        
        # button
        yesBtn=QPushButton(self);
        yesBtn.move(130,460);
        yesBtn.resize(120,40);
        yesBtn.setText("Save");
        yesBtn.clicked.connect(self.saveImage);
        
        noBtn=QPushButton(self);
        noBtn.move(390,460);
        noBtn.resize(120,40);
        noBtn.setText("Quit");
        noBtn.clicked.connect(self.deleteImage);
        
        # show window
        self.show();