import os
import threading
import time
import json

import data_filter
import data_pull
import guinterface

with open('pyDDHQAPI/primary_races.json', 'r') as racefile:
    race_list = json.load(racefile)


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
                state_dir = filteredfp + setstate + '/'

                if not os.path.exists(state_dir):
                    os.makedirs(state_dir)

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
                guinterface.precincts_reporting_calculation_values_label.config(
                    text=f"Current: {round(current_precincts_reporting_percent, 1)}, "
                         f"Previous: {round(previous_precincts_reporting_percent[setstate], 1)}")
        time.sleep(data_interval)
        if not keep_running:
            return


if __name__ == '__main__':
    minutes, setdate = guinterface.confirm_values()
    threading.Thread(target=run_logic).start()
