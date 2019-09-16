"""
    This is hopefully going to be a very simple RPG.
    By Jon Martin
"""

try:
    from tkinter import *
except ImportError:
    from Tkinter import *

##import pandas as pd

#Creates the Window
root=Tk()
#To Manually Size the Window
##root.geometry('300x200')
#Title at the top of the Window
root.title("Python RPG")

class Presser(Frame):#Button Constructor
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.up_button=Button(self, #Up Button
                              text="Up",
                              width=5,
                              height=1)
        self.up_button.grid(row=0,
                            column=0)

        self.down_button=Button(self, #Down Button
                                text="Down",
                                width=5,
                                height=1)
        self.down_button.grid(row=0,
                              column=1)

        self.left_button=Button(self, #Left Button
                                text="Left",
                                width=5,
                                height=1)
        self.left_button.grid(row=1,
                              column=0)

        self.right_button=Button(self, #Right Button
                                 text="Right",
                                 width=5,
                                 height=1)
        self.right_button.grid(row=1,
                               column=1)

        self.status=Text(self, #Output Box
                         wrap=WORD,
                         height=3,
                         width=20)
        self.status.grid(row=0,
                         column=2,
                         rowspan=2)

##zone_one={
##        'items':['computer','tablet','heiroglyphics','king tut'],
##        'control':['up','down','left','right']}
##
##zone_one=pd.DataFrame(zone_one,columns=['items','control'])
##
##zone_two={
##        'items':['dog','cat','sword','god'],
##        'control':['up','down','left','right']}
##
##zone_two=pd.DataFrame(zone_two,columns=['items','control'])
##
##frames=[zone_one,zone_two]
##
##zone_control_map=pd.concat(frames,keys=['zone_one','zone_two'])
##
##print(zone_control_map)

app=Presser(root)
root.mainloop()

"""
dog=input()

print(dog)
"""
