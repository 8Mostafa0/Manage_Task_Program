import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import csv
import sqlite3

def save_link(link,id):
    """
    Saves a single text to the 'sentences' table in the database.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect('./Data/pictures.db')
        c = conn.cursor()

        # Create the 'sentences' table if it doesn't exist
        c.execute("""CREATE TABLE IF NOT EXISTS sentences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    link TEXT NOT NULL
                )""")

        # Insert the text into the 'sentences' table
        c.execute("INSERT INTO sentences (link) VALUES (?)", (link,))
        conn.commit()
        
        print(f"Saved link to the database => ",id)
    except sqlite3.Error as e:
        Alarm(f"Error occurred while saving text to the database: {e}")
    finally:
        # Close the database connection
        conn.close()

def get_data_from_database():
    """
    Retrieves all the texts from the 'sentences' table in the database.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect('pictures.db')
        c = conn.cursor()

        # Fetch all the texts from the 'sentences' table
        c.execute("SELECT text FROM sentences")
        texts = [row[0] for row in c.fetchall()]

        print(f"Retrieved {len(texts)} texts from the database.")
        return texts
    except sqlite3.Error as e:
        Alarm(f"Error occurred while retrieving data from the database: {e}")
        return []
    finally:
        # Close the database connection
        conn.close()


headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }

def get_data():
    id = 0
    for i in range(1,341):
        print("PAGE => ",i)
        url = "https://www.jowhareh.com/search/more?searchQuery=%DA%AF%D9%88%D8%B4%DB%8C&page="+str(i)
        response = requests.get(url,headers=headers)
        html_content = response.content

        # print(html_content)



        soup = BeautifulSoup(html_content, "html.parser")   

        div_element = soup.find_all("img")

        # print(div_element[0].find("p").get_text().strip())
        for i in div_element:
            id+=1

            p = i.get("src")
            
            save_link(p,id)
    print("Program Ended !")
    Alarm("گرفتن عکس ها از سایت https://www.jowhareh.com به اتمام رسید")





def Alarm(text):
    url = "http://emdadmobilerahmati.ir/mosi/API/API.php?username=mosielite&password=mosielite&message="+quote(text)
    response = requests.get(url,headers=headers)

get_data()