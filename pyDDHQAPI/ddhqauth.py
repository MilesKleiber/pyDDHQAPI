import json
import requests


def authenticate(callback=None):
    print("Authenticating...")
    with open('pyDDHQAPI/client_creds.json', 'r') as credentials:
        credentials = json.load(credentials)
    authurl = "https://resultsapi.decisiondeskhq.com/oauth/token"
    authpayload = credentials[0]
    authheaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", authurl, headers=authheaders, data=authpayload)

    if response.status_code == 200:
        response_data = response.json()
        bearer_token_val = response_data['access_token']
        with open('pyDDHQAPI/bearer_token.txt', 'w') as token_file:
            token_file.write(bearer_token_val)
        print("Authenticated. Token set to: " + str(bearer_token_val))
        if callback:
            callback()
    else:
        print("Failed to retrieve token data. Status code:", response.status_code)
