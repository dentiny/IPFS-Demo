# -*- coding: utf-8 -*-

import os;
import sys;
import json;
import ipfsapi;
from PyQt5.QtGui import *;  #QIcon,QFont,QPalette
from PyQt5.QtCore import *; #QCoreApplication,QSize,Qt
from PyQt5.QtWidgets import *;  #QApplication,QWidget,QPushButton,QLabel,QMessageBox,QRadioButton,QMessageBox,QLineEdit
from Receiver import Receiver;
from Mainframe import Mainframe;
from Friend import FriendDialog;
from ViewHistory import ViewHistory;

class GUI(QWidget):
    def __init__(self):
        super().__init__();
        # IPFS api
        try:
            self.api=ipfsapi.connect("127.0.0.1",5001);
        except:
            QMessageBox.information(self,"Error","Launch daemon first.",QMessageBox.Ok,QMessageBox.Ok);
            self.close();
        
        # operation on friend list
        self.ADD_MODE=0;
        self.DELETE_MODE=1;
        
        # log in frame
        log=Mainframe();
        self.user="";
        self.channel="";
        self.loginSuccess=False;
        log.signal.connect(self.getLoginStatus);
        log.user.connect(self.getUserName);
        log.channel.connect(self.getChannel);
        log.exec_();
        
        # add friend frame
        self.friendChange=False;
        self.friendList=QTextEdit(self);
        
        # chatting
        self.channelText=QLineEdit(self);
        self.typeText=QTextEdit(self);
        self.showText=QTextEdit(self);
        
        if(self.loginSuccess):
            self.receiver=Receiver(self);
            self.receiver.daemon=True;
            self.receiver.start();
            self.initUI();
        else:
            self.close();
    
    def checkHistoryLog(self):
        if(not os.path.exists("history.json")):
            with open("history.json",'w',encoding="utf-8") as f:
                json.dump({},f);

    def closeEvent(self,event):
        self.checkHistoryLog();
        history=None;
        historyLog=self.showText.toPlainText().split('\n');
        with open("history.json",'r',encoding="utf-8") as f:
            history=json.load(f);
            history[self.channel]=history.get(self.channel,[])+historyLog;
        with open("history.json",'w',encoding="utf-8") as f:
            json.dump(history,f);
    
    def getChannel(self,channel):
        self.channel=channel if(channel) else "IPFS";
    
    def getUserName(self,name):
        self.user=name;
    
    def getLoginStatus(self,status):
        self.loginSuccess=bool(status);
        
    def getAddFriendStatus(self,status):
        self.friendChange=bool(status);
    
    def loadImage(self,image):
        if(image):
            imageLoader=ImageLoader(image);
            imageLoader.exec_();
    
    def addFriend(self):
        addFriendDialog=FriendDialog(self.api,self.ADD_MODE);
        addFriendDialog.signal.connect(self.getAddFriendStatus);
        addFriendDialog.exec_();
        if(self.friendChange):
            self.changeFriendList();
    
    def deleteFriend(self):
        deleteFriendDialog=FriendDialog(self.api,self.DELETE_MODE);
        deleteFriendDialog.signal.connect(self.getAddFriendStatus);
        deleteFriendDialog.exec_();
        if(self.friendChange):
            self.changeFriendList();
    
    def clearFriend(self):
        reply=QMessageBox.information(self,"Warning","Are you sure you want to clear your friend list?",QMessageBox.Yes,QMessageBox.No);
        if(reply==QMessageBox.Yes):
            self.api.bootstrap_rm(self.api.bootstrap_list()["Peers"]);
            QMessageBox.information(self,"Success","Clear peer success.",QMessageBox.Ok,QMessageBox.Ok);
            self.changeFriendList();
    
    def changeFriendList(self):
        self.friendList.clear();
        addrList=[addr.split('/')[-1] for addr in self.api.bootstrap_list()["Peers"]];
        self.friendList.setText("\n\n".join(addrList));
        self.friendChange=False;
    
    def viewHistory(self):
        historyDialog=ViewHistory(self.channel);
        historyDialog.exec_();
        
    def sendImage(self):
        fileType="Bmp(*.bmp);;Jpg(*.jpg);;Jpeg(*.jpeg);;Png(*.png);;Gif(*.gif);;Icon(*.icon)";
        directory=QFileDialog.getOpenFileName(self,"Select image","./",fileType)[0];
        ret=self.api.add(directory);
        content={};
        content["Type"]="Image";
        content["Hash"]=ret["Hash"];
        content["Name"]=ret["Name"];
        self.sendMessage(content["Type"]+'--'+content["Name"]+'--'+content["Hash"]);
        
    def sendText(self):
        fileType="Txt(*.txt);;Docx(*.docx);;Excel(*.xlsx)";
        directory=QFileDialog.getOpenFileName(self,"Select image","./",fileType)[0];
        ret=self.api.add(directory);
        content={};
        content["Type"]="Text";
        content["Hash"]=ret["Hash"];
        content["Name"]=ret["Name"];
        self.sendMessage(content["Type"]+'--'+content["Name"]+'--'+content["Hash"]);
    
    def sendFile(self):
        fileType="Zip(*.zip);;Rar(*.rar);;7z(*.7z)";
        directory=QFileDialog.getOpenFileName(self,"Select file","./",fileType)[0];
        ret=self.api.add(directory);
        content={};
        content["Type"]="File";
        content["Hash"]=ret["Hash"];
        content["Name"]=ret["Name"];
        self.sendMessage(content["Type"]+"--"+content["Name"]+"--"+content["Hash"]);
         
    def sendMessage(self,content=""):
        if(not content):
            content=self.typeText.toPlainText();
            if(not content):
                QMessageBox.information(self,"Error","Content must not be empty.",QMessageBox.Ok,QMessageBox.Ok);
                return;
            content="Message--"+content;
        self.api.pubsub_pub(self.channel,self.user+':'+content);
        self.typeText.clear();
        
    def initUI(self):
        # set window
        self.setFixedSize(QSize(1000,640)); # width, height
        self.setWindowTitle("IPFS Communication Program");
        self.setWindowIcon(QIcon("IPFS.png"));
        
        # set background image
        self.setWindowOpacity(1);
        palette=QPalette();
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap("IPFS_bg2.jpg")));
        self.setPalette(palette);
        
        # friend list
        friLabel=QLabel(self);
        friLabel.move(10,0);
        friLabel.resize(180,30);
        friLabel.setText("Friend list");
        friLabel.setStyleSheet("color:#ffffff;border :3px ;font-weight:bold;");
        
        self.friendList.move(10,30);
        self.friendList.resize(360,550);
        self.friendList.setEnabled(False);
        self.friendList.setStyleSheet("color:#000000;border :1px ;background-color:rgba(250,250,250,0.7)");
        addrList=[addr.split('/')[-1] for addr in self.api.bootstrap_list()["Peers"]];
        self.friendList.setText("\n\n".join(addrList));
        
        addBtn=QPushButton(self);
        addBtn.setIcon(QIcon("friend.icon"));
        addBtn.setToolTip("Add friend");
        addBtn.move(10,590);
        addBtn.resize(40,40);
        addBtn.clicked.connect(self.addFriend);
        
        deleteBtn=QPushButton(self);
        deleteBtn.setIcon(QIcon("unfriend.icon"));
        deleteBtn.setToolTip("Delete friend");
        deleteBtn.move(70,590);
        deleteBtn.resize(40,40);
        deleteBtn.clicked.connect(self.deleteFriend);
        
        clearBtn=QPushButton(self);
        clearBtn.setIcon(QIcon("clear.icon"));
        clearBtn.setToolTip("Clear friend list");
        clearBtn.move(130,590);
        clearBtn.resize(40,40);
        clearBtn.clicked.connect(self.clearFriend);
        
        # slogan
        memorial1=QLabel(self);
        memorial1.move(180,575);
        memorial1.resize(235,40);
        memorial1.setText("Prophecy is uncertain,");
        memorial1.setStyleSheet("color:#ffffff;border :3px ;font-weight:bold;");

        memorial2=QLabel(self);
        memorial2.move(200,600);
        memorial2.resize(215,40);
        memorial2.setText("There is always hope.");
        memorial2.setStyleSheet("color:#ffffff;border :3px ;font-weight:bold;");
    
        # chatting
        # channel selection
        channelLabel=QLabel(self);
        channelLabel.move(400,0);
        channelLabel.resize(60,30);
        channelLabel.setText("Channel");
        channelLabel.setStyleSheet("color:#ffffff;border :3px ;font-weight:bold;");
            
        self.channelText.move(500,0);
        self.channelText.resize(280,30);
        self.channelText.setText(self.channel);
        self.channelText.setEnabled(False);
        self.channelText.setStyleSheet("color:#000000;border :1px ;background-color:rgba(250,250,250,0.7)");
            
        # chatting content
        self.showText.move(400,40);
        self.showText.resize(580,400);
        self.showText.setStyleSheet("color:#000000;border :1px ;font-size:20px;background-color:rgba(250,250,250,0.7)")
        
        # view history
        historyBtn=QPushButton(self);
        historyBtn.setIcon(QIcon("history.icon"));
        historyBtn.setToolTip("View history");
        historyBtn.move(580,450);
        historyBtn.resize(40,40);
        historyBtn.clicked.connect(self.viewHistory);
            
        # typing content
        self.typeText.move(400,500);
        self.typeText.resize(580,130);
        self.typeText.setStyleSheet("color:#000000;border :1px ;font-size:20px;background-color:rgba(250,250,250,0.7)");
        
        sendBtn=QPushButton(self);
        sendBtn.setIcon(QIcon("send.icon"));
        sendBtn.setToolTip("Send message");
        sendBtn.move(940,450);
        sendBtn.resize(40,40);
        sendBtn.clicked.connect(self.sendMessage);
        
        # file transmission
        imgBtn=QPushButton(self);
        imgBtn.setIcon(QIcon("image.icon"));
        imgBtn.setToolTip("Send image");
        imgBtn.move(400,450);
        imgBtn.resize(40,40);
        imgBtn.clicked.connect(self.sendImage);
        
        txtBtn=QPushButton(self);
        txtBtn.setIcon(QIcon("txt.icon"));
        txtBtn.setToolTip("Send txt");
        txtBtn.move(460,450);
        txtBtn.resize(40,40);
        txtBtn.clicked.connect(self.sendText);

        fileBtn=QPushButton(self);
        fileBtn.setIcon(QIcon("file.icon"));
        fileBtn.setToolTip("Send file");
        fileBtn.move(520,450);
        fileBtn.resize(40,40);
        fileBtn.clicked.connect(self.sendFile);
        
        # show window
        self.show();

if(__name__=="__main__"):
    app=QApplication(sys.argv);  
    gui=GUI();
    sys.exit(app.exec_());
