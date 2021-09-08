from tkinter import *
from collections import Counter, defaultdict
import pandas as pd
import cx_Oracle
import re
from datetime import datetime
from os import name, path
import xlsxwriter
import threading

class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.widgets = []

    def raise_to_front(self):
        self.master.lift()
        self.master.attributes('-topmost', True)
        self.master.attributes('-topmost', False)

    def clear(self):
        for widget in self.widgets:
            widget.destroy()

class CONFIG():
    def __init__(self):
        self.file = "settings/config.txt"
        self.tns_file = None
        self.database = None
        if path.exists(self.file):
            self.read_config()
            #read tns names after
        else:
            gui.
            pass

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

    def init_database(self):
        if path.exists(self.tns_file):
            self.read_config()
            read_tnsnames(config.tns_file)
        else:
            setup_config()
            self.write_config()
        return DATABASE()

class DATABASE():
    def __init__(self):
        self.name

class TABLE():
    def __init__(self):
        self.name

class QUERY():
    def __init__(self):
        self.timeout = 180 # 3 minutes

    def timer_setup(self):
        self.timer = threading.Timer(self.timeout, self.connection.cancel())
        #other methods can call this with self.timer.start() before the execution of the cursor
        #after the cursor executes add a self.timer.cancel() to quit the timer before it goes off

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

title = 'Query Builder'

root = Tk()
root.title(title)
gui = GUI(root)
config = CONFIG()