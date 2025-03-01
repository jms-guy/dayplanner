import tkinter as tk
from tkinter import ttk
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
        self.protocol("WM_DELETE_WINDOW", self.close_program)

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

        # Closing the program and deleting temp files
    def close_program(self):
        if os.path.exists('tempchanges.lst'):
            os.remove('tempchanges.lst')
        self.quit()
        self.destroy()

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
        self.change_month = ttk.Button(self, text='Choose Month', command=lambda: parent.calendar.main_calendar_change(parent, self.months.get(), self.years.get()))
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
        self.save_profile = ttk.Button(self, text='Save Profile', command=lambda: save_profile(self.current_profile.cget('text').split(': ')[1]))
        self.save_profile.grid(row=0, column=7, padx=5)

        # Current profile label -> display current profile
        self.current_profile = ttk.Label(self, text='Current Profile: None')
        self.current_profile.grid(row=0, column=9, padx=5)

        # Delete profile button -> delete current profile
        self.delete_profile = ttk.Button(self, text='Delete Profile', command=lambda: delete_profile(self, self.current_profile.cget('text').split(': ')[1]))
        self.delete_profile.grid(row=0, column=8, padx=5)

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
        self.load_profile_window.geometry('300x250')
        self.load_profile_window.resizable(False, False)

        self.load_profile_label = ttk.Label(self.load_profile_window, text='Current profiles:')
        self.load_profile_label.grid(row=0, column=0, padx=5, pady=5)

        self.load_profile_listbox = tk.Listbox(self.load_profile_window)
        self.load_profile_listbox.grid(row=0, column=1, padx=5, pady=5)

        # Populate listbox with profiles
        if os.path.exists('profiles'):
            for profile in os.listdir('profiles'):
                profile_name = profile.split('.')[0]
                self.load_profile_listbox.insert(tk.END, profile_name)

        self.load_profile_button = ttk.Button(self.load_profile_window, text='Load', command=lambda: load_profile(self, self.load_profile_listbox.get(tk.ACTIVE), self.load_profile_window))
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

        style = ttk.Style()
        style.configure('Normal.TButton', padding=5)
        style.configure('Event.TButton', padding=5, background='lightblue')
        style.map('Event.TButton', background=[('active', 'lightblue')])

        if not os.path.exists('tempchanges.lst'):
            error_window = tk.Toplevel()
            error_window.title('Error')
            error_window.geometry('200x100')
            error_window.resizable(False, False)

            error_label = ttk.Label(error_window, text='Please load a profile')
            error_label.pack(pady=10)
        
        else:
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
                valid_monthly_events = []
                if len(profile_event_list) > 0:
                    for event in profile_event_list:
                        event_data = event.split('-', 3)
                        if (event_data[0] != year) or (event_data[1] != month):
                            continue
                        else:
                            if event_data[2] == str(i):
                                valid_monthly_events.append(event_data[3])
                
                if len(valid_monthly_events) != 0:
                    day_button = ttk.Button(self.calendarbox, text=str(i), style='Event.TButton')
                else:
                    day_button = ttk.Button(self.calendarbox, text=str(i), style='Normal.TButton')

                if i <= 7:
                    day_button.grid(row=0, column=i-1, ipadx=34, ipady=57)
                elif i <= 14:
                    day_button.grid(row=1, column=i-8, ipadx=34, ipady=57)
                elif i <= 21:
                    day_button.grid(row=2, column=i-15, ipadx=34, ipady=57)
                elif i <= 28:
                    day_button.grid(row=3, column=i-22, ipadx=34, ipady=57)
                elif i <= 31:
                    day_button.grid(row=4, column=i-29, ipadx=34, ipady=57)
                day_button.bind("<Button-1>", lambda event, year=year, month=month, day=day_button['text']: parent.time.event_button_creation(year, month, day))
                self.days_of_month.append(day_button)

            # Add event button to each day
            for day in self.days_of_month:
                day.bind("<Button-1>", lambda event, month=month, day=day['text']: parent.time.event_button_creation(year, month, day))

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
   
    def event_button_creation(self, year, month, day):

        style = ttk.Style()
        style.configure('Normal.TButton')
        style.configure('Event.TButton', background='lightblue')
        style.map('Event.TButton', background=[('active', 'lightblue')])

        self.timeofday.config(text=f"Events for {month} {day}")
        #Destroy previous event buttons
        if len(self.hours) > 0:
            for hour in self.hours:
                hour.destroy()

        #Create buttons for each hour of the day
        for i in range(1, 24):
            valid_events = []
            if len(profile_event_list) > 0:
                for event in profile_event_list:
                    event_data = event.split('-', 4)
                    if (event_data[0] != year) or (event_data[1] != month) or (event_data[2] != day):
                        continue
                    else:
                        if event_data[3] == str(i):
                            valid_events.append(event_data[4])
            
            if len(valid_events) > 0:
                self.hour = ttk.Button(self.timeofday, text=f"{i}:00", style='Event.TButton')
            else:
                self.hour = ttk.Button(self.timeofday, text=f"{i}:00", style='Normal.TButton')

            self.hour.grid(row=i, column=0, ipadx=60)
            self.hour.bind("<Button-1>", lambda event: self.open_events_window(year, month, day, self.hours[self.hours.index(event.widget)].cget('text').split(':')[0]))
            self.hours.append(self.hour)

    # Open events window for button
    def open_events_window(self, year, month, day, hour):
        self.events_window = tk.Toplevel(self)
        self.events_window.title(f'Events for {hour}:00')
        self.events_window.geometry('300x350')
        self.events_window.resizable(False, False)

        self.events_label = ttk.Label(self.events_window, text='Events:')
        self.events_label.grid(row=0, column=0, padx=5, pady=5)

        self.events_entry = ttk.Entry(self.events_window, textvariable=tk.StringVar())
        self.events_entry.grid(row=0, column=1, padx=5, pady=5)

        self.events_button = ttk.Button(self.events_window, text='Save', command=self.save_events) 
        self.events_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.events_listbox = tk.Listbox(self.events_window)
        self.events_listbox.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        self.get_saved_events(year, month, day, hour)

        self.events_delete_button = ttk.Button(self.events_window, text='Delete', command=self.delete_events)
        self.events_delete_button.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        self.events_window.protocol("WM_DELETE_WINDOW", lambda: self.finalize_event_changes(year, month, day, hour))

    def get_saved_events(self, year, month, day, hour):
        if len(profile_event_list) > 0:
            events = []
            for event in profile_event_list:
                event_data = event.split('-')
                if (event_data[0] == str(year)) and (event_data[1] ==str(month)) and (event_data[2] == str(day)) and (event_data[3] == str(hour)):
                    events.append(event_data[4])
            if len(events) > 0:
                for event in events:
                    self.events_listbox.insert(tk.END, event)

    def save_events(self):
        self.events_listbox.insert(tk.END, self.events_entry.get())
        self.events_entry.delete(0, tk.END)

    def delete_events(self):
        selected_event = self.events_listbox.get(tk.ACTIVE)
        if selected_event:
            for event in profile_event_list:
                event_data = event.split('-')
                if event_data[4] == selected_event:
                    profile_event_list.remove(event)
                    break
        self.events_listbox.delete(tk.ACTIVE)

    def finalize_event_changes(self, year, month, day, hour):
        with open('tempchanges.lst', 'a+') as file:
            for event in self.events_listbox.get(0, tk.END):
                file.write(f'{year}-{month}-{day}-{hour}-{event}\n')
        self.events_window.destroy()




###### File management of profile and event data ######

# Creating a new profile
def new_profile(profile_name, window):
    if not os.path.exists('profiles'):
        os.makedirs('profiles')
    
    profile_name = profile_name.strip().capitalize()
    # Exception handling
    if profile_name == '':
        error_window = tk.Toplevel()
        error_window.title('Error')
        error_window.geometry('200x100')
        error_window.resizable(False, False)

        error_label = ttk.Label(error_window, text='Profile name cannot be empty')
        error_label.pack(pady=10)
    elif f'{profile_name}' in os.listdir('profiles'):
        error_window = tk.Toplevel()
        error_window.title('Error')
        error_window.geometry('200x100')
        error_window.resizable(False, False)

        error_label = ttk.Label(error_window, text='Profile name already exists')
        error_label.pack(pady=10)
    # Creates new profile dictionary on a global scale
    else:
        with open(f'profiles/{profile_name}.lst', 'w') as file:
            file.write('')
        window.destroy()

# Loading a profile from previously created
def load_profile(master_window, profile_name, window):
    if not os.path.exists('profiles'):
        error_window = tk.Toplevel()   
        error_window.title('Error')
        error_window.geometry('200x100')
        error_window.resizable(False, False)

        error_label = ttk.Label(error_window, text='Profile folder not found')
        error_label.pack(pady=10)

    elif f'{profile_name}.lst' not in os.listdir('profiles'):
        error_window = tk.Toplevel()
        error_window.title('Error')
        error_window.geometry('200x100')
        error_window.resizable(False, False)

        error_label = ttk.Label(error_window, text='Profile not found')
        error_label.pack(pady=10)

    # Load the profile data from save file and import data
    else:
        with open(f'profiles/{profile_name}.lst', 'r') as file:
            global profile_event_list
            profile_event_list = [line.strip() for line in file if line.strip()]
        with open('tempchanges.lst', 'w') as file:
            file.write('')
        window.destroy()
        master_window.current_profile.config(text=f'Current Profile: {profile_name}')

def save_profile(profile_name):
    if profile_name != 'None':
        # Read new events from temp file
        with open('tempchanges.lst', 'r') as temp_file:
            temp_events = set(temp_file.read().splitlines())
            
        # Combine with existing profile_event_list
        all_events = set(profile_event_list)  
        all_events.update(temp_events)        
        
        # Write everything back to main file
        with open(f'profiles/{profile_name}.lst', 'w') as file:
            for event in sorted(all_events): 
                file.write(event + '\n')
                
        os.remove('tempchanges.lst')
    else:
        error_message = tk.Toplevel()
        error_message.title('Error')
        error_message.geometry('300x50')
        error_message.resizable(False, False)

        error_label = ttk.Label(error_message, text='No profile selected')
        error_label.pack(pady=5)
 
 # Deletes profile
def delete_profile(parent, profile_name):
    confirmation_window = tk.Toplevel()
    confirmation_window.title('Confirmation')
    confirmation_window.geometry('300x200')
    confirmation_window.resizable(False, False)

    confirmation_label = ttk.Label(confirmation_window, text=f'Are you sure you want to delete {profile_name}?')
    confirmation_label.pack(pady=10)

    confirmation_yes = ttk.Button(confirmation_window, text='Yes', command=lambda: delete_profile_confirm(parent, profile_name, confirmation_window))
    confirmation_yes.pack(pady=10)
    confirmation_no = ttk.Button(confirmation_window, text='No', command=confirmation_window.destroy)
    confirmation_no.pack(pady=10)

def delete_profile_confirm(parent, profile_name, window):
    os.remove(f'profiles/{profile_name}.lst')
    window.destroy()
    parent.current_profile.config(text='Current Profile: None')

# Main loop

if __name__ == "__main__":
    app = MainApp()


