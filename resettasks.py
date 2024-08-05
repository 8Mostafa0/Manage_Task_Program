import requests
import json
proxy = {
    'http': 'http://78.157.42.101:80',
    'https': 'https://78.157.42.100:443'
}

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }
# address = "http://emdadmobilerahmati.ir/mosi/Tasks/Tasks.php"
address = "https://www.google.com/"

def getData():
    data = requests.get(address,headers=headers)
    print(data.content)
    # data = json.loads(data.content)
    
    # return data

data = getData()

# if len(data) > 0 :
#     for i in data:
#         api = i['apikey']
#         username  = i['username']
#         header = {'Authorization': 'Token {token}'.format(token=api),"Content-Type": "application/json"}
#         api_url = 'https://www.pythonanywhere.com/api/v0/user/{username}/schedule/'.format(username=username)
#         response = requests.get(api_url,headers=header)
#         task_data = json.loads(response.content)
#         id = task_data[0]['id']
#         res_del = requests.delete(api_url+str(id),headers=header)
#         print(res_del.status_code)
#         if res_del.status_code == 204 :
#             t_data = {
#                 "command":i['command'],
#                 'interval':"daily",
#                 'minute':i['minuts'],
#                 'hour':i['hour'],
#                 'enabled':'true',
#                 'description':"added by task reseter program"
#             }
#             res_add = requests.post(api_url,data=json.dumps(t_data), headers=header)
#             status = json.loads(res_add.content)['description']
#             print(status)
