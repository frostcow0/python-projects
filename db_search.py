# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 18:34:36 2021

@author: gamet
"""
try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from collections import Counter

#title = 'DB Search'
title = 'Columns'

# Tables
bp_subscriber_product = ['sub_id', 'subscriber', 'feature 1', 'feature 2']
bp_subscriber = ['sub_id', 'subscriber', 'market', 'address', 'email']

v_sub = ['sub_id', 'subscriber', 'market', 'mrkt_typ']
# Databases
dwh1 = {
        'bp_subscriber': bp_subscriber,
        'bp_subscriber_product': bp_subscriber_product,
        }
qcc1 = {
        'v_sub': v_sub,
        }

db_ref = {
        'dwh1': dwh1,
        'qcc1': qcc1,
        }

table_ref = {}
for db in db_ref.values():
    for table in db.keys():
        table_ref[table] = db[table]

columns = []
for db in db_ref.values():
    for column in db.values():
        columns = columns + list(set(column)-set(columns))

def create_app():
    root=Tk() #Creates the Window
    root.title(title) #Title at the Top
    app=Lbox(root) #Runs Presser or Lbox
    root.mainloop() #Runs Tkinter (Doesn't run anything after this until the window is closed)

class Lbox(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.yscrollbar = Scrollbar(master)
        self.yscrollbar.pack(side = RIGHT, fill = Y)
        self.label = Label(master,
                   text = 'Select from the columns below :  ',
                   font = ('Veridian', 16),
                   padx = 3, pady = 3)
        self.label.pack()
        self.list = Listbox(master, selectmode = 'multiple',
                            yscrollcommand = self.yscrollbar.set)
        self.list.pack(padx = 10, pady = 10,
                  expand = YES, fill = 'both')

        self.button = Button(master,
                  text = 'Enter',
                  font = ('Veridian', 12),
                  padx = 3, pady = 3,
                  command = self.get)
        self.button.pack()
        
        for column in columns:
            self.list.insert(END, column)
        self.yscrollbar.config(command = self.list.yview)
        
    def get(self):
        options = []

        for i in self.list.curselection():
            choice = self.list.get(i)
            for db in db_ref.keys():
                for table in db_ref[db].keys():
                    if choice in db_ref[db][table]:
                        options.append((db, table, choice))
        print(options)
        self.joins(options)
        
    def joins(self, options):
        joins = []
        print(options[0])
        dbs = list(set(options[x][0] for x in range(len(options))))
        for i in range(len(dbs)):
            print(i)
            for col1 in table_ref[options[i][1]]:
                table1 = options[i][1]
                print(f'col 1 - {col1}')
                print(f'table 1 - {table1}')
                for col2 in table_ref[options[i][1]]:
                    table2 = options[i][1]
                    print(f'col 2 - {col2}')
                    print(f'table 2 - {table2}')
                    print(f'choice - {options[i][2]}')
                    if col1 == col2: # choice
                        #joins.append(options[i])
                        print('appended')
                        joins.append((dbs[i], table2, options[i][2], col1))
                        
                        
        print(joins)
        # Tally by table in joins, majority wins for that column
        # Not sure that the tally count is correct, needs to count by joins[i][3]
        tally = dict(Counter(joins))
        print(tally)
        count = list(tally.values())
        location = list(tally.keys())
        print(location[count.index(max(count))]) # need the matching table name
        
        
        
        
create_app()