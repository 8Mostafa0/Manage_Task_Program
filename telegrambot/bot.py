import requests
import json
import os
import sqlite3

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
BOT_TOKEN = "7282153814:AAH24EVXCtNINdTUsQbsiHc62j-lxfjt_y4"
URI = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(text):
    url = f"{URI}/sendMessage"
    params = {
        "chat_id": "983588626",
        # "chat_id": "@bandbchannel",
        "text": text
    }
    return send_reply(url, params)

def send_reply(url: str, params: dict):
    response = requests.get(url, data=params)
    return response.content


def send_pic_text(pic_link,text):
    url = f"{URI}/sendPhoto"
    params = {
        "chat_id": "983588626",
        # "chat_id": "@bandbchannel",
        "photo" : pic_link,
        "caption": text
    }
    return send_reply(url, params)


def get_p(id):
    conn = sqlite3.connect('pictures.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sentences WHERE id = ?", (id,))
    user = c.fetchone()
    conn.commit()
    conn.close()

    if user:
        return user[1]
    else:
        return None
    
def get_t(id):
    conn = sqlite3.connect('sentences.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sentences WHERE id = ?", (id,))
    user = c.fetchone()
    conn.commit()
    conn.close()

    if user:
        return user[1]
    else:
        return None


def get_pic_count():
    conn = sqlite3.connect('pictures.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sentences")
    count = c.fetchone()[0]
    # Close the connection
    conn.commit()
    conn.close()
    return count

def get_text_count():
    conn = sqlite3.connect('sentences.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sentences")
    count = c.fetchone()[0]
    # Close the connection
    conn.commit()
    conn.close()
    return count

state_f = "state.json"
def start():
    if os.path.exists(state_f):
        with open(state_f, "r") as file:
            data = json.load(file)
        t_id = data['text_id']
        p_id = data['pic_id']
        
        t_id += 1
        p_id += 1
        
        if t_id >= (data['text_count'] - 100 ) and p_id >= (data['pic_count'] - 100):
            alarm_to_mosi("اطلاعات ربات B & B به اندازه 100 روز دیگر موجود است لطفا اطلاعات جدید اضافه کنید")

        if t_id <= data['text_count'] and p_id <= data['pic_count']:
            print("Sending Data Count =>",p_id)
            p=get_p(p_id)
            t=get_t(t_id)
            
            data['text_id'] = t_id
            data['pic_id'] = p_id

            write_data(data)
            
            send_pic_text(p,t)
            text = "اطلاعات مرتبه :"
            text += str(p_id)
            text += "با موفقیت از طریق ربات  B & B به کانال ارسال شد"
            alarm_to_mosi(text)
        else:
            alarm_to_mosi("اطلاعات به اندازه کافی در دیتابیس ربات  B & B وجود ندارد لطفا اطلاعات جدید را وارد کنید")
            
    else:
        data = {
            "text_count" : 0,
            "text_id" : 0,
            "pic_count" : 0,
            "pic_id" : 0
        }
        data['text_count'] = get_text_count()
        data['pic_count'] = get_pic_count()
        write_data(data)
        start()

def write_data(data):
    with open(state_f, "w") as file:
        json.dump(data, file)



start()



