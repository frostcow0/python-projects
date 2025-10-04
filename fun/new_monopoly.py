# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 20:31:50 2021

@author: gamet
"""

import pandas as pd
import logging
from dataclasses import dataclass
import os

@dataclass
class Game():
    end_flag:bool = False
    valid_input:bool = True
    output:str = "None"
    prev_command:str = "welcome/to/monopoly!"
    players:dict = {}
    properties:dict = {}

class Bank():
    def check_command(self, game:Game):
        action = game.prev_command.split('/')[0]
        commands={
            "pay":self.pay, # pay/sender/receiver/amount
            "buy":self.buy, # buy/customer/property or "dome"
            "trade":self.trade, # trade/customer/owner/property
            "end":self.end} # end
        commands[action](game)

    def pay(self, game=Game):
        nput = game.prev_command.split('/')
        if len(nput)==4:
            _, sender, receiver, amount = nput
            if sender=="bank": # Bank pays someone for community chest or chance.
                game.players.get(receiver).balance += int(amount)
            else: # People payin people
                game.players.get(sender).balance -= int(amount) # Sender
                game.players.get(receiver).balance += int(amount) # Receiver

    def buy(self, game=Game):
        nput = game.prev_command.split('/')
        if len(nput)==3:
            _, customer, prop = nput
            if prop=="dome":
                if game.players.get(customer):
                    game.players[customer].domes += 1
            elif game.properties.get(prop) and game.players.get(customer):
                game.players[customer].properties[prop] = game.properties[prop]

    def trade(self):
        pass

    def end(self):
        pass


class Player():
    def __init__(self, name:str, balance:int):
        self.name = name
        self.balance = balance
        self.properties = {}
        self.resources = 0
        self.domes = 0

def print_state(state:pd.DataFrame):
    print(state)
    print('-'*60)

def clear():
    """Clears the stdout"""
    os.system("cls")



# def wait(bad_input:bool=False, message:str=None):
#     print(self.df)
#     print('-'*30)
#     print('last input : ',self.prev_command)
#     if bad_input==True:
#         print(message)
#     print('-'*30)
#     nput=input(" : ")
#     self.prev_command=nput
#     nput=nput.split('/')
#     if len(nput)==1:
#         self.command_usage(nput[0])
#     self.check_command(nput)


def main(n_players:int, start_bal:int):
    clear()
    bank = Bank()
    game = Game()
    names = [input(f"Who is player {i}? : ") for i in range(1, n_players+1)]
    game.players = {x:Player(name=x, balance=start_bal) for x in names}
    state = pd.DataFrame({
        "Balance": [player.balance for player in game.players],
        "Resources": [player.resources for player in game.players],
        "Domes": [player.domes for player in game.players]
    }, index=[player.name for player in game.players])

    while not game.end_flag:
        clear()
        print_state(state=state)
        print(f"last input : {game.prev_command}")
        if not game.valid_input:
            print("bad")
        print('-'*60)
        # output = check_command(input(" : "))
        game.prev_command = input(" : ")
        bank.check_command(game=game)
        # check_command(game=game, bank=bank)
        # self.prev_command=nput
        # nput=nput.split('/')
        # if len(nput)==1:
        #     self.command_usage(nput[0])
        # self.check_command(nput)
        # game.end_flag = True

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s: %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S")

    main(n_players=2, start_bal=900)


# class Bank():
#     def __init__(self,num_users,start_bal):
#         format = "%(asctime)s: %(message)s"
#         logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#         clear()
#         self.num_users=num_users
#         self.start_bal=start_bal
#         self.nicknames=[]
#         self.prev_command=None
#         self.df=None
#         self.properties=[
#             {'Name':'Neptune Ring of whatever','Rent':10,'Colorset Rent':30,'Dome Rent':40},
#             {}
#         ]
#         self.get_nicks()
#         self.init_frame()

#     def init_properties(self):
#         for k in self.properties:
#             p.append(Property(k['Name'],k['Rent'],k['Colorset Rent'],k['Dome Rent']))
#         print(p)

#     def get_nicks(self):
#         for i in range(self.num_users):
#             self.nicknames.append(input("Who is player {}? : ".format(i+1)))

#     def init_frame(self):
#         d={"Balance":self.start_bal,"Resources":0,'Domes':0}
#         self.df=pd.DataFrame(data=d,index=self.nicknames)
#         self.wait()

#     def wait(self,bad_input=False,message=None):
#         clear()
#         print(self.df)
#         print('-'*30)
#         print('last input : ',self.prev_command)
#         if bad_input==True:
#             print(message)
#         print('-'*30)
#         nput=input(" : ")
#         self.prev_command=nput
#         nput=nput.split('/')
#         if len(nput)==1:
#             self.command_usage(nput[0])
#         self.check_command(nput)

#     def check_command(self,nput):
#         commands={"pay":self.pay, # pay/sender/receiver/amount
#                   "buy":self.buy, # buy/customer/property or "dome"
#                   "trade":self.trade, # trade/customer/owner/property
#                   'end':self.end} # end
#         commands[nput[0]](nput[1::])

#     def command_usage(self,nput):
#         message=None
#         if nput=='pay':
#             message='*** correct usage: pay/sender/receiver/amount'
#         elif nput=='buy':
#             message='*** correct usage: buy/customer/property or "dome"'
#         elif nput=='trade':
#             message='*** correct usage: trade/customer/owner/property'
#         else:
#             logging.info('Not a command. Try again.')
#         self.wait(True,message)

#     def pay(self,nput):
#         try:
#             if nput[0]=='bank': # Bank pays someone for community chest or chance.
#                 #self.df.iloc[self.nicknames.index(nput[1])][0]+=int(nput[2])
#                 self.df.loc[nput[1]][0]+=int(nput[2])
#             else:
#                 self.df.loc[nput[0]][0]-=int(nput[2]) # Sender
#                 self.df.loc[nput[1]][0]+=int(nput[2]) # Receiver
#         except:
#             self.command_usage('pay')
#         self.wait()

#     def buy(self,nput): 
#         try:
#             if nput[1]=='dome':
#                 if self.df.iloc[self.nicknames.index(nput[0])]:
#                     print('construction')
#                 print('ok')
#         except:
#             pass

#     def trade(self,nput):
#         try:
#             pass
#         except:
#             pass
        
#     def end(self):
#         pass

# class Property():
#     def __init__(self,name,rent,colorset_rent,dome_rent,owner=None):
#         self.name=name
#         self.rent=rent
#         self.colorset_rent=colorset_rent
#         self.dome_rent=dome_rent
#         self.owner=owner

#     def new_owner(self,owner):
#         self.owner=owner

# def clear():
#     """Clears the stdout"""
#     os.system('cls')

# p=[]
# b=Bank(2,900)
