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

#title = 'DB Search'
title = 'Columns'
class Database():
    def __init__(self, name, ref):
        self.name = name
        self.tables = self.build_tables(ref)

    def __str__(self):
        return str(self.name)

    def build_tables(self, ref):
        tables = []
        for table in ref.keys():
            tables.append(Table(table, ref[table], self))
        return tables

    def get_req_tables(self, choices_tables):
        req_tables = {}
        while len(choices_tables.keys())>0:
            choices = [x for x in choices_tables.keys()]
            table_score = self.build_table_score(choices_tables) #build_table_score(choices_tables)
            table = self.keywithmaxval(table_score) # t1
            for choice in choices:
                if choice in table_ref[table]:
                    del choices_tables[choice]
                    if table not in req_tables:
                        req_tables[table] = [choice]
                    else:
                        req_tables[table].append(choice)
        for table, choices in req_tables.items():
            print(table, choices)
        self.build_query(req_tables)

    def build_table_score(self, choices_tables):
        table_score = {};
        choices = choices_tables.keys()
        for choice in choices:
            tables = choices_tables[choice] # array of found_in_tables
            for table in tables:
                if table not in table_score.keys():
                    table_score[table] = 1
                else:
                    table_score[table] += 1
        return table_score

    def keywithmaxval(self, d):
        #print(f'incoming table_score - {table, choices}')
        """ a) create a list of the dict's keys and values; 
            b) return the key with the max value"""  
        v=list(d.values())
        k=list(d.keys())
        return k[v.index(max(v))]

    def build_query(self, req_tables):
        pass
        for table, choices in req_tables.items():
            if table.columns in table.columns.next():
                print("yippe")
                    

class Table():
    def __init__(self, name, columns, database):
        self.name = name
        self.columns = columns
        self.database = database

    def __str__(self):
        return str(self.name)

    def join(self, table2):
        potential_join = ''
        for column in self.columns:
            if column in table2.columns:
                potential_join = column
                break

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
        self.columns = self.unique_columns()
        for column in self.columns:
            self.list.insert(END, column)
        self.yscrollbar.config(command = self.list.yview)
    
    def unique_columns(self):
        columns = []
        for db in db_ref.values():
            for table in db.tables:
                columns = columns + list(set(table.columns)-set(columns))
        return columns
        
    def get(self):
        for db in db_ref.keys():
            obj = db_ref[db]
            choices_tables = {};
            for i in self.list.curselection():
                choice = self.list.get(i)
                for table in db_ref[db].tables:
                    if choice in table.columns:
                        if choice not in choices_tables.keys():
                            choices_tables[choice] = [table]
                        else:
                            choices_tables[choice].append(table)
            obj.get_req_tables(choices_tables)
        
        #print(options)
        #self.joins(options)
        
    def joins(self, options):
        joins = []
        print(options[0])
        dbs = list(set(options[x][0] for x in range(len(options))))
        for i in range(len(options)):
            print(i)
            for col1 in table_ref[options[i][1]]: # table_ref[options[i][1]] -> table, for column in table
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
                        choices[options[i][2]].append(table1)
                        
                        
        print(joins)
        # Tally by table in joins, majority wins for that column
        # Not sure that the tally count is correct, needs to count by joins[i][3]
        tally = dict(Counter(joins))
        print(tally)
        count = list(tally.values())
        location = list(tally.keys())
        print(location[count.index(max(count))]) # need the matching table name
        
        
        

dwh1_db = Database('dwh1', dwh1)

db_ref = {
        'dwh1': dwh1_db,
        }

table_ref = {}
for db in db_ref.values():
    for table in db.tables:
        table_ref[table] = table.columns

create_app()