import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import sv_ttk
import threading
import main

root = tk.Tk()
root.title("pyDDHQAPI GUI")
root.geometry("500x600")
style = ttk.Style(root)


def start_main_logic():
    threading.Thread(target=main.run_logic, args=(minutes, setdate)).start()
    status_label.config(text="Status: Started")

def stop_logic():
    main.keep_running = False
    status_label.config(text="Status: Stopped")

def date_selection_menu(root, options):
    selected_date = tk.StringVar(root)
    selected_date.set(options[0])

    combo_box = (ttk.Combobox(root, width=12, textvariable=selected_date, values=options))
    combo_box.grid(column=1, row=1, padx=0, pady=5)

    return selected_date


def states_selected(root, selected_date):
    ttk.Label(root, text="States being pulled:", font=10).grid(column=0, row=2, padx=0, pady=0)
    states_text = Text(root, width=30, height=15, borderwidth=2, relief="groove")
    states_text.grid(column=1, row=2, padx=0, pady=5)
    states_text.insert('end', '\n'.join(races[selected_date.get()]))

    def update_states(*args):
        states_text.delete('1.0', 'end')
        states_text.insert('end', '\n'.join(races[selected_date.get()]))

    selected_date.trace('w', update_states)

    return states_text


def update_label(value):
    slider_label.config(text=f"Data interval: {int(float(value))} minutes")


def confirm_values():
    global minutes
    global setdate
    minutes = int(minutes_spinbox.get())
    setdate = str(selected_date.get())
    print(f"Confirmed data request interval: {minutes} minutes")
    print(f"Confirmed date: {setdate}")
    start_main_logic()
    return minutes, setdate


races = {
    "1/15": ["Iowa"],
    "1/23": ["New Hampshire"],
    "2/06": ["Nevada"],
    "2/08": ["Virgin Islands"],
    "2/24": ["South Carolina"],
    "2/27": ["Michigan"],
    "3/02": ["Idaho", "Missouri"],
    "3/04": ["North Dakota"],
    "3/05": ["Alabama", "Arkansas", "California", "Colorado", "Maine", "Massachusetts", "Minnesota", "North Carolina",
             "Oklahoma", "Tennessee", "Texas", "Utah", "Vermont", "Virginia"],
    "3/12": ["Georgia", "Hawaii", "Mississippi", "Washington"],
    "3/19": ["Arizona", "Florida", "Illinois", "Kansas", "Ohio"],
    "3/23": ["Louisiana"],
    "4/02": ["Connecticut", "Delaware", "New York", "Rhode Island", "Wisconsin"],
    "4/23": ["Pennsylvania"],
    "5/07": ["Indiana"],
    "5/14": ["Maryland", "Nebraska", "West Virginia"],
    "5/21": ["Kentucky", "Oregon"],
    "6/04": ["D.C.", "Montana", "New Jersey", "New Mexico", "South Dakota"]
}

head_label = ttk.Label(root, text="pyDDHQAPI Data Selection", font=("Calibri", 20))
head_label.grid(column=1, row=0, padx=0, pady=10)

dates = list(races.keys())
ttk.Label(root, text="Select the race date:", font=10).grid(column=0, row=1, padx=0, pady=0)
selected_date = date_selection_menu(root, dates)
states_text = states_selected(root, selected_date)

minutes_spinbox = ttk.Spinbox(root, from_=1, to=20, width=5)
minutes_spinbox.set(1)  # Set the default value to 1
minutes_spinbox.grid(column=1, row=3, padx=0, pady=0)

minutes_label = ttk.Label(root, text="Data interval (minutes):")
minutes_label.grid(column=0, row=3, padx=0, pady=0)

state_data_time_label = ttk.Label(root, text="State data last updated:", font=10)
state_data_time_label.grid(column=1, row=10, padx=0, pady=0)

delegate_data_time_label = ttk.Label(root, text="Delegate data last updated:", font=10)
delegate_data_time_label.grid(column=1, row=11, padx=0, pady=0)

style.configure("Green.TButton", foreground="green")

confirm_button = ttk.Button(root, text="Start", command=confirm_values, style="Green.TButton")
confirm_button.grid(column=1, row=12, padx=0, pady=10)

style.configure("Red.TButton", foreground="red")

stop_button = ttk.Button(root, text="Stop", command=stop_logic, style="Red.TButton")
stop_button.grid(column=1, row=13, padx=0, pady=10)

status_label = ttk.Label(root, text="Status: Stopped", font=10)
status_label.grid(column=1, row=14, padx=0, pady=10)

sv_ttk.set_theme("dark")

root.mainloop()


