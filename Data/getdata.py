import requests
from bs4 import BeautifulSoup

import csv
import sqlite3

def save_text_to_database(text):
    """
    Saves a single text to the 'sentences' table in the database.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect('./Data/database.db')
        c = conn.cursor()

        # Create the 'sentences' table if it doesn't exist
        c.execute("""CREATE TABLE IF NOT EXISTS sentences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL
                )""")

        # Insert the text into the 'sentences' table
        c.execute("INSERT INTO sentences (text) VALUES (?)", (text,))
        conn.commit()

        print(f"Saved text to the database: {text}")
    except sqlite3.Error as e:
        print(f"Error occurred while saving text to the database: {e}")
    finally:
        # Close the database connection
        conn.close()

def get_data_from_database():
    """
    Retrieves all the texts from the 'sentences' table in the database.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Fetch all the texts from the 'sentences' table
        c.execute("SELECT text FROM sentences")
        texts = [row[0] for row in c.fetchall()]

        print(f"Retrieved {len(texts)} texts from the database.")
        return texts
    except sqlite3.Error as e:
        print(f"Error occurred while retrieving data from the database: {e}")
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
url = "https://babezendegi.com/%D8%A8%DB%8C%D9%88%DA%AF%D8%B1%D8%A7%D9%81%DB%8C-%D8%B4%DB%8C%DA%A9/"
response = requests.get(url,headers=headers)
html_content = response.content


soup = BeautifulSoup(html_content, "html.parser")   
div_element = soup.find_all("blockquote",{"class":"aligncenter quote-light"})

for i in div_element:
    p = i.find("p")
    save_text_to_database(p.get_text().strip())
    # print(p.get_text().strip())




