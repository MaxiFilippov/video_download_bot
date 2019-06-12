import glob
import os
import asyncio

async def check_for_big_files(loop):
    while True:
        files = glob.glob("/home/max/Telegram/avd/*")
        for _file in files:
            if os.path.getsize(_file) > 1000000000:
                os.remove(_file)
        await asyncio.sleep(600, loop=loop)
