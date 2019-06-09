import asyncio
import os

from pyrogram import Client
from config import API_TOKEN
from translations import error_messages

app = Client(
    "News Bot",
    bot_token=API_TOKEN,
    api_id=850212,
    api_hash="a7e066cc5644d5c51dac73a1b028e518"
)


async def send_video(username, path, lang):
    try:
        print("Sending video", path)
        await app.send_video(int(username), path)
        print("Video has been saved")
        os.remove(path)
    except Exception as e:
        if 'The file id' in str(e):
            app.send_message(int(username), error_messages[lang][1])
        print("Sending video error ", e)
loop = asyncio.get_event_loop()
loop.create_task(app.start())
# 850212
# a7e066cc5644d5c51dac73a1b028e518