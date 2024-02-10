import json


def state_filter(setstate, state_dir, expected_turnout, pause_pushing, previous_precincts_reporting_percent, max_jump):
    with open(state_dir + f'{setstate}_response_data.json', 'r') as s_response_file:
        s_response_data = json.load(s_response_file)

    if s_response_data['total'] == 0:
        return
    else:
        cand_list = s_response_data['data'][0]['candidates']
        for candidates in cand_list:
            cand_name = candidates['last_name']
            cand_id = candidates['cand_id']
            total_votes = s_response_data['data'][0]['topline_results']['total_votes']
            cand_votes = s_response_data['data'][0]['topline_results']['votes'].get(str(cand_id))
            file_name = f"{cand_name}_{setstate}_votes.txt"
            with open(state_dir + file_name, 'w') as file:
                file.write(str(cand_votes))
            if cand_votes <= 0.0:
                cand_percent = 0.0
            elif total_votes <= 0.0:
                cand_percent = 0.0
            else:
                cand_percent = float(cand_votes / total_votes) * 100
            pfile_name = f"{cand_name}_{setstate}_percent.txt"
            with open(state_dir + pfile_name, 'w') as file:
                if cand_percent == 100.0:
                    file.write("100")
                else:
                    file.write(f"{cand_percent:.1f}")

        total_state_votes_in = s_response_data['data'][0]['topline_results']['total_votes']
        if expected_turnout == 'Low':
            estimated_state_votes = s_response_data['data'][0]['topline_results']['estimated_votes']['estimated_votes_low']
        elif expected_turnout == 'Low-Medium':
            estimated_state_votes = (s_response_data['data'][0]['topline_results']['estimated_votes']['estimated_votes_low'] + s_response_data['data'][0]['topline_results']['estimated_votes']['estimated_votes_mid']) / 2
        elif expected_turnout == 'Medium':
            estimated_state_votes = s_response_data['data'][0]['topline_results']['estimated_votes']['estimated_votes_mid']
        elif expected_turnout == 'Medium-High':
            estimated_state_votes = (s_response_data['data'][0]['topline_results']['estimated_votes']['estimated_votes_mid'] + s_response_data['data'][0]['topline_results']['estimated_votes']['estimated_votes_high']) / 2
        else:  # 'High'
            estimated_state_votes = s_response_data['data'][0]['topline_results']['estimated_votes']['estimated_votes_high']

        precincts_reportingpf = 'precincts_reporting_percent.txt'
        if total_state_votes_in <= 0.0:
            precincts_reporting_percent = 0.0
        elif estimated_state_votes <= 0.0:
            precincts_reporting_percent = 0.0
        else:
            precincts_reporting_percent = float(total_state_votes_in / estimated_state_votes) * 100

        previous_percent = previous_precincts_reporting_percent.get(setstate, 0.0)
        status_message = "Normal"
        jump = precincts_reporting_percent - previous_percent
        if abs(jump) > max_jump:
            status_message = "Jump Detected! Pausing data value output."
            pause_pushing = True

        previous_precincts_reporting_percent[setstate] = precincts_reporting_percent

        if not pause_pushing:
            with open(state_dir + precincts_reportingpf, 'w') as prpfile:
                if precincts_reporting_percent == 100.0:
                    prpfile.write("100")
                else:
                    prpfile.write(f"{precincts_reporting_percent:.1f}")
        elif pause_pushing:
            print("Pushing paused.")
        return precincts_reporting_percent, previous_precincts_reporting_percent, status_message


def delegate_filter(setstate, state_dir, national_deleg_dir):
    with open('CaucusData/delegate_response_data.json', 'r') as d_response_file:
        d_response_data = json.load(d_response_file)

    state_delegate_republican_data = None
    national_delegate_republican_data = None
    for party_data in d_response_data['delegates']:
        if party_data['name'] == 'Republican':
            national_delegate_republican_data = party_data['national']
            for state_data in party_data['states']:
                if state_data['state_name'] == setstate:
                    state_delegate_republican_data = state_data['candidates']
                    state_delegate_vote_total = state_data['total']
                    break
                else:
                    print(f"State ({setstate}) does not exist in delegate data. Continuing...")
                    return
    state_delegate_republican_ids = list(state_delegate_republican_data.keys())
    national_delegate_republican_ids = list(national_delegate_republican_data.keys())

    for candidate in d_response_data['candidates']:
        candidate_id = str(candidate['cand_id'])
        if candidate_id in national_delegate_republican_ids:
            cand_name = candidate['last_name']
            file_name = f"{cand_name}_national_delegate_votes.txt"
            with open(national_deleg_dir + file_name, 'w') as file:
                file.write(str(national_delegate_republican_data[candidate_id]))
        if candidate_id in state_delegate_republican_ids:
            cand_name = candidate['last_name']
            file_name = f"{cand_name}_{setstate}_delegate_votes.txt"
            with open(state_dir + file_name, 'w') as file:
                file.write(str(state_delegate_republican_data[candidate_id]))
            if state_delegate_vote_total <= 0.0:
                cand_percent = 0.0
            else:
                cand_percent = float(state_delegate_republican_data[candidate_id] / state_delegate_vote_total) * 100
            pfile_name = f"{cand_name}_{setstate}_delegate_percent.txt"
            with open(state_dir + pfile_name, 'w') as file:
                if cand_percent == 100.0:
                    file.write("100")
                else:
                    file.write(f"{cand_percent:.1f}")
