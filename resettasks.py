import requests
import json
import os

def alarm_to_mosi(text):
    bt = "7375001658:AAEnUyWR_LjhsGRdKD6-i5hEuEAwYRcXiTQ"
    ur = f"https://api.telegram.org/bot{bt}"
    url = f"{ur}/sendMessage"
    params = {
        "chat_id": "983588626",
        # "chat_id": "@bandbchannel",
        "text": text
    }
    return send_reply(url, params)

def send_reply(url: str, params: dict):
    response = requests.get(url, data=params)
    return response.content


headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }
# address = "http://emdadmobilerahmati.ir/mosi/Tasks/Tasks.php"

j_file = "data.json"

def getData():
    if os.path.exists(j_file):
        with open(j_file, 'r') as file:
            data = json.load(file)
        
        return data
    else:
        data = {}
        with open(j_file, 'w') as file:
            json.dump(data, file, indent=4)
    return getData()


data = getData()

def reset_tasks(data):
    if len(data) > 0 :
        for index in  range(0,len(data)):
            i = data[str(index)]
            api = i["apikey"]
            username  = i['username']
            try:
                header = {'Authorization': 'Token {token}'.format(token=api),"Content-Type": "application/json"}
                api_url = 'https://www.pythonanywhere.com/api/v0/user/{username}/schedule/'.format(username=username)
                response = requests.get(api_url,headers=header)
                task_data = json.loads(response.content)
            except:
                task_data = []
            try:
                id = task_data[0]['id']
                res_del = requests.delete(api_url+str(id),headers=header)
            except:
                res_del = 204
            
            t_data = {
                "command":i['command'],
                'interval':"daily",
                'minute':i['minute'],
                'hour':i['hour'],
                'enabled':'true',
                'description':"added by task reseter program"
            }
            try:
                res_add = requests.post(api_url,data=json.dumps(t_data), headers=header)
                status = json.loads(res_add.content)['description']

                if res_add.status_code == 201:
                    text = username + " Task Reseted Successfuly :D " 
                    print(text)
                    alarm_to_mosi(text)
            except:
                text = username + "Problem in reset task"
                print(text)
                alarm_to_mosi(text)

def add_task(id,command,hour,minute,username,apikey):
    data = {
        "id":id,
        "command":command,
        "hour":hour,
        "minute":minute,
        "username":username,
        "apikey":apikey
    }

    d = getData()
    index = len(d)
    d[index] = data

    write_data(d)


def delete_task(id):
    data = getData()
    del data[str(id)]
    write_data(data)


def write_data(data):
    with open(j_file, 'w') as file:
        json.dump(data, file, indent=4)

# add_task('1',"/home/mosielite1/config_sender.py",'5',"30","mosielite1","08d7f2a8b0a265af1751edb791cfbd348b7c9a41")
# add_task('2',"/home/mosielite2/config_sender.py",'11',"30","mosielite2","5eccbbcf232b675e83daf10a20b517af10f6ccfa")
# add_task('3',"/home/mosielite3/config_sender.py",'17',"30","mosielite3","b4f98e92c9a507e343d82acebd252cafc0089dad")
# add_task('4',"/home/mosielite4/GitTest/automation_test/git_automation.py",'00',"00","mosielite4","6ce92f22f5af9402696773ce78a3fffe09a04d84")
# add_task('5',"/home/mosielite5/mosi/automation_test/git_automation.py",'15',"45","mosielite5","80d3e1a6d644ada6745d7809bb5558ed8e5c588a")
# add_task('6',"/home/mosielite6/resettasks.py",'20',"30","mosielite6","000c5ba46cf65b696d26004ea90e6a915be8ac1e")
# add_task('7',"/home/mosielite7/bot.py",'17',"30","mosielite7","864fcd012e99efda3b4352e7b1c898157d2030c6")

d = getData()
reset_tasks(d)