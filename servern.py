import asyncio
import aiohttp 
from download import download_video

async def get_data():
    _SERVER_NUMBER = 'N'
    print("Connected")
    try:
        username = request.query['username']

        await download_video(url, username)
        print("KEEP WORKING")
    except Exception as e:   
        print(e)
    print(f"Username is {username}, url is {url}")    
    

app = web.Application()
app.add_routes([web.post('/', get_data)])
web.run_app(app, host='localhost', port=8020)