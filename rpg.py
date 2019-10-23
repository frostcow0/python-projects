"""
    Ideas:
        -ASCII Map on a separate .txt file which will be referenced for
            displaying a mini-map
    
    By Jon Martin
    Co-Authored by Michael Pritchard
"""

try:
    from tkinter import *
except ImportError:
    from Tkinter import *

##import pandas as pd

title='Python RPG'


#To Manually Size the Window
##root.geometry('300x200')
    
class Presser(Frame):#Button Constructor
    def __init__(self,master):
        Frame.__init__(self,master)

        self.current_row=0
        self.current_column=0

        self.last_direction=0

        self.inventory=['dog', 'cat']

        self.empty_row='|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|\n'
        self.char_key='X'
        self.wall_key='|'
        self.blank_key='_'

        self.grid()
        self.create_widgets()
        self.place_default_widgets()
        self.place_action_widgets()
        self.read_map_file()
        self.map_update(0)

        previous_map=list()

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
                         state=DISABLED,
                         height=6,
                         width=20)

        self.map=Button(self, #Currently Obsolete
                        text="Map",
                        width=5,
                        height=1,
                        command=self.read_map_file)

        self.map_box=Text(self, #Where the map is printed to
                          wrap=NONE,
                          state=DISABLED,
                          height=16,
                          width=33)

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
                         rowspan=3,
                         padx=2,
                         pady=2)

        self.map.grid(row=3, #Places the Map Button on the Grid
                      column=0,
                      padx=2,
                      pady=2)

        self.map_box.grid(row=4, #Testing a Box specifically for the Map
                          column=0,
                          columnspan=3,
                          rowspan=3,
                          padx=2,
                          pady=2)

    def place_action_widgets(self):
        self.action_button.grid(row=3, #Places the Action Button on the Grid
                                column=2,
                                columnspan=2,
                                padx=2,
                                pady=2)

        self.search_items.grid_remove() #These remove the Search4Items, Pickup Item, and Back Buttons
        self.pickup_item.grid_remove()
        self.back_button.grid_remove()
            
    def place_subaction_widgets(self):
        self.search_items.grid(row=3, #Places the Search4Items Button on the Grid
                               column=2,
                               padx=2,
                               pady=2,
                               sticky=W)

        self.pickup_item.grid(row=3, #Places the Pickup Item Button on the Grid
                              column=2,
                              padx=2,
                              pady=2,
                              sticky=E)

        self.back_button.grid(row=3, #Places the Back Button on the Grid
                              column=1,
                              padx=2,
                              pady=2)
        
        self.action_button.grid_remove() #Removes the Action Button from the Grid

    def up(self): #Moves the Player UP by 1 & Prints New Location
        self.map_update(1)
        
    def down(self): #Moves the Player DOWN by 1 & Prints New Location
        self.map_update(2)

    def left(self): #Moves the Player LEFT by 1 & Prints New Location
        self.map_update(3)

    def right(self): #Moves the Player RIGHT by 1 & Prints New Location
        self.map_update(4)

    def inv(self): #Prints the Player's Current Inventory
        self.output.config(state=NORMAL)
        print(self.previous_map[self.current_row-1][self.current_column-1])

    def read_map_file(self): #Sorts the ascii-map into an Array
        with open("ascii-map.txt") as f: #Can only do Read OR Readlines. The Second will show up blank.
            message=f.readlines()
            row_counter=(-1)
            
            self.previous_map=message
            
            for k in message: #k == the row's text
                row_counter+=1
                if k.find(self.char_key)!=(-1): #Finds the location of the X in the map
                    self.current_row=row_counter
                    self.current_column=(k.find(self.char_key)+1)
            
            self.map_box.config(state=NORMAL)#Outputs the map to the Map_Box
            self.map_box.delete('18.0',END)
            for k in message:
                #print(k)
                self.map_box.insert(0.0,k)
            self.map_box.config(state=DISABLED)

    def map_update(self,num): #Updates the Map_Box and X,Y locations in the Output
        horizontal=0
        vertical=0

        if num==1: #Up
            vertical=1
        if num==2: #Down
            vertical=(-1)
        if num==3: #Left
            horizontal-=2
            #direction=0
        if num==4: #Right
            horizontal+=2
            #direction=0
        
        with open("ascii-map.txt","w") as f:
            new_map=''

            new_row=self.current_row+vertical
            new_column=self.current_column+horizontal

            if new_row>=16 or new_row<=(-1): #To keep the character from going too far up or down.
                vertical=0
                if new_row==16:
                    new_row=15
                if new_row==(-1):
                    new_row=0

            if new_column>=34 or new_column<=0: #To keep the character from going too far left or right.
                horizontal=0
                if new_column==34:
                    new_column=32
                if new_column==0:
                    new_column=2
                    
            for k in range(16):
                if k==new_row: #Finds the new row
                    new_map+=self.row_generator(new_column) #Adds row with Character
                else: new_map+=self.row_generator(0) #Adds empty row
            f.write(new_map)
            self.current_row=new_row
            self.current_column=new_column

        self.read_map_file()
        
        self.output.config(state=NORMAL) #Outputs X,Y to the Output
        self.output.insert(0.0,">> "+str(int(self.current_column/2))+", "+str(self.current_row+1)+"\n")
        self.output.config(state=DISABLED)

        

    def row_generator(self,col): #Builds the new row or provides the empty one
        working_row=''
        
        if col!=0:
            for working_column in range(1,34):
                if working_column==col:
                    working_row+=self.char_key
                else:
                    if working_column%2:
                        working_row+=self.wall_key
                    else:
                        working_row+=self.blank_key
            working_row+='\n'
            return working_row
        else: return self.empty_row

    def minimap_test(self):
        #use find() and then go to that spot in the map string +1 & -1, go to the 
        #row above and row below and do the same thing
        print("yes")

def new_game():
    create_window()
    print('---------------dog that you are')

def load_game():
    create_window(1)
    print('----------------woof')

def create_window(num=0): #Without this, the RPG would always open upon import.
    root=Tk() #Creates the Window
    root.title(title) #Title at the Top
    app=Presser(root) #Runs Presser
    root.mainloop() #Runs Tkinter
    if num==1:
        pass

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

if __name__=='__main__':
    pass