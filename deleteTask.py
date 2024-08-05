import requests
import json

add_addres  = "http://emdadmobilerahmati.ir/mosi/Tasks/Tasks.php"


task = {
    'id' :"1",
}

res = requests.delete(add_addres,params=task)

print("\n")

print(json.loads(res.content)['status'] == 'true')