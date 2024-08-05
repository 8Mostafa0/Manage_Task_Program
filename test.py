import requests
import json

from datetime import datetime, timedelta

username = 'mosielite4'
API_TOKEN = '6ce92f22f5af9402696773ce78a3fffe09a04d84'

response = requests.get(
    'https://www.pythonanywhere.com/api/v0/user/{username}/schedule/'.format(
        username=username
    ),
    headers={'Authorization': 'Token {token}'.format(token=API_TOKEN)}
)


if response.status_code == 200:
    resp = json.loads(response.content)
    print(resp)
    # TASK_ID = resp[0]['id']
    # print("Task id =>", TASK_ID)

    NEW_EXPIRY_DATE = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')

    # Construct the API request URL
    api_url = f"https://www.pythonanywhere.com/api/v0/user/{username}/schedule/"

    # Prepare the request payload
    payload = {
        "command" :"/home/mosielite4/GitTest/automation_test/git_automation.py",
        "interval":"daily",
        "minute" :"00",
        "hour":"00",
        "enabled":"true",
        "description" :"nonenen"
    }

    # Set the request headers
    headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Send the API request to update the task expiry date
    response = requests.post(api_url,data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print(f"Task  expiry date updated to {response.content}")
    else:
        print(f"Error updating task : {response.status_code} - {response.content} ")


else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
     