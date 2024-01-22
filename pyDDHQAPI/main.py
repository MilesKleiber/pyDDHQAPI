import os
import platform
from datetime import datetime

import data_filter
import data_pull
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


def get_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%-m/%d") if platform.system() != "Windows" else current_date.strftime(
        "%#m/%d")
    return formatted_date


def manage_dirs():
    filteredfp = 'CaucusData/'
    if not os.path.exists(filteredfp):
        os.makedirs(filteredfp)
        print(f"Directory '{filteredfp}' created successfully.")
    else:
        print(f"Directory '{filteredfp}' already exists. Continuing.")

    national_deleg_dir = filteredfp + 'National_delegates/'
    if not os.path.exists(national_deleg_dir):
        os.makedirs(national_deleg_dir)
        print(f"Directory '{national_deleg_dir}' created successfully.")
    else:
        print(f"Directory '{national_deleg_dir}' already exists. Continuing.")

    return filteredfp, national_deleg_dir


if __name__ == '__main__':
    formatted_date = get_date()
    print("Current date set to: " + formatted_date)

    # test date
    formatted_date = '1/15'

    if formatted_date in race_list:
        data_pull.pull_data(None, categ='deleg')
        filteredfp, national_deleg_dir = manage_dirs()
        for state in race_list[formatted_date]:
            setstate = state
            print("\nCurrent state set to: " + setstate)
            state_dir = filteredfp + setstate + '/'
            if not os.path.exists(state_dir):
                os.makedirs(state_dir)
                print(f"Directory '{state_dir}' created successfully.")
            else:
                print(f"Directory '{state_dir}' already exists. Continuing.")

            data_pull.pull_data(setstate, categ='state')
            data_filter.state_filter(setstate, state_dir)
            data_filter.delegate_filter(setstate, state_dir, national_deleg_dir)
            print(setstate + " done.\n")
    else:
        print("Race(s) not found for today.\n")
