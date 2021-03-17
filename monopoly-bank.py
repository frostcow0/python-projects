# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 20:31:50 2021

@author: gamet
"""

import pandas as pd
import os

class Bank():
    def __init__(self,num_users,start_bal):
        self.num_users=num_users
        self.start_bal=start_bal
        self.nicknames=[]
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
        print(self.df)
        print('-'*30)
        self.wait()
        
    def wait(self):
        nput=input(" : ").split(' ')
        self.check_command(nput)
        
    def check_command(self,nput):
        commands={"pay":self.pay,
                  "buy":self.buy,
                  "trade":self.trade}
        commands[nput[0]](nput[1::])
        
    def pay(self,nput):
        send_bal=self.df.iloc[self.nicknames.index(nput[0])][0]
        receive_bal=self.df.iloc[self.nicknames.index(nput[1])][0]
        send_bal=int(send_bal)-int(nput[2])
        receive_bal=int(receive_bal)+int(nput[2])
        clear()
        print(self.df)
        print('-'*30)
        self.wait()
        
    def buy(self,nput):
        print('buy')
        
    def trade(self,nput):
        print('buy')
        
clear=lambda:os.system('cls')
            
b=Bank(2,900)
        