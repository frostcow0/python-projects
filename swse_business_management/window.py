# Third Party
import logging
from tkinter import *

# Proprietary
from database import Database


class App(Frame):
    def __init__(self, master, data:dict, db:Database):
        Frame.__init__(self, master)
        self.configure(bg="tan")
        self.root = master
        self.db = db
        self.widgets = []
        self.grid(padx=20, pady=20)
        self.inventory = data['inventory']
        self.transactions = data['transactions']

    def start_screen(self):
        """Loads initial app screen"""
        self.clear()
        self.new_label('SWSE Business Manager', 15
            ).grid(row=0, column=0, columnspan=3)
        self.inv = Button(self,
                    text = 'Inventory',
                    font = ('Veridian', 12),
                    padx = 3, pady =6,
                    width = 15,
                    command = self.inventory_screen)
        self.inv.grid(row=1, column=0, columnspan=3, pady=10)
        self.widgets.append(self.inv)
        self.transaction = Button(self,
                    text = 'Transactions',
                    font = ('Veridian', 12),
                    padx = 3, pady = 6,
                    width = 15,
                    command = self.transaction_screen)
        self.transaction.grid(row=2, column=0, columnspan=3)
        self.widgets.append(self.transaction)
        self.set_background()

    def inventory_screen(self):
        """Loads inventory screen"""
        self.clear()
        self.new_label('See the Inventory listed blow', 15
            ).grid(row=0, column=0, columnspan=3)
        back_row = 2
        try:
            for index, row in self.inventory.iterrows():
                self.new_label(row['item'], 10
                    ).grid(row=index+1, column=0)
                self.new_label(f"{row['quantity']} {row['unit']}", 10
                    ).grid(row=index+1, column=1)
            back_row = len(self.inventory.index)
        except AttributeError:
            self.new_label('No Inventory yet', 12
                ).grid(row=1, column=1)
        self.back_button(self.start_screen)
        self.back.grid(row=back_row,
            column=1)
        self.set_background()

    def transaction_screen(self):
        """Loads transaction screen"""
        self.clear()
        self.new_label('See the Transaction log below', 15
            ).grid(row=0, column=0, columnspan=4)
        back_row = 2
        try:
            for index, row in self.transactions.iterrows():
                for idx, column in enumerate(self.transactions.columns):
                    if column == "trans_type":
                        if row[column] == 0:
                            pass # change color red
                        else:
                            pass # change color green
                    self.new_label(row[column], 10
                        ).grid(row=index+1, column=idx)
            if len(self.transactions.index) > back_row:
                back_row = len(self.transactions.index)
        except AttributeError:
            self.new_label('No Transactions yet', 12
                ).grid(row=1, column=1)
        self.new_tran = Button(self,
                    text = 'New Transaction',
                    font = ('Veridian', 10),
                    padx = 3, pady = 6,
                    width = 15,
                    command = self.new_transaction)
        self.new_tran.grid(row=back_row,
            column=0, columnspan=3)
        self.widgets.append(self.new_tran)
        self.back_button(self.start_screen)
        self.back.grid(row=back_row+1,
            column=0, columnspan=3)
        self.set_background()

    def new_transaction(self):
        """Adds a new transaction to the DataFrame"""
        self.clear()
        self.new_label("Enter Transaction Info", 15
            ).grid(row=0, column=0, columnspan=3)
        self.new_label("Client Name", 12
            ).grid(row=1, column=0)
        self.c_name = Entry(self,
            width=20)
        self.c_name.grid(row=1, column=1, padx=10)
        self.widgets.append(self.c_name)
        self.new_label("Item", 12
            ).grid(row=2, column=0)
        self.item = Entry(self,
            width=20)
        self.item.grid(row=2, column=1, padx=10)
        self.widgets.append(self.item)
        self.new_label("Quantity", 12
            ).grid(row=3, column=0)
        self.quantity = Entry(self,
            width=20)
        self.quantity.grid(row=3, column=1, padx=10)
        self.widgets.append(self.quantity)
        self.new_label("Price", 12
            ).grid(row=4, column=0)
        self.price = Entry(self,
            width=20)
        self.price.grid(row=4, column=1, padx=10)
        self.price.bind("<Return>", self.add_transaction)
        self.widgets.append(self.price)
        self.trans_type = IntVar()
        self.sale = Radiobutton(self,
            variable=self.trans_type,
            value=1,
            text="Sale")
        self.sale.grid(row=5, column=0, pady=5)
        self.widgets.append(self.sale)
        self.purchase = Radiobutton(self,
            variable=self.trans_type,
            value=0,
            text="Purchase")
        self.purchase.grid(row=5, column=1, pady=5)
        self.widgets.append(self.purchase)
        self.submit = Button(self,
                    text = 'Submit',
                    font = ('Veridian', 10),
                    padx = 3, pady = 6,
                    width = 15,
                    command = self.add_transaction)
        self.submit.grid(row=6, column=0, columnspan=3,
            pady=5)
        self.widgets.append(self.submit)
        self.set_background()

    def add_transaction(self, args=None):
        """Adds transaction info to database"""
        data = [self.trans_type.get(), self.c_name.get(),
            self.item.get().upper(), int(self.quantity.get()),
            int(self.price.get())]
        logging.debug(" Submitted transaction data: %s " % data)
        self.db.store_transaction([data])
        self.refresh_transactions()
        self.transaction_screen()

    def refresh_inventory(self):
        """Pulls latest database info"""
        self.inventory = self.db.get_inventory()

    def refresh_transactions(self):
        """Pulls latest database info"""
        self.transactions = self.db.get_transactions()

    def set_background(self):
        """Sets background color for widgets"""
        for widget in self.widgets:
            widget.configure(bg="tan")

    def new_label(self, text, textSize):
        # from tkinter_tinkering.py
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

    def back_button(self, cmd):
        # from tkinter_tinkering.py
        '''
        Creates Back Button
        '''
        self.back = Button(self,
                    text = 'Back',
                    font = ('Veridian', 10),
                    padx = 1, pady = 2,
                    command = cmd)
        self.widgets.append(self.back)

    def clear(self):
        # from tkinter_tinkering.py
        """Destroy all widgets currently on the Frame"""
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []

    def exit(self, args = None):
        # from tkinter_tinkering.py
        self.root.destroy()

def create_app(title, data, db):
    """Creates a new Tkinter application"""
    root = Tk()
    root.title(title)
    root["bg"] = "tan"
    app = App(root, data, db)
    app.start_screen()
    # app.new_transaction()
    root.mainloop()

if __name__ == "__main__":
    print("no.")
