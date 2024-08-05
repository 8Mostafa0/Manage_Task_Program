import requests
import json

add_addres  = "http://emdadmobilerahmati.ir/mosi/Tasks/Tasks.php"


task = {
    'id' :"1",
    'command':"/home/mosielite6/resettasks.py",
    'hour':"20",
    'minuts':"30",
    'username':"mosielite6",
    'apikey':"000c5ba46cf65b696d26004ea90e6a915be8ac1e"
}

res = requests.post(add_addres,params=task)

print("\n")

print(json.loads(res.content)['status'] == 'true')