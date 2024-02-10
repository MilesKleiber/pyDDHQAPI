import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import main
import json
from ddhqauth import authenticate

root = tk.Tk()
root.title("pyDDHQAPI GUI")
root.geometry("500x900")
root.resizable(True, True)

style = ttk.Style(root)


def start_main_logic():
    threading.Thread(target=main.run_logic, args=(minutes, setdate, expected_turnout.get(), max_jump)).start()
    status_label.config(text="Status: Started")


def stop_logic():
    main.keep_running = False
    status_label.config(text="Status: Stopped")


def date_selection_menu(frame, options):
    selected_date = tk.StringVar(root)
    selected_date.set(options[0])

    option_menu = tk.OptionMenu(frame, selected_date, *options)
    option_menu.grid(column=1, row=0, padx=0, pady=0)

    return selected_date


def states_selected(frame, selected_date):
    states_text = Text(frame, width=30, height=22, borderwidth=2, relief="groove")
    states_text.grid(column=2, row=1, padx=10, pady=5, rowspan=12)
    states_text.insert('end', '\n'.join(races[selected_date.get()]))

    def update_states(*args):
        states_text.delete('1.0', 'end')
        states_text.insert('end', '\n'.join(races[selected_date.get()]))

    selected_date.trace('w', update_states)

    return states_text


def set_expected_turnout(frame, options):
    expected_turnout = tk.StringVar(root)
    expected_turnout.set(options[0])

    option_menu = tk.OptionMenu(frame, expected_turnout, *options)
    option_menu.grid(column=1, row=1, padx=0, pady=10)

    return expected_turnout


def confirm_values():
    global minutes
    global setdate
    global max_jump
    minutes = int(minutes_spinbox.get())
    setdate = str(selected_date.get())
    max_jump = int(max_jump_spinbox.get())
    start_main_logic()
    return minutes, setdate, max_jump


def continue_pushing():
    main.pause_pushing = False
    precincts_reporting_status_value_label.config(text="Normal")
    print("Pushing resumed.")


def update_client_creds():
    client_creds = [
        {
            "client_id": client_id_entry.get(),
            "client_secret": client_secret_entry.get()
        }
    ]
    with open('pyDDHQAPI/client_creds.json', 'w') as credentials:
        json.dump(client_creds, credentials)
    authenticate(callback=update_bearer_token_text)


def existing_file_command():
    with open('pyDDHQAPI/client_creds.json', 'r') as credentials:
        client_creds = json.load(credentials)
    print(f"Client ID: {client_creds[0]['client_id']}")
    print(f"Client Secret: {client_creds[0]['client_secret']}")
    authenticate(callback=update_bearer_token_text)


def get_bearer_token():
    with open('pyDDHQAPI/bearer_token.txt', 'r') as token_file:
        return token_file.read()


def update_bearer_token_text():
    bearer_token_text.delete('1.0', 'end')
    bearer_token_text.insert('end', get_bearer_token())
    bearer_token_text.config(state='disabled')


with open('pyDDHQAPI/primary_races.json', 'r') as racefile:
    races = json.load(racefile)

dates = list(races.keys())

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

ttk.Label(root, text="pyDDHQAPI Data Selection", font=("Calibri", 28)).grid(column=0, row=0, padx=3, pady=3)

auth_frame = ttk.Frame(root, borderwidth=2, relief="groove", padding=5, width=700, height=200)
auth_frame.grid(column=0, row=1, padx=0, pady=0)
ttk.Label(auth_frame, text="Enter your Client ID:", font=10).grid(column=0, row=0, padx=0, pady=0)
client_id_entry = ttk.Entry(auth_frame)
client_id_entry.grid(column=1, row=0, padx=0, pady=0)
ttk.Label(auth_frame, text="Enter your Client Secret:", font=10).grid(column=0, row=1, padx=0, pady=0)
client_secret_entry = ttk.Entry(auth_frame)
client_secret_entry.grid(column=1, row=1, padx=0, pady=0)
update_button = ttk.Button(auth_frame, text="Update Client Credentials", command=update_client_creds)
update_button.grid(column=1, row=2, padx=0, pady=2)
new_button = ttk.Button(auth_frame, text="Use Existing File", command=existing_file_command)
new_button.grid(column=1, row=3, padx=0, pady=2)
ttk.Label(auth_frame, text="Current token:", font=10).grid(column=0, row=4, padx=0, pady=0)
bearer_token_text = tk.Text(auth_frame, width=30, height=4, borderwidth=2, relief="groove")
bearer_token_text.grid(column=1, row=4, padx=0, pady=5)

settings_frame = ttk.Frame(root, borderwidth=2, relief="groove", padding=5, width=700, height=200)
settings_frame.grid(column=0, row=2, padx=0, pady=0)
ttk.Label(settings_frame, text="Select the race date:", font=10).grid(column=0, row=0, padx=0, pady=10)
selected_date = date_selection_menu(settings_frame, dates)
ttk.Label(settings_frame, text="Expected reporting value:", font=10).grid(column=0, row=1, padx=15, pady=5)
turnout_options = ['Low', 'Low-Medium', 'Medium', 'Medium-High', 'High']
expected_turnout = set_expected_turnout(settings_frame, turnout_options)
ttk.Label(settings_frame, text="Data interval (minutes):").grid(column=0, row=2, padx=0, pady=0)
minutes_spinbox = ttk.Spinbox(settings_frame, from_=1, to=20, width=5)
minutes_spinbox.set(1)
minutes_spinbox.grid(column=1, row=2, padx=0, pady=0)
max_jump_label = ttk.Label(settings_frame, text="Max precincts reporting jump (%):")
max_jump_label.grid(column=0, row=3, padx=0, pady=0)
max_jump_spinbox = ttk.Spinbox(settings_frame, from_=1, to=100, width=5)
max_jump_spinbox.grid(column=1, row=3, padx=0, pady=0)
max_jump_spinbox.set(10)

status_frame = (ttk.Frame(root, borderwidth=2, relief="groove", padding=5, width=700, height=200))
status_frame.grid(column=0, row=3, padx=0, pady=0)
states_selected(status_frame, selected_date).grid(column=0, row=0, padx=10, pady=5, rowspan=10)
ttk.Label(status_frame, text="State data last updated:", font=10).grid(column=1, row=0, padx=0, pady=0)
state_data_time_label = ttk.Label(status_frame, text="", font=10)
state_data_time_label.grid(column=1, row=1, padx=0, pady=0)
ttk.Label(status_frame, text="Delegate data last updated:", font=10).grid(column=1, row=2, padx=0, pady=0)
delegate_data_time_label = ttk.Label(status_frame, text="", font=10)
delegate_data_time_label.grid(column=1, row=3, padx=0, pady=0)
precincts_reporting_status_label = ttk.Label(status_frame, text="Precincts Reporting Change: ", font=("Calibri", 12))
precincts_reporting_status_label.grid(column=1, row=4, padx=0, pady=0)
precincts_reporting_calculation_values_label = ttk.Label(status_frame, text="", font=("Calibri", 12))
precincts_reporting_calculation_values_label.grid(column=1, row=5, padx=0, pady=0)
precincts_reporting_status_value_label = ttk.Label(status_frame, text="Normal", font=("Calibri", 12))
precincts_reporting_status_value_label.grid(column=1, row=6, padx=0, pady=0)
resume_button = ttk.Button(status_frame, text="Override", command=continue_pushing)
resume_button.grid(column=1, row=7, padx=0, pady=10, columnspan=2)

process_frame = (ttk.Frame(root, borderwidth=2, relief="groove", padding=5, width=700, height=200))
process_frame.grid(column=0, row=4, padx=0, pady=0)
start_button = ttk.Button(process_frame, text="Start", command=confirm_values, style="Green.TButton")
start_button.grid(column=0, row=0, padx=0, pady=10)
stop_button = ttk.Button(process_frame, text="Stop", command=stop_logic, style="Red.TButton")
stop_button.grid(column=1, row=0, padx=0, pady=10)
status_label = ttk.Label(process_frame, text="Status: Stopped", font=10)
status_label.grid(column=0, row=1, padx=0, pady=0, columnspan=2)
style.configure("Green.TButton", foreground="green")
style.configure("Red.TButton", foreground="red")

root.mainloop()
