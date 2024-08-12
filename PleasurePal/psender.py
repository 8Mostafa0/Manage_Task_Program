api_id = "22879721"
api_hash = "2843e297db2631ad42b62937e44cf07e"
phone = "+989020407808"
import requests
from telethon import TelegramClient
import os
client = TelegramClient('anon', api_id, api_hash)
async def send_file_from_url(url, chat_id):
    # Step 1: Download the file
    print("Start Download")
    file_name = url.split('/')[-1]
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)
    
    print("End Download")
    # Step 2: Send the file using Telethon
    await client.send_file(chat_id, file_name)

    # Optionally, delete the file after sending
    os.remove(file_name)
async def main():
    # Getting information about yourself
    me = await client.get_me()
    username = me.username
    print(username)
    print(me.phone)

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    # print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:

    # You can print all the dialogs/conversations that you are part of:
    # async for dialog in client.iter_dialogs():
    #     print(dialog.name, 'has ID', dialog.id)

    # You can send messages to yourself...
    message = await client.send_message('+989399497154', 'Hello, Sami this message sended from python script :D!')
    # ...to some chat ID
    # ...or even to any username
    # await client.send_message('+989020407808', 'Testing Telethon!')

    # You can, of course, use markdown in your messages:
    # message = await client.send_message(
    #     'me',
    #     'This message has **bold**, `code`, __italics__ and '
    #     'a [nice website](https://example.com)!',
    #     link_preview=False
    # )

    # Sending a message returns the sent message object, which you can use
    # print(message)

    # You can reply to messages directly if you have a message object
    await message.reply('Cool!')
    await send_file_from_url('https://video7.xhcdn.com/key=7xtaih6T9JKg1wD8oSAY4g,end=1723410000,limit=3/data=172.86.108.84-dvp/speed=0/012/697/719/720p.h264.mp4','@mosix_ph')
    # Or send files, songs, documents, albums...
    # await client.send_file('@mosix_ph', 'https://video7.xhcdn.com/key=7xtaih6T9JKg1wD8oSAY4g,end=1723410000,limit=3/data=172.86.108.84-dvp/speed=0/012/697/719/720p.h264.mp4',caption="This is a test Cation")

    # You can print the message history of any chat:
    # async for message in client.iter_messages('+989399497154'):
    #     print(message.id, message.text)

        # You can download media from messages, too!
        # The method will return the path where the file was saved.
        # if message.photo:
        #     path = await message.download_media()
        #     print('File saved to', path)  # printed after download is done

with client:
    client.loop.run_until_complete(main())