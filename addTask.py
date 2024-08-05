import requests
add_addres  = "https://emdadmobilerahmati.ir/mosi/Tasks/Tasks.php"


task = {
    'id' :"123",
    'command':"/home/mosielite4/GitTest/automation_test/git_automation.py",
    'hour':"00",
    'minuts':"00",
    'username':"mosielite4",
    'apikey':"6ce92f22f5af9402696773ce78a3fffe09a04d84"
}

res = requests.post(add_addres,params=task)

print(res.content)