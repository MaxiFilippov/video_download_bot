# Just a models not for production!!!

import aiohttp
import asyncio
from pyro import loop
from config import SERVER_IP

# Getting data to the server
async def get_data():
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(SERVER_IP) as resp:
                print(resp.status)
                print(await resp.text())
        await asyncio.sleep(0.2, loop=loop)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(get_data())
