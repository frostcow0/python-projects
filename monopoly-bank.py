# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 20:31:50 2021

@author: gamet
"""

import pandas as pd
import logging
import os

class Bank():
    def __init__(self,num_users,start_bal):
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
        
        self.num_users=num_users
        self.start_bal=start_bal
        self.nicknames=[]
        self.prev_command=None
        self.get_nicks()
        clear()
        self.init_frame()
        self.df=None
        
    def get_nicks(self):
        for i in range(self.num_users):
            self.nicknames.append(input("Who is player {}? : ".format(i+1)))
            
    def init_frame(self):
        d={"Balance":self.start_bal,"Resources":0}
        self.df=pd.DataFrame(data=d,index=self.nicknames)
        self.wait()
        
    def wait(self):
        clear()
        print(self.df)
        print('-'*30)
        print('last input : ',self.prev_command)
        print('-'*30)
        nput=input(" : ")
        self.prev_command=nput
        nput=nput.split(' ')
        if len(nput)==1:
            self.command_usage(nput)
        self.check_command(nput)
        
    def check_command(self,nput):
        commands={"pay":self.pay,
                  "buy":self.buy,
                  "trade":self.trade}
        commands[nput[0]](nput[1::])
        
    def command_usage(self,nput):
        if nput=='pay':
            pass
        elif nput=='buy':
            pass
        elif nput=='trade':
            pass
        else:
            logging.info('Not a command. Try again.')
        self.wait()
        
        
    def pay(self,nput):
        try:
            if nput[0]=='bank': # Bank pays someone for community chest or chance.
                self.df.iloc[self.nicknames.index(nput[1])][0]+=int(nput[2])
            else:
                self.df.iloc[self.nicknames.index(nput[0])][0]-=int(nput[2]) # Sender
                self.df.iloc[self.nicknames.index(nput[1])][0]+=int(nput[2]) # Receiver
        except IndexError:
            self.prev_commands.append(logging.info('Error, not enough values.'))
        self.wait()
        
    def buy(self,nput):
        print('buy')
        
    def trade(self,nput):
        print('buy')
        
    def end(self):
        pass
        
clear=lambda:os.system('cls')
            
b=Bank(2,900)
        