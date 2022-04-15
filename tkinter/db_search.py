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
import pandas as pd
import cx_Oracle
import re
from datetime import datetime
from os import name, path
import xlsxwriter

'''
This script assumes similar tnsnames.ora structure, as well as an
Oracle database.
'''

title = 'Query Builder'
databases = {}

class Database():
    def __init__(self, name, host, port, tab_own):
        self.name = name
        self.host = host
        self.port = port
        self.table_owner = tab_own.upper()  
        self.cursor = None
        self.schema = defaultdict(list)
        self.unique_columns = []
        self.filters = []
        self.distinct = 0
        self.init_db_connection()
        self.loading()

        self.tables = self.build_tables()
        self.pop_unique_columns()
        db_ref[self.name] = self

        create_app(0, self)

    def create_popup(self, query, option, db = None):
        root=Tk() #Creates the Window
        root.title(title) #Title at the Top
        raise_to_front(root)
        app=Popup(root, query, option, db) #Runs Popup or Lbox
        root.mainloop()

    def __str__(self):
        return str(self.name)

    def init_db_connection(self):
        self.login_info = []
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
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 1403:
                self.create_popup(f"No rows returned. Error code: {error.code}", 1)
                self.init_db_connection()
            elif error.code == 1017:
                self.create_popup(f"Invalid login. Error code: {error.code}", 1)
                self.init_db_connection()
            elif error.code == 28000:
                self.create_popup(f"Too many login attempts. Error code: {error.code}", 1)
                quit()
            else:
                print(f"Un-caught error. Error code: {error.code}")
        except Exception as error:
            self.create_popup(f"Couldn't connect to the database. -- {repr(error)}", 1)
            self.init_db_connection()

    def create_schema(self):
        query = f'''
        select
            table_name, column_name
        from dba_tab_cols
        where owner = '{self.table_owner}'
        and avg_col_len > 0
        order by table_name
        '''
        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            while row:
                self.schema[row[0]].append(row[1])
                row = self.cursor.fetchone()
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 942:
                self.loading.destroy()
                self.create_popup(f"Schema query failed. Use a different DB. Error code: {error.code}", 1)
                init()
            else:
                print(f"Un-caught error. Error code: {error.code}")
        self.exit_popup()

    def write_schema(self): # deprecated
        with open(f"schemas/schema_{self.name.upper()}", "w") as file:
            for table, columns in self.schema.items():
                file.write(table+"\n")
                for column in columns:
                    file.write("\t"+column+"\n")

    def read_schema(self): # much slower than just querying - deprecated
        pattern = re.compile(r'\s')
        with open(f"schemas/schema_{self.name.upper()}") as file:
            last_table = ''
            while True:
                content = file.readline()
                if pattern.match(content):
                    self.schema[last_table].append(content.strip())
                else:
                    last_table = content[:len(content)-2]

    def pop_unique_columns(self):
        query = f'''
        select distinct
            column_name
        from all_tab_cols
        where owner = '{self.table_owner}'
        and avg_col_len > 0
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
        self.loading = root = Tk()
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
        raise_to_front(root)
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
        root.user.focus_force()
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

    def get_login(self, obj = 0):
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
        while len(choices_tables.keys())>0:
            choices = [x for x in choices_tables.keys()]
            table_score = self.build_table_score(choices_tables) #build_table_score(choices_tables)
            table = self.keywithmaxval(table_score) # t1
            for choice in choices:
                if choice in self.tables[self.tables.index(table)].columns:
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
        self.req_tables = req_tables
        self.get_filters(set(tuple(x) for x in req_tables.values())) # Easiest way to get choices at this point
        if len(req_tables) == 1:
            for table, choices in req_tables.items():
                i = 0
                keyword = '\nWHERE'
                where = ''
                if self.distinct == 1:
                    query = f'SELECT DISTINCT\n\t'
                else: query = f'SELECT\n\t'
                for choice in choices:
                    query += f'{choice.lower()}, '
                query = query[:len(query) - 2]
                query += f'\nFROM\n\t{self.table_owner.lower()}.{table.name.lower()}'
                for filter in self.filters:
                    if i == 1:
                        keyword = '\nAND '
                    else:
                        i += 1
                    where += f'{keyword} {filter.upper()}'
                query += where
        else: 
            joins = self.join([x for x in req_tables.keys()])
            if self.distinct == 1:
                select = f'SELECT DISTINCT\n\t'
            else: select = f'SELECT\n\t'
            frm = '\nFROM\n\t'
            where = ''
            i = 0
            keyword = '\nWHERE '
            for table, choices in req_tables.items():
                for choice in choices:
                    select += f'{table.name.lower()}.{choice.lower()}, '
                frm += f'{self.table_owner.lower()}.{table.name.lower()}, '
            select = select[:len(select) - 2]
            frm = frm[:len(frm) - 2]
            for table1, container in joins.items():
                for table2, common in container:
                    if i == 1:
                        keyword = '\nAND '
                    else:
                        i += 1
                    where += keyword
                    where += f'{table1.name.lower()}.{common.lower()} = {table2.name.lower()}.{common.lower()}'
            if i == 1:
                keyword = '\nAND '
            else:
                i += 1
            for filter in self.filters:
                where += f'{keyword} {filter.upper()}'
            query = select + frm + where
        print('='*60)
        print(query+'\n')
        self.create_popup(query, 0, self)

    def join(self, tables):
        joins = defaultdict(list)
        for i, table1 in enumerate(tables):
            if i == len(tables)-1:
                break
            for j, table2 in enumerate(tables[i+1:]):
                common = list(set(self.tables[self.tables.index(table1)].columns).intersection(
                            set(self.tables[self.tables.index(table2)].columns)))
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
                        common1 = list(set(self.tables[self.tables.index(table1)].columns).intersection(
                                    set(self.tables[self.tables.index(table3)].columns)))
                        common2 = list(set(self.tables[self.tables.index(table2)].columns).intersection(
                                    set(self.tables[self.tables.index(table3)].columns)))
                        if common1 and common2:
                            joins[table1].append((table3, common1[0])) # maybe ?
                            joins[table2].append((table3, common2[0]))
                            x = True
                            break
                if not x:
                    self.create_popup(f"Nothing in common found for {table1}", 1)
                    raise(f"Nothing in common found for {table1}")
        return joins

    def get_filters(self, choices):
        self.choice_list = []
        for choice in choices:
            for item in choice:
                self.choice_list.append(item)
        create_app(2, self)

class Table():
    def __init__(self, name, columns, database):
        self.name = name
        self.columns = columns
        self.database = database

    def __str__(self):
        return str(self.name)
        # return f"Table - {self.name}"

    def name(self):
        return str(self.name)

def create_app(option, db):
    root=Tk() #Creates the Window
    root.title(title) #Title at the Top
    raise_to_front(root)
    app=Lbox(root, option, db) #Runs Presser or Lbox
    root.mainloop() #Runs Tkinter (Doesn't run anything after this until the window is closed)

class Lbox(Frame):
    def __init__(self, master, option, db):
        Frame.__init__(self, master)
        self.root = master
        self.db = db
        self.option = option
        self.filter_choices = {}
        self.current_filters = []
        self.choose(self.option)

    def choose(self, option):
        mode = 'single'
        if option == 0 or option == 2:
            choices = 'columns'
            self.search_var = StringVar()
            self.search_var.trace('w', lambda name, index, mode: self.update_list())
            self.search_lab = Label(self,
                        text = 'Search',
                        font = ('Veridian', 10),
                        padx = 3, pady = 3)
            self.search_bar = Entry(self,
                        textvariable = self.search_var,
                        width = 20)
        elif option == 1:
            choices = 'databases'

        self.pack()
        self.yscrollbar = Scrollbar(self)
        self.yscrollbar.pack(side = RIGHT, fill = BOTH)
        self.label = Label(self,
                   text = f'Select from the {choices} below',
                   font = ('Veridian', 16),
                   padx = 3, pady = 3)
        self.label.pack()
        self.list_all = Listbox(self, selectmode = mode,
                        yscrollcommand = self.yscrollbar.set,
                        width = 30)
        self.list_all.pack(padx = 10, pady = 10,
                  expand = YES, fill = BOTH, side = LEFT)
        self.button = Button(self,
                  text = 'Enter',
                  font = ('Veridian', 12),
                  padx = 3, pady = 3,
                  command = self.get)
        if option == 0 or option == 2:
            self.list_selected = Listbox(self, selectmode = mode,
                            yscrollcommand = self.yscrollbar.set,
                            width = 30)
            self.list_selected.pack(padx = 10, pady = 10,
                  expand = YES, fill = BOTH, side = RIGHT)
            if option == 2:
                self.text = StringVar(self, value = "ex. = 'MI'")
                self.lab = Label(self,
                   text = 'Create filter here',
                   font = ('Veridian', 10),
                   padx = 3, pady = 3).pack()
                self.entry = Entry(self, width = 20, textvariable = self.text)
                self.entry.pack()
                self.entry.bind('<Return>', self.add)
                self.entry.bind('<FocusIn>', self.clear_entry)
            elif option == 0:
                self.search_lab.pack()
                self.search_bar.pack()
                self.search_bar.focus_force()
            self.add_b = Button(self,
                  text = 'Add',
                  font = ('Veridian', 10),
                  padx = 3, pady = 3,
                  command = self.add)
            self.rem_b = Button(self,
                  text = 'Remove',
                  font = ('Veridian', 10),
                  padx = 3, pady = 3,
                  command = self.rem)
            self.add_b.pack(fill = X)
            self.rem_b.pack(fill = X)
            if option == 0:
                self.distinct = IntVar()
                self.radio = Checkbutton(self,
                        text = 'DISTINCT',
                        padx = 15, pady = 15,
                        font = ('Veridian', 10),
                        variable = self.distinct
                        ).pack(fill = X)
            self.button.pack(side = BOTTOM, fill = X)
            self.list_all.focus_force()
            if option == 0:
                for column in sorted(self.db.unique_columns):
                    self.list_all.insert(END, column)
            elif option == 2:
                self.list_all.insert(END, 'ROWNUM')
                for table in self.db.req_tables.keys():
                    for column in sorted(self.db.tables[self.db.tables.index(table)].columns):
                        self.list_all.insert(END, column)
                        self.filter_choices[column] = table
                if len(self.db.filters) > 0:
                    for filter in self.db.filters:
                        if not re.match('ROWNUM', filter):
                            self.list_selected.insert(END, filter.split('.')[1])
                        else: self.list_selected.insert(END, filter)
                
        elif option == 1:
            self.refresh = Button(self,
                            text = 'New TNS File',
                            font = ('Veridian', 12),
                            padx = 3, pady = 3,
                            command = self.refresh_config)
            self.refresh.pack(fill = X)
            self.button.pack(fill = X)
            for db in sorted(self.db.keys()):
                self.list_all.insert(END, db)
        self.yscrollbar.config(command = self.list_all.yview)

    def clear_entry(self, event = None):
        self.text.set('')

    def update_list(self):
        self.list_all.delete(0, END)
        for item in sorted(self.db.unique_columns):
            if self.search_var.get().lower() in item[0].lower():
                self.list_all.insert(END, item)

    def add(self, extra = None):
        choice = self.list_all.get(ANCHOR)
        if choice == '':
            return # they tried to add w/o a selection.
        if self.option == 0:
            self.list_selected.insert(END, choice)
            self.list_all.delete(ANCHOR)
        elif self.option == 2:
            filt = self.entry.get()
            if not choice == 'ROWNUM':
                table = self.filter_choices[choice]
                self.current_filters.append(table.name+'.'+choice+' '+filt)
            else:
                self.current_filters.append(choice+' '+filt)
            self.list_selected.insert(END, choice+' '+filt)
            self.list_all.delete(ANCHOR)

    def rem(self):
        if self.option == 0:
            choice = self.list_selected.get(ANCHOR)
            self.list_selected.delete(ANCHOR)
            self.list_all.insert(END, choice)
        elif self.option == 2:
            choice = self.list_selected.get(ANCHOR)
            self.list_selected.delete(ANCHOR)
            if not choice == 'ROWNUM':
                table = self.filter_choices[choice]
                self.current_filters.remove(table.name+'.'+choice)
            else:
                self.current_filters.remove(choice)

        
    def get(self, extra = None):
        if self.option == 0:
            for db in db_ref.keys():
                obj = db_ref[db]
                choices_tables = {};
                for choice in self.list_selected.get(0, END):
                    choice = choice[0]
                    for table in obj.tables:
                        if choice in table.columns:
                            if choice not in choices_tables.keys():
                                choices_tables[choice] = [table]
                            else:
                                choices_tables[choice].append(table)
                self.db.distinct = self.distinct.get()
                obj.get_req_tables(choices_tables)
        elif self.option == 1:
            choice = self.list_all.get(ANCHOR)
            self.root.destroy()
            config.db_info = [choice, databases[choice]]
            if choice in config.dbs:
                config.create_db(config.dbs[choice])
            else:
                owner_popup(f'Set Up {choice}')
        elif self.option == 2:
            self.db.filters = []
            for filt in self.current_filters:
                self.db.filters.append(filt)
            self.root.quit()
            self.root.destroy()
    
    def refresh_config(self):
        self.root.destroy()
        setup_config()
        config.write_config()

class Popup(Frame):
    def __init__(self, master, message, option, db = None):
        Frame.__init__(self, master)
        self.root = master
        self.message = message
        self.option = option
        self.db = db
        self.widgets = []
        
        self.pack()
        if self.option == 0:
            self.place_buttons()
        elif self.option == 1:
            self.error(self.message)
        elif self.option == 2:
            self.setup()
        elif self.option == 3:
            self.tab_owner()

    def clear(self):
        for widget in self.widgets:
            widget.destroy()

    def exit(self, extra = None):
        self.root.destroy()

    def tab_owner(self):
        self.pack()
        self.label = Label(self,
                    text = 'Who\'s the table owner? ex. PROD :  ',
                    font = ('Veridian', 12),
                    padx = 3, pady = 3).pack()
        self.entry = Entry(self,
                    width = 20)
        self.entry.pack()
        self.entry.bind('<Return>', self.owner_get)
        self.entry.focus_force()
        self.button = Button(self,
                    text = 'Enter',
                    font = ('Veridian', 12),
                    padx = 3, pady = 3,
                    command = self.owner_get).pack()
    
    def owner_get(self, obj = 0):
        owner = self.entry.get()
        self.exit()
        if not owner:
            owner_popup('Must choose a table owner')
            return
        config.create_db(owner)

    def setup(self):
        self.pack()
        self.label = Label(self,
                    text = self.message,
                    font = ('Veridian', 12),
                    padx = 3, pady = 3).pack() #easier to pack this way

        self.top_frame = Frame(self)
        self.bot_frame = Frame(self)
        self.top_frame.pack()
        self.bot_frame.pack()

        self.tns = Label(self,
                    text = 'TNSNAMES.ORA Path :  ',
                    font = ('Veridian', 10),
                    padx = 3, pady = 3).pack(
                            in_ = self.top_frame,
                            side = LEFT)
        self.path = Entry(self,
                    width = 30)
        self.path.pack(
            in_ = self.top_frame,
            side = RIGHT) # Have to pack separate when binding
        self.path.bind('<Return>', self.setup_get)
        self.button = Button(self,
                    text = 'Enter',
                    font = ('Veridian', 12),
                    padx = 3, pady = 3,
                    command = self.setup_get).pack()

    def setup_get(self, obj = 0):
        tnsnames_file = self.path.get()
        if path.exists(tnsnames_file):
            self.exit()
            config.tns_file = tnsnames_file
            read_tnsnames(tnsnames_file)
        else:
            self.exit()
            root = Tk()
            root.title('File doesn\'t exist')
            raise_to_front(root)
            app = Popup(root, 'File doesn\'t exist.', 1)
            root.mainloop()
            setup_config()

    def error(self, message):
        self.clear()
        self.lbl = Label(self,
                    text = message,
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
        self.clear()
        self.sql = Button(self,
                  text = 'SQL Query',
                  font = ('Veridian', 12),
                  padx = 3, pady = 6,
                  width = 15,
                  command = self.export_sql_query)
        self.sql.pack(fill = X)
        self.xlsx = Button(self,
                  text = 'Excel',
                  font = ('Veridian', 12),
                  padx = 3, pady = 6,
                  width = 15,
                  command = self.loading_xlsx)
        self.xlsx.pack(fill = X)
        self.csv = Button(self,
                  text = 'CSV',
                  font = ('Veridian', 12),
                  padx = 3, pady = 6,
                  width = 15,
                  command = self.loading_csv)
        self.csv.pack(fill = X)

        self.widgets = [self.sql, self.xlsx, self.csv]

    def back(self):
        self.clear()
        self.place_buttons()
    
    def export_sql_query(self):
        self.clear()
        self.text = Text(self,
                        height = 10,
                        width = 100,
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
        self.clear()
        self.root.geometry('500x50')
        while True:
            try:
                for db in db_ref.keys():
                    db_obj = db_ref[db]
                    df = pd.read_sql(self.message, db_obj.connection)
                break
            except ValueError as e:
                self.error(f'Error: {e}')
            except pd.io.sql.DatabaseError as e:
                self.root.geometry('400x200')
                self.error(f'Error: {e}')
        
        today = datetime.today().strftime('%Y-%m-%d')
        filename = f'{db_obj.name}_query-{today}.xlsx'
        sheetname = f'Excel Export {today}'
        try:
            writer = pd.ExcelWriter(filename, engine = 'xlsxwriter')
            df.to_excel(writer, sheet_name = sheetname, header = False, index = False)
            worksheet = writer.sheets[sheetname]
            (max_row, max_col) = df.shape

            headers = [{'header': header} for header in df.columns] # Cool way to create list w/ one line
            worksheet.add_table(0, 0, max_row - 1, max_col - 1, {'columns': headers})
            writer.save()

            self.label = Label(self,
                text = f'Exported {db_obj.name} to {filename}',
                font = ("Verdana", 14)).pack()

            self.widgets = [self.label]
        except xlsxwriter.exceptions.XlsxFileError as e:
            self.error(f'Error: {e}')
        except PermissionError as e:
            self.error("If the Excel file is open, close it.\n"
                            f"--- {e}")

    def export_csv(self):
        self.clear()
        self.root.geometry('500x50')
        for db in db_ref.keys():
            db_obj = db_ref[db]
            df = pd.read_sql(self.message, db_obj.connection)
        today = datetime.today().strftime('%Y-%m-%d')
        filename = f'{db_obj.name}_query-{today}.csv'
        df.to_csv(filename, index = False)
        self.label = Label(self,
                text = f'Exported {db_obj.name} to {filename}',
                font = ("Verdana", 14)).pack()

        self.widgets = [self.label]

    def loading_xlsx(self):
        self.clear()
        self.load = Label(self,
                text = 'Loading query for XLSX . . .',
                font = ("Verdana", 14))
        self.load.pack()
        self.widgets = [self.load]
        self.after(200, self.export_xlsx)

    def loading_csv(self):
        self.clear()
        self.load = Label(self,
                text = 'Loading query for CSV . . .',
                font = ("Verdana", 14))
        self.load.pack()
        self.widgets = [self.load]
        self.after(200, self.export_csv)
            
def raise_to_front(window):
    window.lift()
    window.attributes('-topmost', True)
    window.attributes('-topmost', False)

def read_tnsnames(file):
    with open (file) as f:
        global databases
        message = f.readlines()
        dbs = {}
        db_flag = False
        host = port = sid = ''
        for line in message:
            line = line.lower()
            line = line.split('(')
            for split in line:
                if 'tcp-loopback' in split:
                    continue
                if split[0] == '#' or split == '\n':
                    db_flag = True
                    continue
                if db_flag == True:
                    if 'host' in split:
                        host = line[3][7:].strip(')')
                    if 'port' in split:
                        port = line[4].strip('port = ').strip('))\n')
                    if 'service_name' in split or 'sid' in split:
                        temp = line[1].split(' ')
                        sid = temp[2].strip(')\n')
                        dbs[sid] = [host, port]
                        db_flag = False
        if 'orcl' in dbs.keys():
            del dbs['orcl']
        databases = dbs
        create_app(1, dbs)

class Config():
    def __init__(self):
        self.file = "settings/config.txt"
        self.dbs = {}
        self.db_info = None
        self.tns_file = None
        self.db = None

    def read_config(self):
        with open(self.file) as file:
            contents = file.read()
            contents = contents.split('&')
            del contents[0] # empty space from first &
            self.tns_file = contents[0]
            for content in contents:
                if re.match('C:', content):
                    self.tns_file = content
                    continue
                content = content.split('=')
                self.dbs[content[0]] = content[1]

    def write_config(self):
        if not config.tns_file == '':
            with open(self.file, "w") as file:
                content = f'&{config.tns_file}'
                content += f'&{self.db.name}={self.db.table_owner}'
                file.write(content)

    def create_db(self, owner):
        self.db = Database(self.db_info[0], self.db_info[1][0], self.db_info[1][1], owner)
        if not self.db_info[0] in self.dbs:
            self.write_config()

def setup_config():
    root = Tk()
    root.title('Set Up Config')
    raise_to_front(root)
    app = Popup(root, 'First Time Setup', 2)
    root.mainloop()

def owner_popup(title):
    root = Tk()
    root.title(title)
    raise_to_front(root)
    app = Popup(root, 'First Time Setup', 3)
    root.mainloop()

def init():
    if path.exists(config.file):
        config.read_config()
        read_tnsnames(config.tns_file)
    else:
        setup_config()
        config.write_config()
        
config = Config()
db_ref = {}

if __name__=='__main__':
    init()
    quit()

#C:\app\client\Administrator\product\18.0.0\client_1\network\admin\tnsnames.ora