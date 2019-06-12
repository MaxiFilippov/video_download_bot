import youtube_dl
import asyncio
import aiohttp
import os
from config import API_TOKEN
from pyro import send_video, loop, app
from helpers import *
from translations import *
from make_thumb import make_thumbnail, make_ydl_thumbnail


async def download_video(url, username, lang, overload, adv_text, adv_lang):
    try:
        if overload == "busy":
            index = 5 # Index for message about downloading
            index_edit = 6
        else:
            index = 0    
            index_edit = 4
        name = "%(title)s"
        
        ydl = youtube_dl.YoutubeDL(
            {'outtmpl': name, 'progress_hooks': [hook_func]}) # ydl-opts
        with ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None) 
            ydl_thumbnail = info_dict['thumbnail']
        
        if ydl_thumbnail != None:
            thumbnail = await make_ydl_thumbnail(ydl_thumbnail, video_title)
        if ydl_thumbnail == None or thumbnail == None:     
            thumbnail = make_thumbnail(str(video_title))
        
        print(video_title)    
        print('Start downloading')
        
        msg = await app.send_message(int(username), common_messages[lang][index].format(f"<b>{video_title}</b>"), parse_mode="HTML")
        
        with ydl:
            await loop.run_in_executor(None, ydl.download,
                                 [url]
                                 )                        
        await msg.edit(common_messages[lang][index_edit].format(f"<b>{video_title}</b>"), parse_mode="HTML")
        await send_video(username, video_title, lang, msg, thumbnail, adv_text, adv_lang)

    except Exception as e:
        print("Error ", e)
        os.remove(thumbnail)
        if "Unsupported URL" in str(e):
            await app.send_message(int(username), error_messages[lang][1], parse_mode="HTML")
        elif str(e) == "TBF":
            await app.send_message(int(username), error_messages[lang][0], parse_mode="HTML")
        elif "Forbidden" in str(e):
            await app.send_message(int(username), error_messages[lang][3], parse_mode="HTML")   
        else:
            await app.send_message(int(username), error_messages[lang][2], parse_mode="HTML")

def hook_func(file_info):
    max_size = 1000000000  # 1 GB
    if 'total_bytes' in file_info:
        if(file_info['total_bytes'] >= max_size):
            raise Exception("TBF")
