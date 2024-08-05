import requests
import json


address = "https://emdadmobilerahmati.ir/mosi/Tasks/Tasks.php"

def getData():
    data = requests.get(address)

    data = json.loads(data.content)
    
    return data

data = getData()

if len(data) > 0 :
    for i in data:
        api = i['apikey']
        username  = i['username']
        header = {'Authorization': 'Token {token}'.format(token=api),"Content-Type": "application/json"}
        api_url = 'https://www.pythonanywhere.com/api/v0/user/{username}/schedule/'.format(username=username)
        response = requests.get(api_url,headers=header)
        task_data = json.loads(response.content)
        id = task_data[0]['id']
        res_del = requests.delete(api_url+str(id),headers=header)
        print(res_del.status_code)
        if res_del.status_code == 204 :
            t_data = {
                "command":i['command'],
                'interval':"daily",
                'minute':i['minuts'],
                'hour':i['hour'],
                'enabled':'true',
                'description':"added by task reseter program"
            }
            res_add = requests.post(api_url,data=json.dumps(t_data), headers=header)
            status = json.loads(res_add.content)['description']
            print(status)
