import requests
add_addres  = "https://emdadmobilerahmati.ir/mosi/Tasks/Tasks.php"


task = {
    'id' :"4",
}

res = requests.delete(add_addres,params=task)

print(res.content)