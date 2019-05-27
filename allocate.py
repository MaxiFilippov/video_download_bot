# # Just a models not for production!!!

# import aiohttp
# import asyncio
# from pyro import loop
# from config import SERVER_IP

# # Getting data to the server
# async def get_data():
#     while True:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(SERVER_IP) as resp:
#                 print(resp.status)
#                 print(await resp.text())
#         await asyncio.sleep(0.2, loop=loop)
# # loop = asyncio.get_event_loop()
# # loop.run_until_complete(get_data())

import asyncio
import aiohttp

class Allocate:

    _SERVER_COUNTER = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    _MAX_SERVERS = 3
    _COUNTER = -1
    # Queues with array
    _QUEUE = []
    _QUEUE_COUNTER = 0

    def __init__(self):
        pass

    def add_to_queue(self, info):
        self._QUEUE.append(info)

    def inc_counter(self, server_number):
        print("Incrementing server ", server_number)
        if server_number < self._MAX_SERVERS:
            self._SERVER_COUNTER[server_number] += 1
            print(self._SERVER_COUNTER)

    

    async def send_to_server(self, chat_id, url, server_number):
        if self._QUEUE == []:
            await self.send_data(chat_id, url, server_number)
        
            

    def get_server_for_queue(self):
        for i in range(self._MAX_SERVERS):
            if self._SERVER_COUNTER[i] < 50:
                return self._SERVER_COUNTER[i]

    def get_server(self):
        self._COUNTER += 1
        if self._COUNTER > 2:
            self._COUNTER = 0

        print("Counter is ", self._COUNTER)
        if self._SERVER_COUNTER[self._COUNTER] < 50:  # 50 - max downloads
            self.inc_counter(self._COUNTER)
            return self._COUNTER
        else:
            return "Queue"
            # Make queue
    async def send_data(self, username, url, server_number):
        # from allocate import Allocate
        # al = Allocate()
        print("Sending data to server ", server_number)
        params = {'username': username, 'url': url}
        session = aiohttp.ClientSession()
        
        async with session.post('http://localhost:8020', params=params) as resp: # because post is better # !!!server will change here
            print('Inside post')
            if text == 'dec':
                self.dec_counter(str(text[1]))
        print("Closing session")      
        await session.close()  
         
