import requests
import json
import time


def pull_data(setstate, categ):
    with open('bearer_token.txt', 'r') as token_val:
        token_val = token_val.read()
    headers = {
        'Accept': 'application/json',
        'Authorization': f"Bearer {token_val}"
    }
    print("Pulling data at: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    if categ == "state":
        url = (f'https://resultsapi.decisiondeskhq.com/api/v3/races?limit=1&page=1&year=2024'
                     f'&state_name={setstate}&party_id=2')
    elif categ == "deleg":
        url = 'https://resultsapi.decisiondeskhq.com/api/v3/delegates/2024'

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        if categ == "state":
            s_response_data = response.json()
            with open(f'CaucusData/f{setstate}/state_response_data.json', 'w') as s_response_file:
                json.dump(s_response_data, s_response_file, indent=4)
            print(f"State data was retrieved and written to state_response_data.json")
        elif categ == "deleg":
            d_response_data = response.json()
            with open(f'CaucusData/f{setstate}_delegates/deleg_response_data.json', 'w') as d_response_file:
                json.dump(d_response_data, d_response_file, indent=4)
            print(f"Delegate data was retrieved and written to deleg_response_data.json")
    else:
        print("GET request failed with status code:", response.status_code)