from tkinter import *


class App(Frame):
    def __init__(self, master, data):
        Frame.__init__(self, master)
        self.root = master
        self.widgets = []
        # self.pack()
        self.grid()
        self.inventory = data['inventory']

    def start_screen(self):
        """Loads initial app screen"""
        self.clear()
        self.new_label('SWSE Business Manager', 15
            ).grid(row=0, column=0, columnspan=3)
        self.inv = Button(self,
                    text = 'Inventory',
                    font = ('Veridian', 12),
                    padx = 3, pady = 6,
                    width = 15,
                    command = self.inventory_screen)
        # self.inv.pack()
        self.inv.grid(row=1, column=0, columnspan=3)
        self.widgets.append(self.inv)
        self.transaction = Button(self,
                    text = 'Make a Transaction',
                    font = ('Veridian', 12),
                    padx = 3, pady = 6,
                    width = 15,
                    command = self.transaction_screen)
        # self.transaction.pack()
        self.transaction.grid(row=2, column=0, columnspan=3)
        self.widgets.append(self.transaction)

    def inventory_screen(self):
        """Loads inventory screen"""
        self.clear()
        self.new_label('See the Inventory listed blow', 15
            ).grid(row=0, column=0, columnspan=3)
        for index, row in self.inventory.iterrows():
            # print(row)
            self.new_label(row['name'].upper(), 10
                ).grid(row=index+1, column=0)
            self.new_label(f"{row['amount']} {row['unit']}", 10
                ).grid(row=index+1, column=1)
        self.back_button(self.start_screen)

    def transaction_screen(self):
        """Loads transaction screen"""
        pass

    def new_label(self, text, textSize):
        '''
        Create a new label

        :param text What text the label displays
        :param textSize What size the text is
        '''
        self.label = Label(self,
                    text = text,
                    font = ('Veridian', textSize),
                    padx = 3, pady = 6,)
        self.widgets.append(self.label)
        return self.label

    def new_entry(self, text=None):
        '''
        Create a new entry with a StringVar

        Returns StringVar for tracing
        '''
        self.stringvar = StringVar(self, text)
        self.entry = Entry(self,
                    textvariable = self.stringvar,
                    width = 20)
        self.entry.pack()
        return self.stringvar

    def back_button(self, cmd):
        '''
        Creates Back Button
        '''
        self.back = Button(self,
                    text = 'Back',
                    font = ('Veridian', 12),
                    padx = 3, pady = 6,
                    command = cmd)
        self.back.pack()
        self.widgets.append(self.back)

    def clear(self):
        """Destroy all widgets currently on the Frame"""
        for widget in self.widgets:
            widget.destroy()

    def exit(self, args = None):
        self.root.destroy()

def create_app(title, data):
    """Creates a new Tkinter application"""
    root = Tk()
    root.title(title)
    app = App(root, data)
    app.start_screen()
    root.mainloop()

if __name__ == "__main__":
    print("no.")
