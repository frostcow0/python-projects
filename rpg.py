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
        self.create_action_widgets()

    def create_widgets(self):
        self.up_button=Button(self, #Up Button
                              text="Up",
                              width=5,
                              height=1)
        self.up_button.grid(row=0,
                            column=0,
                            padx=2,
                            pady=2)

        self.down_button=Button(self, #Down Button
                                text="Down",
                                width=5,
                                height=1)
        self.down_button.grid(row=0,
                              column=1,
                              padx=2,
                              pady=2)

        self.left_button=Button(self, #Left Button
                                text="Left",
                                width=5,
                                height=1)
        self.left_button.grid(row=1,
                              column=0,
                              padx=2,
                              pady=2)

        self.right_button=Button(self, #Right Button
                                 text="Right",
                                 width=5,
                                 height=1)
        self.right_button.grid(row=1,
                               column=1,
                               padx=2,
                               pady=2)

        self.status=Text(self, #Output Box
                         wrap=WORD,
                         height=3,
                         width=20)
        self.status.grid(row=0,
                         column=2,
                         rowspan=2,
                         padx=2,
                         pady=2)

        self.inventory_button=Button(self,
                                     text="Inv.",
                                     width=5,
                                     height=1)
        self.inventory_button.grid(row=2,
                                   column=0,
                                   padx=2,
                                   pady=2)

    def create_action_widgets(self):
        self.action_button=Button(self,
                                  text="Actions",
                                  width=20,
                                  height=1,
                                  command=self.place_subaction_widgets)
        self.action_button.grid(row=2,
                                column=2,
                                columnspan=2,
                                padx=2,
                                pady=2)

        self.search_items=Button(self,
                                 text="Search4Items",
                                 width=10,
                                 height=1)
        self.pickup_item=Button(self,
                                text="PickupItem",
                                width=10,
                                height=1)
        self.back_button=Button(self,
                                text="Back",
                                width=5,
                                height=1,
                                command=self.create_action_widgets)

        self.search_items.grid_remove()
        self.pickup_item.grid_remove()
        self.back_button.grid_remove()
            
    def place_subaction_widgets(self):
        self.search_items.grid(row=2,
                               column=2,
                               padx=2,
                               pady=2,
                               sticky=W)

        self.pickup_item.grid(row=2,
                              column=2,
                              padx=2,
                              pady=2,
                              sticky=E)

        self.back_button.grid(row=2,
                              column=1,
                              padx=2,
                              pady=2)
        
        self.action_button.grid_remove()


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
