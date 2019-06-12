import asyncio
import os

from pyrogram import Client
from config import API_TOKEN
from translations import error_messages
from helpers import check_for_big_files
app = Client(
    "Bot",
    bot_token=API_TOKEN,
    api_id=850212,
    api_hash="a7e066cc5644d5c51dac73a1b028e518"
)


async def send_video(username, video_title, lang, msg, thumbnail, adv_text, adv_lang):
    try:
        path = "./" + video_title
        print("Sending video", path)
        await app.send_video(int(username), path, caption=f"<b>{video_title}</b>", parse_mode="HTML", thumb=thumbnail)
        await app.delete_messages(int(username), msg["message_id"])
        print("Video has been saved")
        os.remove(path)
        os.remove(thumbnail)
        print(adv_text != "Empty")
        if adv_text != "Empty" and ((adv_lang == lang) or (adv_lang == all)):
            await app.send_message(int(username), adv_text, parse_mode="HTML") 
    except Exception as e:
        if 'The file id' in str(e):
            await app.send_message(int(username), error_messages[lang][1], parse_mode="HTML")   
        print("Sending video error ", e)
        os.remove(path)
        os.remove(thumbnail)
loop = asyncio.get_event_loop()
loop.create_task(app.start())
loop.create_task(check_for_big_files(loop))
