import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json
import sqlite3
import asyncio
api_id = "22879721"
api_hash = "2843e297db2631ad42b62937e44cf07e"
phone = "+989020407808"
import requests
from telethon import TelegramClient
import os

async def send_file_from_url(url, chat_id):
    # Step 1: Download the file
    Alarm("Start Download")
    file_name = url.split('/')[-1]
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)
    
    Alarm("End Download")
    # Step 2: Send the file using Telethon
    await client.send_file(chat_id, file_name)

    # Optionally, delete the file after sending
    os.remove(file_name)


def save_category(tag,count):

    conn = sqlite3.connect('./category.db')
    try:
        # Connect to the database
        c = conn.cursor()

        # Create the 'sentences' table if it doesn't exist
        c.execute("""CREATE TABLE IF NOT EXISTS category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag TEXT NOT NULL,
                    count INTIGER NOT NULL,
                    curser INTIGER NOT NULL
                )""")

        # Insert the text into the 'sentences' table
        c.execute("INSERT INTO category (tag,count,curser) VALUES (?,?,?)", (tag,count,0,))
        conn.commit()
        
    except sqlite3.Error as e:
        Alarm(f"Error occurred while saving text to the database: {e}")
    finally:
        # Close the database connection
        conn.close()


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


# def save_link(link,tags):
#     """
#     Saves a single text to the 'links' table in the database.
#     """
#     conn = sqlite3.connect('./porn.db')
#     try:
#         # Connect to the database
#         c = conn.cursor()

#         # Create the 'sentences' table if it doesn't exist
#         c.execute("""CREATE TABLE IF NOT EXISTS data (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     link TEXT NOT NULL,tags TEXT NOT NULL
#                 )""")

#         # Insert the text into the 'sentences' table
#         c.execute("INSERT INTO data (link,tags) VALUES (?,?)", (link,tags,))
#         conn.commit()
        
#     except sqlite3.Error as e:
#         Alarm(f"Error occurred while saving text to the database: {e}")
#     finally:
#         # Close the database connection
#         conn.close()

def get_all_links():
    """
    Retrieves all the texts from the 'links' table in the database.
    """
    conn = sqlite3.connect('./porn.db')
    try:
        # Connect to the database
        c = conn.cursor()

        # Fetch all the texts from the 'sentences' table
        c.execute("SELECT links FROM data")
        texts = [row[0] for row in c.fetchall()]

        print(f"Retrieved {len(texts)} links from the database.")
        return texts
    except sqlite3.Error as e:
        Alarm(f"Error occurred while retrieving data from the database: aa{e}")
        return []
    finally:
        # Close the database connection
        conn.close()




def save_link(tbname,link):

    conn = sqlite3.connect('/content/drive/MyDrive/main_db.db')
    try:
        # Connect to the database
        c = conn.cursor()

        # Create the 'sentences' table if it doesn't exist
        c.execute(f"""CREATE TABLE IF NOT EXISTS {tbname} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    link TEXT NOT NULL
                )""")

        # Insert the text into the 'sentences' table
        link = str(link)
        c.execute(f"INSERT INTO {tbname} (link) VALUES (?)", (link,))
        conn.commit()
        
    except sqlite3.Error as e:
        Alarm(f"Error occurred while saving text to the database: {e}")
    finally:
        # Close the database connection
        conn.close()








headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }

link = 'https://xhamster.com/categories'


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


def get_server_tags():
    id = 0

    html_content = get_response(link)

    
    soup = BeautifulSoup(html_content, "html.parser")   
    div = soup.find_all("section")
    for b in div:

        div_element = b.find_all("a",class_="item-f658a thumbItem-f658a")
        

        for i in div_element:
            id +=1
            p = i['href']
            count = get_tag_count(p)
            print("getted ",id," tagsand count : ",count," from server",end='\r', flush=True)
            
            save_category(p,count)

def get_tag_count(link):

    html_content = get_response(link)

    
    soup = BeautifulSoup(html_content, "html.parser")
    
    div = soup.find_all("a",class_="page-button-link")

    last_link = div[-1]['href']
    count = last_link.split("/")[-1]
    return count
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
loop = asyncio.get_event_loop()
async def get_data():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()
    me = await client.get_me()
    username = me.username
    print(username)
    print(me.phone)
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
                client.loop.run_until_complete(await send_file_from_url(vid['src'],"@PleasurePal_IR"))

                # Use tqdm.write to log the current progress
                # tqdm.write(f"Processed Movie: {movie_count}, Page: {page_count}, Tag: {tag_count}")

    print("Program Ended !")
    Alarm("گرفتن اطلاعات از سایت xhamester به پایان رسید 😄")

loop.run_until_complete(get_data())