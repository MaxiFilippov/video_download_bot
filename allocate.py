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


class Allocate:

    
    _MAX_SERVERS = 3
    _COUNTER = -1
    # Queues with array
    _QUEUE = []
    def __init__(self):
        pass

    def inc_counter(self, server_number):
        print("Incrementing server ", server_number)
        
            self._SERVER_COUNTER[server_number] += 1

    def dec_counter(self, server_number):
        print("Decrementing server ", server_number)
        if server_number < self._MAX_SERVERS:
            self._SERVER_COUNTER[server_number] -= 1

    def get_server(self):
        self._COUNTER += 1
        if self._COUNTER > 2:
            self._COUNTER = 0
        
        print("Counter is ",self._COUNTER)
        if self._SERVER_COUNTER[self._COUNTER] < 50: 
            inc_counter(self._COUNTER)
            return _COUNTER
        
            # Make queue     
