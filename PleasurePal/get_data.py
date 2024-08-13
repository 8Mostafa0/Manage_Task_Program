# !pip install telethon
# !pip install cryptg
# !pip install pillow
# !pip install aiohttp
# !pip install hachoir

api_id = "22879721"
api_hash = "2843e297db2631ad42b62937e44cf07e"
phone = "+989020407808"

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }

link = 'https://xhamster.com/categories'

import requests
import json
from bs4 import BeautifulSoup
from telethon.tl.types import InputFile
from telethon import TelegramClient
import os
import sqlite3
from io import BytesIO
from urllib.parse import quote
import asyncio

client = TelegramClient('anon', api_id, api_hash)

file_path="state.json"
def load_data():
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

def update_count(c):
    with open('state.json', 'r') as file:
        data = json.load(file)

    data['count'] = c
    # 3. Save the updated JSON data back to the file
    with open('state.json', 'w') as file:
        json.dump(data, file, indent=4)

def update_tag(c):
    with open('state.json', 'r') as file:
        data = json.load(file)

    data['tag'] = c
    # 3. Save the updated JSON data back to the file
    with open('state.json', 'w') as file:
        json.dump(data, file, indent=4)

def Alarm(text):
    url = "http://emdadmobilerahmati.ir/mosi/API/API.php?username=mosielite&password=mosielite&message="+quote(text)
    response = requests.get(url,headers=headers)

def get_response(link):
    try:
        response = requests.get(link)
        res = response.status_code
        if res != 200:
            return get_response(link)
        else:
            soup = BeautifulSoup(response.content, 'html.parser')

            return soup.prettify()
    except:
        return get_response(link)
    
async def send_video(video_url):
    # Fetch the video from the URL and load it into memory
    Alarm("Start Download")
    response = requests.get(video_url, stream=True)

    if response.status_code == 200:
        video_stream = BytesIO(response.content)
        video_stream.name = "video.mp4"  # You must set the name attribute for the video stream

        # Send the video
        await client.send_file("@PleasurePal_IR", video_stream)
    Alarm("End Download")


def get_tags():
    conn = sqlite3.connect('./category.db')
    try:
        # Connect to the database
        c = conn.cursor()

        # Fetch all the texts from the 'sentences' table
        c.execute("SELECT tag,count FROM category")
        data=c.fetchall()
        texts = [row[0] for row in data]
        counts = [row[1] for row in data]

        return counts,texts
    except sqlite3.Error as e:
        Alarm(f"Error occurred while retrieving data from the database: {e}")
        return []
    finally:
        # Close the database connection
        conn.close()

async def start():
    await client.start(bot_token="7002468912:AAGgj6eHJXQFFO-aPXx3gCJq1pZm3dYU_io")
    me = await client.get_me()

async def main():
    await client.start()
    me = await client.get_me()

    counts, tags = get_tags()
    state = load_data()
    tag = [item.split("/")[-1] for item in tags]
    last_index = tag.index(state['tag'])
    del tag[:last_index]
    movie_count = 0
    page_count = 0
    tag_count = 0
    page_count = int(state['count'])
    page = state['count']
    tags_count = len(tag)

    # Progress bar for tags
    for i, v in enumerate(tag):
        update_tag(v)
        tag_count += 1
        Alarm("Getting Tag : " + str(v) + " From Xhamester 😎")
        l = tags[i]
        count = counts[i]

        # Progress bar for pages within each tag
        for d in range(int(page), count):
            page_count += 1
            update_count(d)
            Alarm("Getting Tag : " + str(v) + ", Page " + str(d) +"/"+str(count)+ " From Xhamester 😬")
            link = l + "/" + str(d)
            data = get_response(link)
            soup = BeautifulSoup(data, "html.parser")
            div = soup.find_all("a", class_="video-thumb__image-container role-pop thumb-image-container")
            tb_name = l.split("/")[-1]

            # Progress bar for movies within each page
            for a in div:
                movie_count += 1
                content = get_response(a['href'])
                soup = BeautifulSoup(content, "html.parser")
                vid = soup.find("video")
                await send_video(vid['src'])


await start()
await main()