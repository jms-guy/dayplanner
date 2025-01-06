import tkinter as tk
from tkinter import ttk

class MainApp(tk.Tk):
    def __init__(self):

        # Main window setup
        super().__init__()
        self.title("Day Planner")
        self.geometry("1400x800")
        self.minsize(1400,800)
        self.maxsize(1400,800)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Menu setup
        self.menu = MainMenu(self)
        self.menu.grid(row=0, column=0, sticky='NW')

        # Calendar setup
        self.calendar = CalendarFrame(self)
        self.calendar.grid(row=1, column=0, sticky='NW')

        # Main loop
        self.mainloop()

# Menu class
class MainMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, columnspan=5, sticky='NW')

        # Select month -> add calender changes to main window
        self.months = ttk.Combobox(self, state='readonly')
        self.months['values'] = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
        self.months.grid(row=0, column=0)
        self.months.current(0)
        
        # Select year -> add calender changes to main window
        self.years = ttk.Combobox(self, state='readonly')
        self.years['values'] = [i for i in range(2025, 2040)]
        self.years.grid(row=0, column=1)
        self.years.current(0)

        s = ttk.Separator(self, orient='horizontal')
        s.grid(row=1, column=0, columnspan=2, sticky='EW')

        # Change month button -> change month in calendar
        self.change_month = ttk.Button(self, text='Change Month')
        self.change_month.grid(row=0, column=2, padx=5)

        # Add event button -> add event to calendar
        self.add_event = ttk.Button(self, text='Add Event')
        self.add_event.grid(row=0, column=3, padx=5)

        # Remove event button -> remove event from calendar
        self.remove_event = ttk.Button(self, text='Remove Event')
        self.remove_event.grid(row=0, column=4, padx=5)

# Calendar frame
class CalendarFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=2, column=0, columnspan=5, sticky='NW')
        
        self.calendarbox = ttk.LabelFrame(self, text=f"{parent.menu.months.get()} {parent.menu.years.get()}", width=1100, height=750)
        self.calendarbox.grid(row=1, column=1, sticky='NW', padx=10, pady=10)








