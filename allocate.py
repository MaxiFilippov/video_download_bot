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
from helpers import bot_language
from stats import Stats
from db import get_info_about_servers
stats = Stats()


class Allocate:

    _SERVER_COUNTER = [0, 0, 0, 0]
    _SERVERS = get_info_about_servers()
    _COUNTER = -1
    # Queues with array
    _QUEUE = []
    _QUEUE_COUNTER = 0
    _SINGLE_USER_QUEUE = []

    def __init__(self):
        pass

    def add_to_queue(self, info):
        print("Adding to queue")
        self._QUEUE.append(info)

    def add_to_single_queue(self, chat_id):
        self._SINGLE_USER_QUEUE.append(chat_id)

    def remove_from_single_queue(self, chat_id):
        self._SINGLE_USER_QUEUE.remove(chat_id)

    def check_user_in_single_queue(self, chat_id):
        if chat_id in self._SINGLE_USER_QUEUE:
            print("User in the queue")
            return False
        print("User is not in queue")
        return True

    def inc_counter(self, server_number):
        print("Incrementing server ", server_number)
        if server_number < int(self._SERVERS['max_servers']):
            self._SERVER_COUNTER[server_number] += 1
            print(self._SERVER_COUNTER)

    async def dec_counter(self, server_number):
        print("Decrementing server ", server_number)
        if int(server_number) < int(self._SERVERS['max_servers']):
            self._SERVER_COUNTER[server_number] -= 1
            if self._QUEUE != []:
                await self.send_to_server(None, None, -1)

    async def send_to_server(self, chat_id, url, server_number):
        if self._QUEUE == [] and chat_id != None and server_number != -1:
            print("Queue is empty")
            await self.send_data(chat_id, url, server_number)
        else:
            print("Queue is not empty")
            print("Queue before removing", self._QUEUE, " ", url)
            user_id = self._QUEUE[0]['id']
            url = self._QUEUE[0]['url']
            self._QUEUE.pop(0)
            await self.send_data(user_id, url, self.get_server())
            print("Queue after removing ", self._QUEUE)
        

    # def get_server_for_queue(self):
    #     for i in range(int(self._SERVERS['max_servers'])):
    #         if self._SERVER_COUNTER[i] < 41:  # 40 - max downloads at a time
    #             return i

    def get_server(self):
        self._COUNTER += 1
        if self._COUNTER >= int(self._SERVERS['max_servers']):
            self._COUNTER = 0

        print("Counter is ", self._COUNTER)
        # 40 - max downloads at a time
        if self._SERVER_COUNTER[self._COUNTER] < 41:
            self.inc_counter(self._COUNTER)
            return self._COUNTER
        else:
            return "Queue"

    async def send_data(self, username, url, server_number):
        # from allocate import Allocate
        # al = Allocate()
        print("Server number is ", server_number)
        try:
            print("Sending data to server ", server_number)
            print("Username is ", username, 'Url is ', url)
            # Change lang after tests bot_language[str(username)]
            params = {'username': username, 'url': url, 'lang': bot_language[str(username)]}
            timeout = aiohttp.ClientTimeout(total=1800)
            session = aiohttp.ClientSession()

            # because post is better # !!!server will change here
            stats.add_unique(int(username))
            stats.inc_counter()
            # Instead of 1 must be str(server_number)
            async with session.post(self._SERVERS[str(int(server_number)+1)], params=params, timeout=timeout) as resp:
                print('Inside post')
                text = await resp.text()
                print("Text before splitting ", text)
                text = text.split(":")
                print(text, text[1]) 
                if text[0] == 'dec':
                    await self.dec_counter(int(text[1]))
                    self.remove_from_single_queue(int(text[2])) # Uncomment after tests
            print("Closing session")
            await session.close()
        except Exception as e:
            self.remove_from_single_queue(username) # Uncomment after tests
            print("Error in send_data ", e)
           
