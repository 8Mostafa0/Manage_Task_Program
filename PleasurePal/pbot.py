
import requests
import json
import os
from urllib.parse import quote
# Replace with your bot token and chat ID

file_path = 'db_state.json'
BOT_TOKEN = '7002468912:AAGgj6eHJXQFFO-aPXx3gCJq1pZm3dYU_io'
CHAT_ID = '983588626'
CH_ID = "@PleasurePal_ch"
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }


def Alarm(text):
    url = "http://emdadmobilerahmati.ir/mosi/API/API.php?username=mosielite&password=mosielite&message="+quote(text)
    response = requests.get(url,headers)

# Telegram API URL
def send_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    # Payload with the message
    payload = {
        'chat_id': CH_ID,
        'text': text,
        'parse_mode' : 'Markdown'
    }
    response = requests.post(url, data=payload)
    print(response.json()['ok'])

def load_data():
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data
    
def save_state(data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def get_last_count():
    js = load_data()
    return js['count']

def set_count():
    data = load_data()
    data['count'] +=5
    save_state(data)

def get_response(link):
    try:
        response = requests.get(link)
        res = response.status_code
        if res == 400 or res == 200:
            return response
        else:
            return get_response(link)
             
    except:
        return get_response(link)
    
def check_message(message_id):
    channel_id = "@PleasurePal_IR"

    # Telegram API endpoint
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessage?chat_id={CHAT_ID}&message_id={message_id}&from_chat_id={channel_id}"

    # Send a GET request to fetch the message data
    response = get_response(url)

    # Check if the request was successful
    print(response.status_code)
    if response.status_code == 200:
        message_data = response.json()
        return message_data
    else:
        return False


def get_links(index):
    messages = []
    for i in range(index,index+20):
        print(i)
        if len(messages) < 6:
            mid = check_message(i)
            if mid != False:
                messages.append(i)
        else:
            break
    return messages
    
def save_state_to_json(state, json_file):
    try:
        with open(json_file, 'w') as f:
            json.dump(state, f, indent=4)

    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

def generate_state_json(json_file):
    state = {
        'count':0
    }
    save_state_to_json(state,json_file)

def main():
    if os.path.exists(file_path):
        last_count = get_last_count()
        links = get_links(last_count)
        if( len(links) >0):
            text = "بهترین بهترینها باز هم از  🍑  PleasurePal@ 🍑 \n\n"
            text += "[مشاهده فیلم های جدید😻](https://t.me/PleasurePal_bot?start=vid-"+str(links[0])+"-"+str(links[-1])+")\n"

            text+= "\n\n 💪 با ما همیشه عقاب تک پر بمانید🦅 "
            send_message(text)
        set_count()
        Alarm("محتوای جدید به کانال PleasurePal@ اضافه شد")
    else:
        generate_state_json(file_path)
        main()

# main()
main()