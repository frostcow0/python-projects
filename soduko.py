"""
Goals:
    1. Learn how to use Pandas
    2. Input/Output Interface

Going to make a GUI that contains a 3x3 of text boxes.
Input given soduko problem and it should auto-complete.
Would be a cool idea to color the text boxes with answers.

Current To-Do:
    GUI with Buttons & 3x3 Text Boxes

    By: Jon Martin
"""

from tkinter import *

#Creating the Window
root=Tk()
root.title('Soduko Solver')

class Application(Frame): #Window Constructor
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()
        self.place_widgets()
        x=EntryBox(root)
        x.create_box()
        x.place_box()

    def create_widgets(self): #Creating the Widgets to be placed
        
        self.submit_button=Button(self,
                                    text='Submit',
                                    width=10,
                                    height=1,
                                    command=self.submit)

        self.box1=Text(self,
                        width=3,
                        height=1)

        self.box2=Text(self,
                        width=3,
                        height=1)

        self.box3=Text(self,
                        width=3,
                        height=1)

        self.box4=Text(self,
                        width=3,
                        height=1)

        self.box5=Text(self,
                        width=3,
                        height=1)

        self.box6=Text(self,
                        width=3,
                        height=1)

    def place_widgets(self): #Placing the Widgets on the grid
        
        self.submit_button.grid(row=1,
                                column=0)
        
        self.box1.grid(row=0,
                        column=1)

    def submit(self): #Takes the input and finds the answers
        print('boy howdy')

class EntryBox(Application):
    def __init__(self,master):
        self.height=1
        self.width=2
        self.create_box()
        self.place_box()

    def create_box(self):
        self.box=Text(self,
                        height=self.height,
                        width=self.width,
                        text='congrats!')

    def place_box(self):
        self.box.grid(row=3,
                        column=3)



app=Application(root)


root.mainloop()