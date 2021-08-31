# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 18:34:36 2021

@author: gamet
"""
try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from collections import Counter, defaultdict
import pandas
import cx_Oracle
import re

title = 'Query Builder'

# Tables
bp_subscriber_product = ['SUBSCRIBER_ID', 'SUBSCRIBER', 'feature_1', 'feature_2']
bp_subscriber = ['SUBSCRIBER_ID', 'SUBSCRIBER', 'SUBSCRIBER_COMPANY_NAME', 'MARKET', 'BUSINESS_UNIT', 'SUBSCRIBER_STATUS', 'SUBSCRIBER_STATE',
                'SERVICE_COMBINATION', 'SERVICE_SET', 'SERVICE_START_DATE', 'SUBSCRIBER_END_DATE', 'BUILDING_TYPE']

v_sub = ['sub_id', 'subscriber', 'market', 'mrkt_typ']
# Databases
# dwh1 = {
#         'bp_subscriber': bp_subscriber,
#         'bp_subscriber_product': bp_subscriber_product,
#         }
qcc1 = {
        'v_sub': v_sub,
        }

class Database():
    def __init__(self, name, host, port, tab_own):
        self.name = name
        if self.name == 'dwh1':
            self.schema = 'PROD'
        
        self.host = host
        self.port = port
        self.table_owner = tab_own
        self.login_info = []
        self.cursor = None
        self.schema = defaultdict(list)
        self.unique_columns = []
        self.init_db_connection()
        self.loading()

        self.tables = self.build_tables()
        self.pop_unique_columns()
        db_ref[self.name] = self

        create_app(1, self)

    def create_popup(self, query, option):
        root=Tk() #Creates the Window
        root.title(title) #Title at the Top
        raise_to_front(root)
        app=Popup(root, query, option) #Runs Presser or Lbox
        root.mainloop()

    def __str__(self):
        return str(self.name)

    def init_db_connection(self):
        self.login()
        try:
            dsn_tns = cx_Oracle.makedsn(self.host, self.port, service_name = self.name )
            self.connection = cx_Oracle.connect(
                user = self.login_info[0],
                password = self.login_info[1],
                dsn = dsn_tns)
            self.cursor = self.connection.cursor()
        except IndexError: # Closed with no entry
            quit()
        except Exception as error:
            self.create_popup(f"Couldn't connect to the database. -- {repr(error)}", 1)
            self.init_db_connection()

    def create_schema(self):
        query = f'''
        select
            table_name, column_name
        from dba_tab_cols
        where owner = '{self.table_owner}'
        order by table_name
        '''
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        while row:
            self.schema[row[0]].append(row[1])
            row = self.cursor.fetchone()
        del self.schema['ACES_CIRCUIT_COST']
        del self.schema['ACES_VENDOR_FILES']
        del self.schema['ADP_ROSTER_DATA_ALL']
        self.write_schema() #if we dont read, dont need write
        self.exit_popup()

    def write_schema(self):
        with open(f"schemas/schema_{self.name.upper()}", "w") as file:
            for table, columns in self.schema.items():
                file.write(table+"\n")
                for column in columns:
                    file.write("\t"+column+"\n")

    def read_schema(self): # much slower than just querying
        pattern = re.compile(r'\s')
        with open(f"schemas/schema_{self.name.upper()}") as file:
            last_table = ''
            while True:
                content = file.readline()
                if pattern.match(content):
                    #print("column")
                    self.schema[last_table].append(content.strip())
                else:
                    #print(content)
                    last_table = content[:len(content)-2]
                #print('='*60)
                #print(self.schema)

    def pop_unique_columns(self):
        query = f'''
        select distinct
            column_name
        from all_tab_cols
        where owner = '{self.table_owner}'
        '''
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        while row:
            self.unique_columns.append(row)
            row = self.cursor.fetchone()

    def loading(self):
        ref = {
            'create_schema': self.create_schema,
            'read_schema': self.read_schema,
        }

        if f"schemas/schema_{self.name.upper()}":
            message = f"Reading from schema_{self.name.upper()} . . ."
            func = ref['read_schema']
        else: 
            message = f"Loading from {self.name.upper()} . . ."
            func = ref['create_schema']

        message = f"Loading from {self.name.upper()} . . ."
        func = ref['create_schema']    
        root = Tk()
        raise_to_front(root)
        root.title('Loading DB Schema')
        root.geometry('400x50')
        self.popup = root
        label = Label(root,
                        text = message,
                        font = ("Verdana", 14))
        label.pack()
        root.after(200, func)
        root.mainloop()
        

    def login(self):
        root = Tk()
        root.title(title)
        top_frame = Frame(root)
        bot_frame = Frame(root)
        
        root.geometry('300x150')
        self.popup = root

        root.l0 = Label(root,
                   text = self.name.upper(),
                   font = ('Veridian', 15),
                   padx = 3, pady = 3)
        root.l0.pack(side = TOP, fill = X)
        top_frame.pack()
        bot_frame.pack()
        root.l1 = Label(root,
                   text = 'Username :  ',
                   font = ('Veridian', 12),
                   padx = 3, pady = 10)
        root.l1.pack(in_ = top_frame, side = LEFT)
        root.l2 = Label(root,
                   text = 'Password :  ',
                   font = ('Veridian', 12),
                   padx = 3, pady = 5)
        root.l2.pack(in_ = bot_frame, side = LEFT)
        root.user = Entry(root,
                        width = 15)
        root.user.pack(in_ = top_frame, side = RIGHT, fill = X)
        root.passw = Entry(root,
                        show = "*",
                        width = 15)
        root.passw.pack(in_ = bot_frame, side = RIGHT)
        root.passw.bind('<Return>', self.get_login)
        root.enter = Button(root,
                  text = 'Enter',
                  font = ('Veridian', 12),
                  padx = 3, pady = 3,
                  command = self.get_login)
        root.enter.pack(side = BOTTOM)
        
        root.mainloop()

    def get_login(self, obj=0):
        self.login_info.append(self.popup.user.get())
        self.login_info.append(self.popup.passw.get())
        self.exit_popup()

    def exit_popup(self):
        self.popup.destroy()

    def execute_query(self, query):
        data = self.cursor.execute(query)
        return data

    def build_tables(self):
        tables = []
        for table, columns in self.schema.items():
            tables.append(Table(table, columns, self))
        return tables

    def get_req_tables(self, choices_tables):
        req_tables = {}
        self.choice_table_key = {}
        while len(choices_tables.keys())>0:
            choices = [x for x in choices_tables.keys()]
            table_score = self.build_table_score(choices_tables) #build_table_score(choices_tables)
            table = self.keywithmaxval(table_score) # t1
            for choice in choices:
                if choice in self.tables[self.tables.index(table)].columns:
                    del choices_tables[choice]
                    if table not in req_tables:
                        req_tables[table.name] = [choice]
                        self.choice_table_key[choice] = table.name
                    else:
                        req_tables[table.name].append(choice)
                        self.choice_table_key[choice].append(table.name)
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
                query += f'\nFROM\n\t{self.table_owner}.{table}'
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
                frm += f'{self.table_owner}.{table}, '
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
        self.create_popup(query, 0)

    def join(self, tables):
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
                    self.create_popup(f"Nothing in common found for {table1}", 1)
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

def create_app(option, db):
    root=Tk() #Creates the Window
    root.title(title) #Title at the Top
    raise_to_front(root)
    if option == 0:
        root.geometry('200x100')
    app=Lbox(root, option, db) #Runs Presser or Lbox
    root.mainloop() #Runs Tkinter (Doesn't run anything after this until the window is closed)

class Lbox(Frame):
    def __init__(self, master, option, db):
        Frame.__init__(self, master)
        self.db = db
        self.option = option
        if self.option == 0:
            self.login()
        elif self.option == 1:
            self.choose_columns()
        
    def choose_columns(self):
        self.pack()
        self.yscrollbar = Scrollbar(self)
        self.yscrollbar.pack(side = RIGHT, fill = Y)
        self.label = Label(self,
                   text = 'Select from the columns below :  ',
                   font = ('Veridian', 16),
                   padx = 3, pady = 3)
        self.label.pack()
        self.list = Listbox(self, selectmode = 'multiple',
                            yscrollcommand = self.yscrollbar.set)
        self.list.pack(padx = 10, pady = 10,
                  expand = YES, fill = 'both')

        self.button = Button(self,
                  text = 'Enter',
                  font = ('Veridian', 12),
                  padx = 3, pady = 3,
                  command = self.get)
        self.button.pack()
        self.columns = self.db.unique_columns
        for column in self.columns:
            self.list.insert(END, column)
        self.yscrollbar.config(command = self.list.yview)
        
    def get(self):
        for db in db_ref.keys():
            obj = db_ref[db]
            choices_tables = {};
            for i in self.list.curselection():
                choice = self.list.get(i)[0]
                for table in db_ref[db].tables:
                    if choice in table.columns:
                        if choice not in choices_tables.keys():
                            choices_tables[choice] = [table]
                        else:
                            choices_tables[choice].append(table)
            obj.get_req_tables(choices_tables)

class Popup(Frame):
    def __init__(self, master, message, option):
        Frame.__init__(self, master)
        self.root = master
        self.message = message
        self.option = option
        
        self.pack()
        if self.option == 0:
            self.place_buttons()
        elif self.option == 1:
            self.error()

    def exit(self):
        self.root.destroy()

    def error(self):
        self.pack()
        self.lbl = Label(self,
                    text = self.message,
                    font = ('Veridian', 12),
                    padx = 3, pady = 3)
        self.lbl.pack()
        self.button = Button(self,
                    text = 'Exit',
                    font = ('Veridian', 12),
                    padx = 3, pady = 3,
                    command = self.exit)
        self.button.pack()

        self.widgets = [self.lbl, self.button]
        
    def place_buttons(self):
        self.sql = Button(self,
                  text = 'SQL Query',
                  font = ('Veridian', 12),
                  padx = 3, pady = 6,
                  command = self.export_sql_query)
        self.sql.pack()
        self.xlsx = Button(self,
                  text = 'Excel',
                  font = ('Veridian', 12),
                  padx = 3, pady = 6,
                  command = self.export_xlsx)
        self.xlsx.pack()
        self.csv = Button(self,
                  text = 'CSV',
                  font = ('Veridian', 12),
                  padx = 3, pady = 6,
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

        self.text.insert(END, self.message)

        self.widgets = [self.text, self.back_button]

    def export_xlsx(self):
        for widget in self.widgets:
            widget.pack_forget()
        pass

    def export_csv(self):
        for widget in self.widgets:
            widget.pack_forget()
            
def raise_to_front(window):
    window.lift()
    window.attributes('-topmost', True)
    window.attributes('-topmost', False)

db_ref = {}

dwh1 = Database('dwh1', 'ora-tns-dwh1.in.qservco.com', 1521, 'PROD')

table_ref = {}
for db in db_ref.values():
    for table in db.tables:
        table_ref[table] = table.columns