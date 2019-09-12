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

zone_one={
        'items':['computer','tablet','heiroglyphics','king tut'],
        'control':['up','down','left','right']}

zone_one=pd.DataFrame(zone_one,columns=['items','control'])

zone_two={
        'items':['dog','cat','sword','god'],
        'control':['up','down','left','right']}

zone_two=pd.DataFrame(zone_two,columns=['items','control'])

frames=[zone_one,zone_two]

zone_control_map=pd.concat(frames,keys=['zone_one','zone_two'])

print(zone_control_map)

"""
dog=input()

print(dog)
"""