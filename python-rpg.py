"""
    This is hopefully going to be a very simple RPG.
    By Jon Martin
"""

try:
    from tkinter import *
except ImportError:
    from Tkinter import *

import pandas as pd

#Creates the Window
root=Tk()
#To Manually Size the Window
root.geometry('300x200')
#Title at the top of the Window
root.title("Python RPG")

class Presser(Frame):#Button Constructor
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.button=Button(self,
                           text="Doggo")
        self.button.grid(row=1,
                         column=0)

#Similar to Game State, also keeps track of location
currentZone=0

#Going to contain all of the data for zone items and etc.
zoneData={
    'Zone':['0'],
    'Items':[''],
    'Paths':[
        'Up':[''],
        'Down':[''],
        'Left':[''],
        'Right':['']],
    'Zone':['1'],
    'Items':[''],
    'Paths':[
        'Up':[''],
        'Down':[''],
        'Left':[''],
        'Right':['']],
    'Zone':['2'],
    'Items':[''],
    'Paths':[
        'Up':[''],
        'Down':[''],
        'Left':[''],
        'Right':['']]]


"""
    PANDAS LIST
    
zoneData={
    'Zone':[0,1,2],
    'Items':['','',''],
    'Paths':[
    
"""

#Keeps track of the items picked up by the player
inventory=[
    '']

"""
    Goals:
     - Have Three Zones
     - Make an Inventory
     - Make a Title Page
"""

app=Presser(root)

root.mainloop()
