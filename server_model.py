import asyncio
import aiohttp


async def send_data(username,url):
    print("Connected")
    return aiohttp.web.Response(text=f"username{username} : {url}")

# app = aiohttp.web.Application()
# app.add_routes([aiohttp.web.get('/', respond_with_data)])
# aiohttp.web.run_app(app, host='localhost', port=8020)