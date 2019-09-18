"""
    Ideas:
        -ASCII Map on a separate .txt file which will be referenced for
            displaying a mini-map

        -The ASCII Map is going to have to be upside down so that y will
            increase as you move up instead of decrease.
    
    By Jon Martin
    Co-Authored by Michael Pritchard
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
        self.place_default_widgets()
        self.place_action_widgets()

        self.x_location=16
        self.y_location=16

        self.current_row=0

        self.inventory=['dog', 'cat']

    def create_widgets(self):

        ##Default Widgets ---------------------------------------------------
        
        self.up_button=Button(self, #Up Button
                              text="Up",
                              width=5,
                              height=1,
                              command=self.up)
        
        self.down_button=Button(self, #Down Button
                                text="Down",
                                width=5,
                                height=1,
                                command=self.down)
        
        self.left_button=Button(self, #Left Button
                                text="Left",
                                width=5,
                                height=1,
                                command=self.left)
        
        self.right_button=Button(self, #Right Button
                                 text="Right",
                                 width=5,
                                 height=1,
                                 command=self.right)
        
        self.inventory_button=Button(self, #Inventory Button
                                     text="Inv.",
                                     width=5,
                                     height=1,
                                     command=self.inv)

        self.output=Text(self, #Output Box
                         wrap=WORD,
                         height=3,
                         width=20)

        self.map=Button(self, #Temporary Map Print Button
                        text="Map",
                        width=5,
                        height=1,
                        command=self.read_map_file)

        ##Action Widgets ---------------------------------------------------

        self.action_button=Button(self, #Actions Button
                                  text="Actions",
                                  width=20,
                                  height=1,
                                  command=self.place_subaction_widgets)

        self.search_items=Button(self, #Search4Items Button
                                 text="Search4Items",
                                 width=10,
                                 height=1)
        
        self.pickup_item=Button(self, #Pickup Item Button
                                text="PickupItem",
                                width=10,
                                height=1)
        
        self.back_button=Button(self, #Back Button
                                text="Back",
                                width=5,
                                height=1,
                                command=self.place_action_widgets)
        
    def place_default_widgets(self):
        self.up_button.grid(row=0, #Places the Up Button on the Grid
                            column=0,
                            padx=2,
                            pady=2)
        
        self.down_button.grid(row=0, #Places the Down Button on the Grid
                              column=1,
                              padx=2,
                              pady=2)
        
        self.left_button.grid(row=1, #Places the Left Button on the Grid
                              column=0,
                              padx=2,
                              pady=2)
        
        self.right_button.grid(row=1, #Places the Right Button on the Grid
                               column=1,
                               padx=2,
                               pady=2)
        
        self.inventory_button.grid(row=2, #Places the Inv. Button on the Grid
                                   column=0,
                                   padx=2,
                                   pady=2)
        
        self.output.grid(row=0, #Places the Output Box on the Grid
                         column=2,
                         rowspan=2,
                         padx=2,
                         pady=2)

    def place_action_widgets(self):
        self.action_button.grid(row=2, #Places the Action Button on the Grid
                                column=2,
                                columnspan=2,
                                padx=2,
                                pady=2)
        
        self.map.grid(row=2, #Places the Map Button on the Grid
                      column=1,
                      padx=2,
                      pady=2)

        self.search_items.grid_remove() #These remove the Search4Items, Pickup Item, and Back Buttons
        self.pickup_item.grid_remove()
        self.back_button.grid_remove()
            
    def place_subaction_widgets(self):
        self.search_items.grid(row=2, #Places the Search4Items Button on the Grid
                               column=2,
                               padx=2,
                               pady=2,
                               sticky=W)

        self.pickup_item.grid(row=2, #Places the Pickup Item Button on the Grid
                              column=2,
                              padx=2,
                              pady=2,
                              sticky=E)

        self.back_button.grid(row=2, #Places the Back Button on the Grid
                              column=1,
                              padx=2,
                              pady=2)
        
        self.action_button.grid_remove() #Removes the Action Button from the Grid
        self.map.grid_remove() #Removes the Map Button from the Grid


    def up(self): #Moves the Player UP by 1 & Prints New Location
        self.y_location+=1
        self.output.insert(0.0,">> "+str(self.x_location)+", "+str(self.y_location)+"\n")

    def down(self): #Moves the Player DOWN by 1 & Prints New Location
        self.y_location-=1
        self.output.insert(0.0,">> "+str(self.x_location)+", "+str(self.y_location)+"\n")

    def left(self): #Moves the Player LEFT by 1 & Prints New Location
        self.x_location+=1
        self.output.insert(0.0,">> "+str(self.x_location)+", "+str(self.y_location)+"\n")

    def right(self): #Moves the Player RIGHT by 1 & Prints New Location
        self.x_location-=1
        self.output.insert(0.0,">> "+str(self.x_location)+", "+str(self.y_location)+"\n")

    def inv(self): #Prints the Player's Current Inventory
        self.output.insert(0.0,">> "+str(self.inventory)+"\n")

    def read_map_file(self): #Sorts the ascii-map into an Array
        with open("ascii-map.txt") as f:
            message=f.readlines()
            for x in message:
                if X in message[x]:
                    self.current_row=x
            print(message[self.current_row])
        

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
