import asyncio
from db import get_adv, reset_session, return_list_of_users
from pyro import app
from helpers import bot_language


class Advirt:
    _COUNT_OF_SHOWS = 0
    _TEXT = ''
    _SESSION = 'inactive'
    _USERS = []
    _LANGUAGE = ''
    _LIST_OF_MESSAGES = []

    def __init__(self):
        pass

    def inc_count(self):
        print("Incrementing")
        self._COUNT_OF_SHOWS += 1

    def reset_count(self):
        print('Reseting')
        reset_session(self._COUNT_OF_SHOWS)
        self._COUNT_OF_SHOWS = 0
        self._SESSION = 'inactive'
        self._USERS.clear()

    async def check_new_session(self, loop):
        while True:
            adv = get_adv()
            if adv['session'] == 'active' and self._SESSION != 'active':
                print("Session is active")
                self._TEXT = adv['text']
                self._SESSION = 'active'
                self._LANGUAGE = adv['language']
                adv = Advirt()
                loop.run_until_complete(adv.send_advirt(loop))
            if adv['reset'] == 'reset':
                await self.reset_count()
                await self.delete_all_advirt(loop)
            await asyncio.sleep(3600, loop=loop)

    async def delete_all_advirt(self, loop):
        await asyncio.sleep(1, loop=loop)
        msgs = list(reversed(self._LIST_OF_MESSAGES))
        print(msgs)
        for i in range(len(self._LIST_OF_MESSAGES)):
            try:
                await app.delete_messages(int(self._USERS[i]), msgs[i]["message_id"])
            except Exception as e:
                print(e)

    async def send_advirt(self, loop):
        await asyncio.sleep(3, loop=loop)
        self._USERS = return_list_of_users()
        print("Sending message")
        for user in self._USERS:
            if bot_language[str(user)] is self._LANGUAGE or 'all':
                try:
                    msg = await app.send_message(int(user), self._TEXT)
                    self._LIST_OF_MESSAGES.append(msg)
                except:
                    print("Inactive user")
