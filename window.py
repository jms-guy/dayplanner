import tkinter as tk
from tkinter import ttk
from savedata import *
import os

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Main window setup
        self.title("Day Planner")
        self.geometry("1400x800")
        self.minsize(1400,800)
        self.maxsize(1400,800)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Menu setup
        self.menu = MainMenu(self)
        self.menu.grid(row=0, column=0, sticky='NW')

        # Calendar setup
        self.calendar = CalendarFrame(self)
        self.calendar.grid(row=1, column=0, sticky='NW')

        # Time of day & event setup
        self.time = TimeFrame(self)
        self.time.grid(row=1, column=3, sticky='N')

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
        self.change_month = ttk.Button(self, text='Change Month', command=lambda: parent.calendar.main_calendar_change(parent, self.months.get(), self.years.get()))
        self.change_month.grid(row=0, column=2, padx=5)

        # Add blank space
        self.blank = ttk.Label(self, text='                              ')
        self.blank.grid(row=0, column=3, padx=5)

        # New profile button -> create new profile
        self.new_profile = ttk.Button(self, text='New Profile', command=self.open_new_profile_window)
        self.new_profile.grid(row=0, column=5, padx=5)

        # Load profile button -> load existing profile
        self.load_profile = ttk.Button(self, text='Load Profile', command=self.open_load_profile_window)
        self.load_profile.grid(row=0, column=6, padx=5)

        # Save profile button -> save current profile
        self.save_profile = ttk.Button(self, text='Save Profile')
        self.save_profile.grid(row=0, column=7, padx=5)

        ############### Insert textvariable later#################
        # Current profile label -> display current profile
        self.current_profile = ttk.Label(self, text='Current Profile:                            ')
        self.current_profile.grid(row=0, column=8, padx=5)

        # Search events button -> search for events
        self.search_events = ttk.Button(self, text='Search Events')
        self.search_events.grid(row=0, column=9, padx=5)

    # Open new profile window for button
    def open_new_profile_window(self):
        self.new_profile_window = tk.Toplevel(self)
        self.new_profile_window.title('Create Profile')
        self.new_profile_window.geometry('300x100')
        self.new_profile_window.resizable(False, False)

        self.new_profile_label = ttk.Label(self.new_profile_window, text='Enter profile name:')
        self.new_profile_label.grid(row=0, column=0, padx=5, pady=5)

        self.new_profile_entry = ttk.Entry(self.new_profile_window)
        self.new_profile_entry.grid(row=0, column=1, padx=5, pady=5)

        self.new_profile_button = ttk.Button(self.new_profile_window, text='Save', command=lambda: new_profile(self.new_profile_entry.get(), self.new_profile_window))
        self.new_profile_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Open load profile window for button
    def open_load_profile_window(self):
        self.load_profile_window = tk.Toplevel(self)
        self.load_profile_window.title('Load Profile')
        self.load_profile_window.geometry('300x300')
        self.load_profile_window.resizable(False, False)

        self.load_profile_label = ttk.Label(self.load_profile_window, text='Current profiles:')
        self.load_profile_label.grid(row=0, column=0, padx=5, pady=5)

        self.load_profile_listbox = tk.Listbox(self.load_profile_window)
        self.load_profile_listbox.grid(row=0, column=1, padx=5, pady=5)

        # Populate listbox with profiles
        if os.path.exists('profiles'):
            for profile in os.listdir('profiles'):
                self.load_profile_listbox.insert(tk.END, profile)

        self.load_profile_button = ttk.Button(self.load_profile_window, text='Load', command=lambda: load_profile(self.load_profile_listbox.get(tk.ACTIVE), self.load_profile_window))
        self.load_profile_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Calendar frame
class CalendarFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=2, column=0, columnspan=5, sticky='NW')
        
        self.calendarbox = ttk.LabelFrame(self, text=f"{parent.menu.months.get()} {parent.menu.years.get()}", width=1100, height=750)
        self.calendarbox.grid(row=4, column=7, sticky='NWES', padx=10, pady=10)
        self.calendarbox.grid_propagate(False)

        # List of buttons representing days
        self.days_of_month = []

    # Function to change calendar frames based on month and year
    def main_calendar_change(self, parent, month, year):
        
        # Destroys previous month's buttons
        self.calendarbox.config(text=f"{month} {year}")
        if len(self.days_of_month) > 0:
            for day in self.days_of_month:
                day.destroy()
            self.days_of_month.clear()
        
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
        
         # Create buttons for each day in the calendar
        for i in range(1, num_of_days+1):
            day_button = ttk.Button(self.calendarbox, text=f"{i}")
            if i <= 7:
                day_button.grid(row=0, column=i-1, ipadx=36, ipady=58)
            elif i <= 14:
                day_button.grid(row=1, column=i-8, ipadx=36, ipady=58)
            elif i <= 21:
                day_button.grid(row=2, column=i-15, ipadx=36, ipady=58)
            elif i <= 28:
                day_button.grid(row=3, column=i-22, ipadx=36, ipady=58)
            elif i <= 31:
                day_button.grid(row=4, column=i-29, ipadx=36, ipady=58)
            day_button.bind("<Button-1>", lambda event, month=month, day=day_button['text']: parent.time.event_button_creation(month, day))
            self.days_of_month.append(day_button)

        # Add event button to each day
        for day in self.days_of_month:
            day.bind("<Button-1>", lambda event, month=month, day=day['text']: parent.time.event_button_creation(month, day))


# Time of day & event frame
class TimeFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=1, column=5, columnspan=5, sticky='NW')

        # Time of day labelframe to the right of the calendar
        self.timeofday = ttk.LabelFrame(self, text='Events', width=210, height=750)  
        self.timeofday.grid(row=0, column=2, columnspan=4, sticky='NSE', padx=10, pady=10)
        self.timeofday.grid_propagate(False)

        self.hours = []

    
    def event_button_creation(self, month, day):

        self.timeofday.config(text=f"Events for {month} {day}")
        #Destroy previous event buttons
        if len(self.hours) > 0:
            for hour in self.hours:
                hour.destroy()

        #Create buttons for each hour of the day
        for i in range(24):
            self.hour = ttk.Button(self.timeofday, text=f"{i}:00")
            self.hour.grid(row=i, column=0, ipadx=60, ipady=1)
            self.hours.append(self.hour)


        



        

# Main loop

if __name__ == "__main__":
    app = MainApp()


