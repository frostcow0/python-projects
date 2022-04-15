#!/usr/bin/python
from tkinter import *
import pandas as pd
from datetime import date

test_frame = [['2021-10-12', 'Logan Ragsdale', 'chicken butt'], ['2021-10-12', 'Maya Christo', '2chicken 2butt']]

class Config():
    def __init__(self):
        self.meetings_filename = 'sga_data/meetings.csv'
        self.members_filename = 'sga_data/members.csv'
        self.cabinet_members = []
        self.senators = []
        self.members = []
        self.load()

    def save(self):
        # self.write_meetings()
        self.write_members()

    def load(self):
        self.read_meetings()
        self.read_members()

    def read_meetings(self):
        try:
            self.meetings_df = pd.read_csv(self.meetings_filename, index_col=0)
        except Exception as e:
            print('Error reading meetings: \n\t- ',e)

    def read_members(self):
        try:
            self.members_df = pd.read_csv(self.members_filename, index_col=0)
            for index, row in self.members_df.iterrows():
                new = Member(row['Name'], row['Position'])
                if row['Position'] == 'Senator':
                    self.senators.append(new)
                    self.members.append(new)
                else:
                    self.cabinet_members.append(new)
                    self.members.append(new)
        except Exception as e:
            print('Error reading members: \n\t- ',e)

    def write_meetings(self, d):
        df = pd.DataFrame(data = d, columns = ['Meeting', 'Name', 'Report'])
        df.to_csv(self.meetings_filename)

    def write_members(self):
        # data = [mem.get_list() for mem in self.members]
        # df = pd.DataFrame(data = data, columns = ['Name', 'Position'])
        # df.to_csv(self.members_filename)
        self.members_df.to_csv(self.members_filename)

class Member():
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def get_list(self):
        return [self.name, self.position]

class Meeting():
    def __init__(self, date, reports):
        self.date = date
        self.reports = reports

class App(Frame):
    def __init__(self, master, config):
        Frame.__init__(self, master)
        self.root = master
        self.widgets = []
        self.pack()
        self.config = config

    def start_screen(self):
        """
        Loads initial app screen.
        """
        self.clear()
        self.new_label('Student Governing Association Manager', 15).pack()
        self.report = Button(self,
                    text = 'Reports',
                    font = ('Veridian', 12),
                    padx = 3, pady = 6,
                    width = 15,
                    command = self.meetings)
        self.report.pack()
        self.widgets.append(self.report)
        self.member = Button(self,
                    text = 'Members',
                    font = ('Veridian', 12),
                    padx = 3, pady = 6,
                    width = 15,
                    command = self.members)
        self.member.pack()
        self.widgets.append(self.member)
    
    def meetings(self):
        """
        Loads a list of historical meetings to choose from.
        """
        self.clear()
        self.new_label('Choose a meeting\'s reports to view', 15).pack()
        for meeting in self.config.meetings_df.Meeting.unique():
            temp_df = self.config.meetings_df[self.config.meetings_df['Meeting'] == meeting]
            self.meeting_label = Button(self,
                            text = meeting,
                            font = ('Veridian', 12),
                            padx = 3, pady = 6,
                            width = 15,
                            command = lambda df=temp_df: self.reports(df))
            self.meeting_label.pack()
            self.widgets.append(self.meeting_label)
        self.add = Button(self,
                text = 'New Meeting',
                font = ('Veridian', 12),
                padx = 3, pady = 6,
                width = 15,
                command = self.new_meeting)
        self.add.pack()
        self.widgets.append(self.add)
        self.back_button(self.start_screen)
    
    def reports(self, df):
        """
        Loads a list of Cabinet reports for the chosen meeting.
        """
        self.clear()
        self.new_label(df.loc[0]['Meeting'], 15).pack()
        for index, row in df.iterrows():
            self.new_label(f'{row["Name"]}:\t"{row["Report"]}"', 12).pack()
        self.back_button(self.meetings)

    def members(self):
        self.clear()
        self.new_label('Below is a list of SGA Members', 15).pack()
        for member in self.config.members_df.Name:
            Button_Frame = Frame(self)
            self.new_label(member, 12).pack()
            self.edit_button = Button(self,
                            text = 'EDIT',
                            font = ('Veridian', 10),
                            padx = 1, pady = 2,
                            width = 10,
                            command = lambda m=member: self.edit_member(m))
            self.edit_button.pack(in_ = Button_Frame, side = LEFT)
            self.widgets.append(self.edit_button)
            self.delete_button = Button(self,
                            text = 'DELETE',
                            font = ('Veridian', 10),
                            padx = 1, pady = 2,
                            width = 10,
                            command = lambda m=member: self.delete_member(m))
            self.delete_button.pack(in_ = Button_Frame, side = RIGHT)
            Button_Frame.pack()
            self.widgets.append(self.delete_button)
        self.add_button = Button(self,
                        justify = LEFT,
                        text = 'Add',
                        font = ('Veridian', 12),
                        padx = 3, pady = 6,
                        width = 15,
                        command = self.add_member)
        self.add_button.pack()
        self.widgets.append(self.add_button)

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

    def add_member(self):
        '''
        Opens window for adding a new SGA Member
        '''
        self.clear()
        self.new_label('Add SGA Member', 15).pack()
        Name_Frame = Frame(self)
        Position_Frame = Frame(self)
        self.new_label('Name: ', 12).pack(in_ = Name_Frame, side = LEFT)
        self.name_var = StringVar(self)
        self.name_entry = Entry(self,
                    textvariable = self.name_var,
                    width = 20)
        self.name_entry.pack(in_ = Name_Frame, side = LEFT)
        self.widgets.append(self.name_entry)
        self.new_label('Position: ', 12).pack(in_ = Position_Frame, side = LEFT)
        self.position_var = StringVar(self)
        self.position_entry = Entry(self,
                    textvariable = self.position_var,
                    width = 20)
        self.position_entry.pack(in_ = Position_Frame, side = LEFT)
        self.widgets.append(self.position_entry)
        Name_Frame.pack()
        Position_Frame.pack()
        svars = [self.name_var, self.position_var]
        self.add = Button(self,
                    text = 'Add',
                    font = ('Veridian', 12),
                    padx = 3, pady = 6,
                    command = lambda s=svars: self.create_new_member(s))
        self.add.pack()
        self.widgets.append(self.add)

    def create_new_member(self, svars): # Currently just overwrites existing
        name = svars[0].get()
        position = svars[1].get()
        self.config.members_df.loc[self.config.members_df.index] = [name, position]
        self.members()


    def edit_member(self, member):
        pass

    def delete_member(self, member):
        del self.config.members_df.Name.loc[member]
    
    def new_meeting(self):
        '''
        Add info for a new meeting
        '''
        self.clear()
        today = date.today()
        self.new_label(today, 15).pack()
        entries = []
        for member in self.config.members:
            self.new_label(member.name, 12).pack()
            entries.append(self.new_entry('Enter here'))

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

    def clear(self):
        """
        Destroy all widgets currently on the Frame.
        """
        for widget in self.widgets:
            widget.destroy()

    def exit(self, args = None):
        self.root.destroy()

def create_app(title, config):
    """
    Creates a new Tkinter application.
    """
    root = Tk()
    root.title(title)
    app = App(root, config)
    app.start_screen()
    root.mainloop()
    config.save()

if __name__ == '__main__':
    config = Config()

    create_app('SGA Manager', config)