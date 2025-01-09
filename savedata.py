# File management of profile and event data

import os
import tkinter as tk
from tkinter import ttk

# Creating a new profile
def new_profile(profile_name, window):
    if not os.path.exists('profiles'):
        os.makedirs('profiles')
    
    # Exception handling
    if profile_name == '':
        error_window = tk.Toplevel()
        error_window.title('Error')
        error_window.geometry('200x100')
        error_window.resizable(False, False)

        error_label = ttk.Label(error_window, text='Profile name cannot be empty')
        error_label.pack(pady=10)
    elif f'{profile_name}.txt' in os.listdir('profiles'):
        error_window = tk.Toplevel()
        error_window.title('Error')
        error_window.geometry('200x100')
        error_window.resizable(False, False)

        error_label = ttk.Label(error_window, text='Profile name already exists')
        error_label.pack(pady=10)
    # Create new profile file in profiles folder
    else:
        with open(f'profiles/{profile_name}.txt', 'w') as file:
            file.write('')
        window.destroy()

# Loading a profile from previously created
def load_profile(profile_name, window):
    if not os.path.exists('profiles'):
        error_window = tk.Toplevel()   
        error_window.title('Error')
        error_window.geometry('200x100')
        error_window.resizable(False, False)

        error_label = ttk.Label(error_window, text='Profile folder not found')
        error_label.pack(pady=10)

    elif f'{profile_name}.txt' not in os.listdir('profiles'):
        error_window = tk.Toplevel()
        error_window.title('Error')
        error_window.geometry('200x100')
        error_window.resizable(False, False)

        error_label = ttk.Label(error_window, text='Profile not found')
        error_label.pack(pady=10)

    else:
        with open(f'profiles/{profile_name}.txt', 'r') as file:
            pass
        window.destroy()    

def save_profile(profile_name):
    pass
    
    