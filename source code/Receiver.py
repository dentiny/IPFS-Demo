# -*- coding: utf-8 -*-

import os;
import base64;
import threading;
from PyQt5.QtCore import pyqtSignal;

class Receiver(threading.Thread):
    imageReceived=pyqtSignal(str);
    
    def __init__(self,gui):
        threading.Thread.__init__(self);
        self.gui=gui;
    
    def run(self):
        self.receiveMessage(self.gui);
    
    def receiveMessage(self,gui):
        api=self.gui.api;
        topic=gui.channel;
        while(True):
            with api.pubsub_sub(topic,discover=True) as sub:
                for message in sub:
                    data=base64.b64decode(message["data"]).decode("utf-8"); # str(format(base64.b64decode(message["data"])))
                    
                    try:
                        author=data.split('--')[0].split(':')[0];
                        messageType=data.split('--')[0].split(':')[1];
                    
                        # receive image
                        if(messageType=="Image"):
                            image=data.split('--')[1];
                            hashkey=data.split('--')[2];
                            api.get(hashkey);
                            while(not os.path.exists(hashkey)):
                                continue;
                            try:
                                os.rename(hashkey,image);
                            except:
                                pass;
                            self.gui.showText.append(author+': send an image');
                    
                        # receive text
                        elif(messageType=="Text"):
                            text=data.split('--')[1];
                            hashkey=data.split('--')[2];
                            api.get(hashkey);
                            while(not os.path.exists(hashkey)):
                                continue;
                            try:
                                os.rename(hashkey,text);
                            except:
                                pass;
                            self.gui.showText.append(author+': send a text');
                            
                        # receive file
                        elif(messageType=="File"):
                            file=data.split('--')[1];
                            hashkey=data.split('--')[2];
                            api.get(hashkey);
                            while(not os.path.exists(hashkey)):
                                continue;
                            try:
                                os.rename(hashkey,file);
                            except:
                                pass;
                            self.gui.showText.append(author+": send a file");
                    
                        # receive message
                        else:
                            message=data.split('--')[1];
                            self.gui.showText.append(author+':'+message);
                            
                    except:
                        self.gui.showText.append(data);