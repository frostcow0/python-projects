try:
    from tkinter import *
except ImportError:
    from Tkinter import*
    
root=Tk()
root.title('Start Screen')
#root.geometry('300x300')

import rpg

class Home(Frame):
    def __init__(self,master):
        Frame.__init__(self,master,
                       background='Moccasin')

        self.button_height=1 #Height of Buttons
        self.button_width=15 #Width of Buttons
        self.button_pad_x=2
        self.button_pad_y=10
        self.font='Courier'

        self.background_color='Moccasin'
        self.background_button='PeachPuff'
        
        self.grid()
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.welcome_text=Label(self,
                                background=self.background_color,
                                font='Courier 16',
                                text='Welcome to Jon\'s Python RPG!')

        self.new_game=Button(self,
                             width=self.button_width,
                             height=self.button_height,
                             font=self.font,
                             background=self.background_button,
                             text='New Game',
                             command=self.new)

        self.load_game=Button(self,
                              width=self.button_width,
                              height=self.button_height,
                              font=self.font,
                              background=self.background_button,
                              text='Load Game',
                              command=self.load)

        self.quit=Button(self,
                         width=self.button_width,
                         height=self.button_height,
                         font=self.font,
                         background=self.background_button,
                         text='Quit',
                         command=self.quit)

    def place_widgets(self):
        self.welcome_text.grid(row=0,
                               column=1,
                               rowspan=2,
                               padx=10,
                               pady=10)

        self.new_game.grid(row=2,
                           column=1,
                           padx=self.button_pad_x,
                           pady=self.button_pad_y)

        self.load_game.grid(row=3,
                            column=1,
                            padx=self.button_pad_x,
                            pady=self.button_pad_y)

        self.quit.grid(row=4,
                       column=1,
                       padx=self.button_pad_x,
                       pady=self.button_pad_y)

    def load(self):
        if __name__=='__main__':
            root.destroy()
            rpg.load_game()

    def new(self):
        popup = Tk()
        popup.title('Howdy')
        popup.background=('Moccasin') #Doesn't work
        
        def run():
            if __name__=='__main__':
                popup.destroy()
                root.destroy()
                rpg.new_game()
                
        label=Label(popup,
                    font='Courier 24',
                    text='Hi :)')
        
        button1=Button(popup,
                       font=self.font,
                       width=self.button_width,
                       background='Green',
                       text='Confirm',
                       command=run)
        
        button2=Button(popup,
                       font=self.font,
                       width=self.button_width,
                       background='Red',
                       text='Never mind',
                       command=popup.destroy)
        
        label.grid(row=0,columnspan=2,sticky=N)
        button1.grid(row=1,column=0,sticky=W)
        button2.grid(row=1,column=1,sticky=E)

        popup.mainloop()
        
    def quit(self):
        root.destroy()
        





app=Home(root)

root.mainloop()
