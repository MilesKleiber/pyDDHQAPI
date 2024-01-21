import os
import json
import platform
from datetime import datetime
import data_pull
import data_filter
import ddhqauth


RACE_LIST_DB="2024_primary_dates.json"


def __init__(self=None):

def get_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%-m/%d") if platform.system() != "Windows" else current_date.strftime(
        "%#m/%d")
    return formatted_date


def manage_dirs(setstate):
    filteredfp = 'CaucusData/'
    if not os.path.exists(filteredfp):
        os.makedirs(filteredfp)
        print(f"Directory '{filteredfp}' created successfully.")
    else:
        print(f"Directory '{filteredfp}' already exists. Continuing.")

    state_dir = filteredfp + setstate + '/'
    if not os.path.exists(state_dir):
        os.makedirs(state_dir)
        print(f"Directory '{state_dir}' created successfully.")
    else:
        print(f"Directory '{state_dir}' already exists. Continuing.")

    state_deleg_dir = filteredfp + setstate + '_delegates/'
    if not os.path.exists(state_deleg_dir):
        os.makedirs(state_deleg_dir)
        print(f"Directory '{state_deleg_dir}' created successfully.")
    else:
        print(f"Directory '{state_deleg_dir}' already exists. Continuing.")

    national_deleg_dir = filteredfp + 'National_delegates/'
    if not os.path.exists(national_deleg_dir):
        os.makedirs(national_deleg_dir)
        print(f"Directory '{national_deleg_dir}' created successfully.")
    else:
        print(f"Directory '{national_deleg_dir}' already exists. Continuing.")

    return state_dir, state_deleg_dir, national_deleg_dir


if __name__ == '__main__':
    formatted_date = get_date()  # Call get_date and store the returned value
    print("Current date set to: " + formatted_date)

    with open(RACE_LIST_DB, 'r') as dates_db:
        date_list = json.load(dates_db)

    for date in date_list['races']:
        if date['date'] == formatted_date:
            for state in date['states']:
                setstate = date['states'][state]
                state_dir, state_deleg_dir, national_deleg_dir = manage_dirs(setstate)
                data_pull.pull_data(setstate, categ='state')
                data_pull.pull_data(setstate, categ='deleg')
                data_filter.state_filter(setstate, state_dir)
                data_filter.delegate_filter(setstate, state_deleg_dir, national_deleg_dir)