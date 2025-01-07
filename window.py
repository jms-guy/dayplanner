import tkinter as tk
from tkinter import ttk
from datetime import datetime

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

# Menu frame
class MainMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, columnspan=5, sticky='NW')

        # Select month -> add calender changes to main window
        self.months = ttk.Combobox(self, state='readonly')
        self.months['values'] = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
        self.months.grid(row=0, column=0)
        self.months.current(0)
        self.months.focus_set()
        
        # Select year -> add calender changes to main window
        self.years = ttk.Combobox(self, state='readonly')
        self.years['values'] = [i for i in range(2025, 2040)]
        self.years.grid(row=0, column=1)
        self.years.current(0)

        s = ttk.Separator(self, orient='horizontal')
        s.grid(row=1, column=0, columnspan=2, sticky='EW')

        # Change month button -> change month in calendar
        self.change_month = ttk.Button(self, text='Change Month', command=lambda: parent.calendar.main_calendar_change(self.months.get(), self.years.get()))
        self.change_month.grid(row=0, column=2, padx=5)

        # Add event button -> add event to calendar
        self.add_event = ttk.Button(self, text='Add Event')
        self.add_event.grid(row=0, column=3, padx=5)

        # Remove event button -> remove event from calendar
        self.remove_event = ttk.Button(self, text='Remove Event')
        self.remove_event.grid(row=0, column=4, padx=5)

        # New profile button -> create new profile
        self.new_profile = ttk.Button(self, text='New Profile')
        self.new_profile.grid(row=0, column=5, padx=5)

        # Load profile button -> load existing profile
        self.load_profile = ttk.Button(self, text='Load Profile')
        self.load_profile.grid(row=0, column=6, padx=5)

        # Save profile button -> save current profile
        self.save_profile = ttk.Button(self, text='Save Profile')
        self.save_profile.grid(row=0, column=7, padx=5)

        # Current profile label -> display current profile
        self.current_profile = ttk.Label(self, text='Current Profile: ')
        self.current_profile.grid(row=0, column=8, padx=5)


# Calendar frame
class CalendarFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=2, column=0, columnspan=5, sticky='NW')
        
        self.calendarbox = ttk.LabelFrame(self, text=f"{parent.menu.months.get()} {parent.menu.years.get()}", width=1100, height=750)
        self.calendarbox.grid(row=4, column=7, sticky='NWES', padx=10, pady=10)

        # List of buttons representing days
        self.days_of_month = []

    # Function to change calendar frames based on month and year
    def main_calendar_change(self, month, year):

        self.calendarbox.config(text=f"{month} {year}")
        self.destroy_calendar()
        
        # Get number of days in month
        num_of_days = 0
        if month in ['January', 'March', 'May', 'July', 'August', 'October', 'December']:
            num_of_days = 31
        elif month in ['April', 'June', 'September', 'November']:
            num_of_days = 30
        elif month == 'February' and int(year) % 4 == 0:
            num_of_days = 29
        else:
            num_of_days = 28
        
        # Create buttons for each day in the calendar, create new rows for each week
        for i in range(1, num_of_days+1):
            if i <= 7:
                self.day = ttk.Button(self.calendarbox, text=f"{i}")
                self.day.grid(row=0, column=i-1)
            elif i <= 14:
                self.day = ttk.Button(self.calendarbox, text=f"{i}")

                self.day.grid(row=1, column=i-8)
            elif i <= 21:
                self.day = ttk.Button(self.calendarbox, text=f"{i}")
                self.day.grid(row=2, column=i-15)
            elif i <= 28:
                self.day = ttk.Button(self.calendarbox, text=f"{i}")
                self.day.grid(row=3, column=i-22)
            elif i <= 31:
                self.day = ttk.Button(self.calendarbox, text=f"{i}")
                self.day.grid(row=4, column=i-29)
            self.days_of_month.append(self.day)

    # Function to destroy current calendar buttons
    def destroy_calendar(self):
        for day in self.days_of_month:
            day.destroy()



        



        


# Main loop

if __name__ == "__main__":
    app = MainApp()


