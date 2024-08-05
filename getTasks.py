import requests
import json

add_addres  = "https://emdadmobilerahmati.ir/mosi/Tasks/Tasks.php"

res = requests.get(add_addres)

print("\n")

print(json.loads(res.content))