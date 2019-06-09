import datetime
import asyncio
from db import send_stats, return_list_of_users, send_active
from pyro import app

class Stats:
    _UNIQUE_USERS_BY_DAY = []
    _UNIQUE_USERS_BY_WEEK = []
    _UNIQUE_USERS_BY_MONTH = []
    _DAY_COUNTER = 0
    _DOWNLOAD_COUNTER_DAY = 0
    _DOWNLOAD_COUNTER_WEEK = 0
    _DOWNLOAD_COUNTER_MONTH = 0

    def __init__(self):
        pass

    def add_unique(self, user):
        if user not in self._UNIQUE_USERS_BY_DAY:
            self._UNIQUE_USERS_BY_DAY.append(user)
        if user not in self._UNIQUE_USERS_BY_WEEK:
            self._UNIQUE_USERS_BY_DAY.append(user)
        if user not in self._UNIQUE_USERS_BY_MONTH:
            self._UNIQUE_USERS_BY_DAY.append(user)

    def inc_counter(self):
        self._DOWNLOAD_COUNTER_DAY += 1
        self._DOWNLOAD_COUNTER_WEEK += 1
        self._DOWNLOAD_COUNTER_MONTH += 1

    async def check_and_send_stats(self, loop):
        while True:
            now = datetime.datetime.now()
            if int(now.hour) is 0:
                statistics = {
                    'DAY_UNIQUE': self._UNIQUE_USERS_BY_DAY,
                    'DAY_COUNTER': self._DOWNLOAD_COUNTER_DAY,
                    'FOR_DAY': now.day
                }
                send_stats(statistics)
                self._UNIQUE_USERS_BY_DAY.clear()
                self._DOWNLOAD_COUNTER_DAY = 0
            if int(now.day) % 7 is 0:
                statistics = {
                    'WEEK_UNIQUE': self._UNIQUE_USERS_BY_WEEK,
                    'WEEK_COUNTER': self._DOWNLOAD_COUNTER_WEEK
                }
                send_stats(statistics)
                self._UNIQUE_USERS_BY_WEEK.clear()
                self._DOWNLOAD_COUNTER_WEEK = 0
            if int(now.day) is 30:
                statistics = {
                    'MONTH_UNIQUE': self._UNIQUE_USERS_BY_MONTH,
                    'MONTH_COUNTER': self._DOWNLOAD_COUNTER_MONTH,
                    'FOR_MONTH': now.month
                }
                send_stats(statistics)
                self._UNIQUE_USERS_BY_MONTH.clear()
                self._DOWNLOAD_COUNTER_MONTH = 0
            await asyncio.sleep(3600, loop=loop)

    async def check_active_users(self, loop):
            while True:
                counter = 0
                await asyncio.sleep(5, loop=loop)
                self._USERS = return_list_of_users()
                for user in self._USERS:
                    try:
                        await app.get_chat(int(user))
                        counter += 1
                    except:
                        print("User is inactive")
                send_active(counter)        
                await asyncio.sleep(172800, loop=loop)



