import asyncio
import aiohttp 
from aiohttp import web
from download import download_video

async def get_data(request):
    _SERVER_NUMBER = 2
    print("Connected")
    try:
        username = request.query['username']
        url = request.query['url']
        lang = request.query['lang']
        overload = request.query['overload']
        adv_text = request.query['adv_text']
        adv_lang = request.query['adv_lang']
        await download_video(url, username, lang, overload, adv_text, adv_lang)
        print("KEEP WORKING")
    except Exception as e:   
        print(e)
    print(f"Username is {username}, url is {url}")    
    return web.Response(text=f"dec:{_SERVER_NUMBER}:{username}")

app = web.Application()
app.add_routes([web.post('/', get_data)])
web.run_app(app, host='0.0.0.0', port=8020)