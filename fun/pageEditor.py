"""
Goals:
    1. Working Buttons through a Constructor
    2. Create a Display for the File's contents
    3. Read & Write to a File

    By: Jon Martin
"""


from tkinter import *

#creating the window
root=Tk()
"""root.geometry('800x500')"""
root.title("Test GUI")

class Application(Frame): #Constructor
#Constructor for Buttons
    def __init__(self,master):
        #Initializes the Frame
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self): #Method
        #button that reads the file
        self.button=Button(self,
                            text="Read",
                            command=self.read_file)
        self.button.grid(row=1,
                         column=1,
                         sticky=NW)
        #description
        self.instructions=Label(self,
                                text="Enter new text here:")
        self.instructions.grid(row=0,
                               column=0,
                               sticky=W)
        #text entry box
        self.entry=Entry(self)
        self.entry.grid(row=0,
                        column=0,
                        sticky=E)
        #button that writes the file
        self.submit_button=Button(self,
                                  text="Write",
                                  command=self.write_file)
        self.submit_button.grid(row=0,
                                column=1,
                                sticky=W)
        #output
        self.text=Text(self,
                       width=35,
                       height=50,
                       wrap=WORD)
        self.text.grid(row=1,
                       column=0,
                       sticky=W)
        
    def read_file(self): #Method
        #reads the file
        with open("page.txt") as f:
            self.text.delete('1.0',END)#deletes what was in the text box
            message=f.read()
            """message=f.readlines()#pulls the file's contents line by line in an array"""
            self.text.insert(0.0,str(message))#puts the file's contents in the text box

    def write_file(self):
        #writes to the file
        with open("page.txt","w") as f:
            entry=self.entry.get()
            self.entry.delete(0,'end')
            f.write(entry)
            self.text.delete('1.0',END)#deletes what was in the text box
            self.text.insert(0.0,str(entry))#puts the file's contents in the text box
        
app=Application(root)





root.mainloop() #Needed for the window. Ends the program, commands after this won't run.
