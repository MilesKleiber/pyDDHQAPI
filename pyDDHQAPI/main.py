import os
import platform
import threading
import time
from datetime import datetime

import data_filter
import data_pull
import guinterface

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


keep_running = True
pause_pushing = False
previous_precincts_reporting_percent = {}


def run_logic(minutes, setdate, expected_turnout, max_jump):
    global keep_running
    global pause_pushing
    global previous_precincts_reporting_percent
    data_interval = minutes * 60

    while keep_running:
        if setdate in race_list:
            filteredfp = 'CaucusData/'
            national_deleg_dir = 'CaucusData/National_delegates/'
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
                current_precincts_reporting_percent, previous_precincts_reporting_percent, status_message = data_filter.state_filter(
                    setstate, state_dir, expected_turnout, pause_pushing, previous_precincts_reporting_percent,
                    max_jump)
                guinterface.precincts_reporting_status_value_label.config(text=status_message)
                if abs(current_precincts_reporting_percent - previous_precincts_reporting_percent[setstate]) > max_jump:
                    guinterface.precincts_reporting_status_value_label.config(text="Jump Detected! Pausing data value "
                                                                                   "output.")
                    pause_pushing = True
                data_filter.delegate_filter(setstate, state_dir, national_deleg_dir)
                guinterface.delegate_data_time_label.config(text=delegate_time)
                guinterface.state_data_time_label.config(text=state_time)
                print(setstate + " done.\n")
        else:
            print("Race(s) not found for today.\n")
        time.sleep(data_interval)
        if not keep_running:
            return


if __name__ == '__main__':
    minutes, setdate = guinterface.confirm_values()
    threading.Thread(target=run_logic).start()
