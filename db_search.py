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
import pandas
import cx_Oracle



# Tables
bp_subscriber_product = ['SUBSCRIBER_ID', 'SUBSCRIBER', 'feature_1', 'feature_2']
bp_subscriber = ['SUBSCRIBER_ID', 'SUBSCRIBER', 'SUBSCRIBER_COMPANY_NAME', 'MARKET', 'BUSINESS_UNIT', 'SUSBCRIBER_STATUS', 'SUBSCRIBER_STATE',
                'SERVICE_COMBINATION', 'SERVICE_SET', 'SERVICE_START_DATE', 'SUBSCRIBER_END_DATE', 'BUILDING_TYPE']

v_sub = ['sub_id', 'subscriber', 'market', 'mrkt_typ']
# Databases
dwh1 = {
        'bp_subscriber': bp_subscriber,
        'bp_subscriber_product': bp_subscriber_product,
        }
qcc1 = {
        'v_sub': v_sub,
        }

class Database():
    def __init__(self, name, ref):
        self.name = name
        self.tables = self.build_tables(ref)
        self.init_db_connection()

    def create_popup(self, query):
        root=Tk() #Creates the Window
        root.title('How do you want to Export?') #Title at the Top
        app=Popup(root, query) #Runs Presser or Lbox
        root.mainloop()

    def __str__(self):
        return str(self.name)

    def init_db_connection(self):
        try:
            dsn_tns = cx_Oracle.makedsn('HOSTNAME', 'PORTNUMBER', service_name = 'SERVICENAME', )
            self.connection = cx_Oracle.connect(
                user = "jmartin",
                password = "", # put in later
                dsn = dsn_tns)
            self.cursor = self.connection.cursor()
        except Exception as error:
            print("Couldn't connect to the database. -- "+repr(error))

    def execute_query(self, query):
        data = self.cursor.execute(query)
        return data

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
        """ a) create a list of the dict's keys and values; 
            b) return the key with the max value"""  
        v=list(d.values())
        k=list(d.keys())
        return k[v.index(max(v))]

    def build_query(self, req_tables):
        query = ''
        if len(req_tables) == 1:
            for table, choices in req_tables.items():
                query += 'SELECT\n\t'
                for choice in choices:
                    query += f'{choice}, '
                query = query[:len(query) - 2]
                query += f'\nFROM\n\t{table}'
        else: 
            joins = self.join([x for x in req_tables.keys()])
            select = 'SELECT\n\t'
            frm = '\nFROM\n\t'
            where = ''
            i = 0
            keyword = '\nWHERE '
            for table, choices in req_tables.items():
                for choice in choices:
                    select += f'{table}.{choice}, '
                
                frm += f'{table}, '
            select = select[:len(select) - 2]
            frm = frm[:len(frm) - 2]
            for table1, container in joins.items():
                for table2, common in container:
                    if i == 1:
                        keyword == '\nAND '
                    else:
                        i += 1
                    where += keyword
                    where += f'{table1.name}.{common} = {table2}.{common}'
            query += select + frm + where
        print('='*60)
        print(query)
        self.create_popup(query)

    def join(self, tables):
        from collections import defaultdict
        joins = defaultdict(list)
        for i, table1 in enumerate(tables):
            if i == len(tables)-1:
                break
            for j, table2 in enumerate(tables[i+1:]):
                common = list(set(table1.columns).intersection(set(table2.columns)))
                if common:
                    joins[table1].append((table2, common[0]))
            if not joins[table1]:
                x = False
                for j, table2 in enumerate(tables):
                    if table2 == table1: 
                        continue
                    if x:
                        break
                    for k, table3 in enumerate(self.tables):
                        if table3 == table1 or table3 == table2:
                            continue
                        common1 = list(set(table1.columns).intersection(set(table3.columns)))
                        common2 = list(set(table2.columns).intersection(set(table3.columns)))
                        if common1 and common2:
                            joins[table1].append((table3, common1[0])) # maybe ?
                            joins[table2].append((table3, common2[0]))
                            x = True
                            break
                if not x:
                    raise(f"Nothing in common found for {table1}")
        return joins

class Table():
    def __init__(self, name, columns, database):
        self.name = name
        self.columns = columns
        self.database = database

    def __str__(self):
        return str(self.name)

    def name(self):
        return str(self.name)

def create_app():
    root=Tk() #Creates the Window
    root.title('Query Builder') #Title at the Top
    app=Lbox(root) #Runs Presser or Lbox
    root.mainloop() #Runs Tkinter (Doesn't run anything after this until the window is closed)

class Lbox(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
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

class Popup(Frame):
    def __init__(self, master, query):
        Frame.__init__(self, master)
        self.query = query
        self.pack()
        self.place_buttons()
        
    def place_buttons(self):
        self.sql = Button(self,
                  text = 'SQL Query',
                  font = ('Veridian', 12),
                  padx = 3, pady = 3,
                  command = self.export_sql_query)
        self.sql.pack()
        self.xlsx = Button(self,
                  text = 'Excel',
                  font = ('Veridian', 12),
                  padx = 3, pady = 3,
                  command = self.export_xlsx)
        self.xlsx.pack()
        self.csv = Button(self,
                  text = 'CSV',
                  font = ('Veridian', 12),
                  padx = 3, pady = 3,
                  command = self.export_xlsx)
        self.csv.pack()

        self.widgets = [self.sql, self.xlsx, self.csv]

    def back(self):
        for widget in self.widgets:
            widget.pack_forget()
        self.place_buttons()
    
    def export_sql_query(self):
        for widget in self.widgets:
            widget.pack_forget()
        self.text = Text(self,
                        height = 10,
                        width = 60,
                        font = ("Veridian", 10),
                        padx = 3, pady = 3)
        self.text.pack()
        self.back_button = Button(self,
                  text = 'Back',
                  font = ('Veridian', 12),
                  padx = 3, pady = 3,
                  command = self.back)
        self.back_button.pack()

        self.text.insert(END, self.query)

        self.widgets = [self.text, self.back_button]

    def export_xlsx(self):
        for widget in self.widgets:
            widget.pack_forget()
        pass

    def export_csv(self):
        for widget in self.widgets:
            widget.pack_forget()
        pass

dwh1_db = Database('dwh1', dwh1)

db_ref = {
        'dwh1': dwh1_db,
        }

table_ref = {}
for db in db_ref.values():
    for table in db.tables:
        table_ref[table] = table.columns

create_app()