import os
import platform
import threading
import time
from datetime import datetime

import data_filter
import data_pull
import guinterface
import ddhqauth

race_list = {
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


def manage_dirs():
    dirs = ['CaucusData/', 'CaucusData/National_delegates/']
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
        print(f"Directory '{dir}' ensured to exist.")
    return dirs[0], dirs[1]


keep_running = True


def run_logic(minutes, setdate):
    global keep_running
    data_interval = minutes * 60
    previous_precincts_reporting_percent = 0.0
    while keep_running:
        if setdate in race_list:
            filteredfp, national_deleg_dir = manage_dirs()
            delegate_time = data_pull.pull_data(None, categ='deleg')
            for state in race_list[setdate]:
                setstate = state
                print("\nCurrent state set to: " + setstate)
                state_dir = filteredfp + setstate + '/'
                if not os.path.exists(state_dir):
                    os.makedirs(state_dir)
                    print(f"Directory '{state_dir}' created successfully.")
                else:
                    print(f"Directory '{state_dir}' already exists. Continuing.")

                state_time = data_pull.pull_data(setstate, categ='state')
                data_filter.state_filter(setstate, state_dir)
                guinterface.state_data_time_label.config(text=state_time)
                data_filter.delegate_filter(setstate, state_dir, national_deleg_dir)
                guinterface.delegate_data_time_label.config(text=delegate_time)
                print(setstate + " done.\n")
        else:
            print("Race(s) not found for today.\n")
        time.sleep(data_interval)
        if not keep_running:
            return


if __name__ == '__main__':
    minutes, setdate = guinterface.confirm_values()
    threading.Thread(target=run_logic).start()  # Start the logic in a new thread
