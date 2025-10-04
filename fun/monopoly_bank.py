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
        clear()
        self.num_users=num_users
        self.start_bal=start_bal
        self.nicknames=[]
        self.prev_command=None
        self.df=None
        self.properties=[
            {'Name':'Neptune Ring of whatever','Rent':10,'Colorset Rent':30,'Dome Rent':40},
            {}
        ]
        self.get_nicks()
        self.init_frame()

    def init_properties(self):
        for k in self.properties:
            p.append(Property(k['Name'],k['Rent'],k['Colorset Rent'],k['Dome Rent']))
        print(p)

    def get_nicks(self):
        for i in range(self.num_users):
            self.nicknames.append(input("Who is player {}? : ".format(i+1)))

    def init_frame(self):
        d={"Balance":self.start_bal,"Resources":0,'Domes':0}
        self.df=pd.DataFrame(data=d,index=self.nicknames)
        self.wait()

    def wait(self,bad_input=False,message=None):
        clear()
        print(self.df)
        print('-'*30)
        print('last input : ',self.prev_command)
        if bad_input==True:
            print(message)
        print('-'*30)
        nput=input(" : ")
        self.prev_command=nput
        nput=nput.split('/')
        if len(nput)==1:
            self.command_usage(nput[0])
        self.check_command(nput)

    def check_command(self,nput):
        commands={"pay":self.pay, # pay/sender/receiver/amount
                  "buy":self.buy, # buy/customer/property or "dome"
                  "trade":self.trade, # trade/customer/owner/property
                  'end':self.end} # end
        commands[nput[0]](nput[1::])

    def command_usage(self,nput):
        message=None
        if nput=='pay':
            message='*** correct usage: pay/sender/receiver/amount'
        elif nput=='buy':
            message='*** correct usage: buy/customer/property or "dome"'
        elif nput=='trade':
            message='*** correct usage: trade/customer/owner/property'
        else:
            logging.info('Not a command. Try again.')
        self.wait(True,message)

    def pay(self,nput):
        try:
            if nput[0]=='bank': # Bank pays someone for community chest or chance.
                #self.df.iloc[self.nicknames.index(nput[1])][0]+=int(nput[2])
                self.df.loc[nput[1]][0]+=int(nput[2])
            else:
                self.df.loc[nput[0]][0]-=int(nput[2]) # Sender
                self.df.loc[nput[1]][0]+=int(nput[2]) # Receiver
        except:
            self.command_usage('pay')
        self.wait()

    def buy(self,nput): 
        try:
            if nput[1]=='dome':
                if self.df.iloc[self.nicknames.index(nput[0])]:
                    print('construction')
                print('ok')
        except:
            pass

    def trade(self,nput):
        try:
            pass
        except:
            pass
        
    def end(self):
        pass

class Property():
    def __init__(self,name,rent,colorset_rent,dome_rent,owner=None):
        self.name=name
        self.rent=rent
        self.colorset_rent=colorset_rent
        self.dome_rent=dome_rent
        self.owner=owner

    def new_owner(self,owner):
        self.owner=owner

def clear():
    """Clears the stdout"""
    os.system('cls')

p=[]
b=Bank(2,900)
