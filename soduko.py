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
import pandas as pd

#Creating the Window
root=Tk()
root.title('Soduko Solver')

class Application(Frame): #Window Constructor
    def __init__(self,master):
        Frame.__init__(self,master)

        self.width=3
        self.listofboxes=list()
        self.listofnums=list()

        self.grid()
        self.create_widgets()
        self.place_widgets()
        
        self.create_entries() # Creates the entry boxes
        self.grid_entries(8,8,self.listofboxes) # Recursively places 81 entry boxes on the Frame

        self.framesetup=dict()
        self.dict_setup(self.framesetup)

    def build_dataframe(self,d):
        areas=('area0','area1','area2','area3','area4','area5','area6','area7','area8')
        temp=list()
        c1=list()
        c2=list()
        c3=list()
        for k in range(9):
            temp.append(pd.DataFrame(d[areas[k]],columns=['1','2','3'])) # ,index=['1','2','3']
            if k==8 or k==5 or k==2:
                c1.append(temp[len(temp)-1])
            elif k==7 or k==4 or k==1:
                c2.append(temp[len(temp)-1])
            else:
                c3.append(temp[len(temp)-1])
            
        c1.reverse()
        c2.reverse()
        c3.reverse()
        c1=pd.concat(c1)
        c2=pd.concat(c2)
        c3=pd.concat(c3)
            
        part1=c1.merge(c2)
        print(part1)

    def dict_setup(self,d):
        for i in range(9):
            d['area'+str(i)]=[]
            
    def test_fill_frame_setup(self): # Used to auto-fill the table with nums
        self.framesetup={'area0':'000000000',
                         'area1':'111111111',
                         'area2':'222222222',
                         'area3':'333333333',
                         'area4':'444444444',
                         'area5':'555555555',
                         'area6':'666666666',
                         'area7':'777777777',
                         'area8':'888888888'}
        self.format_frame_setup(self.framesetup)
        self.build_dataframe(self.framesetup)

    def frame_setup(self):
        self.fill_frame_setup(self.framesetup,self.listofnums,0,0)
        self.format_frame_setup(self.framesetup)

        self.build_dataframe(self.framesetup)

    def fill_frame_setup(self,d,l,n,x): # fill_frame_setup(n=0,x=0)
        if n==8 and x==80:
            return self.dict_add(d,l,n,x)
        elif (x+1)%27==0: # If this works, then this and the %3 can be combined with an OR operator, maybe ?
            self.dict_add(d,l,n,x)
            return self.fill_frame_setup(d,l,n+1,x+1) # Moving up to the next set of areas
        elif (x+1)%9==0:
            self.dict_add(d,l,n,x)
            return self.fill_frame_setup(d,l,n-2,x+1) # Moving back to the far right, one row up
        elif (x+1)%3==0:
            self.dict_add(d,l,n,x)
            return self.fill_frame_setup(d,l,n+1,x+1) # Moving to the next area in the larger row
        else:
            self.dict_add(d,l,n,x)
            return self.fill_frame_setup(d,l,n,x+1) # Moving through the row in the area

    def format_frame_setup(self,d):
        for i in range(9):
            s=d['area'+str(i)]
            d['area'+str(i)]=([s[0],s[1],s[2]],[s[3],s[4],s[5]],[s[6],s[7],s[8]])

    def dict_add(self,d,l,n,x):
        temp=''
        if d['area'+str(n)]!=[]:
            temp=d['area'+str(n)]
            d['area'+str(n)]=temp+l[x]
        else:
            d['area'+str(n)]=l[x]
        
    def create_entries(self):
        for i in range(81):
            self.box=Entry(self,
                          width=self.width)
            self.listofboxes.append(self.box)
    
    def grid_entries(self,r,c,list):
        if r==0 and c==0:
            return list[0].grid(row=r,
                               column=c)
        else:
            if c==0:
                list[0].grid(row=r,
                            column=c)
                return self.grid_entries(r-1,8,list[1:])
            else: 
                list[0].grid(row=r,
                             column=c)
                return self.grid_entries(r,c-1,list[1:])
        
    def read_entries(self):
        for k in self.listofboxes:
            self.listofnums.append(k.get()) # NEED TO assert that the inputs are all integers and that the chart is full, and set this to int(k.get())

        self.frame_setup()

    def create_widgets(self): #Creating the Widgets to be placed
        self.submit_button=Button(self,
                                    text='Submit',
                                    width=8,
                                    height=1,
                                    command=self.read_entries)
        self.test_button=Button(self,
                                text='Test',
                                width=2,
                                height=1,
                                command=self.test_fill_frame_setup)

    def place_widgets(self): #Placing the Widgets on the grid
        self.submit_button.grid(row=9,
                                column=6,
                                columnspan=3)
        self.test_button.grid(row=9,
                              column=2)
        
app=Application(root)


root.mainloop()