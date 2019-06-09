import random
import string
from db import get_lang
import re
import glob
import os
import asyncio
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def random_string(stringLength):
    """Generate a random string video name """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


list_of_errors = ["TBF"]

bot_language = get_lang()

rus = InlineKeyboardButton('Русский🇷🇺', callback_data='rus')
eng = InlineKeyboardButton('English🇺🇸', callback_data='eng')

language_markup = InlineKeyboardMarkup().add(eng, rus)

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


async def check_for_big_files(loop):
    while True:
        files = glob.glob("/home/max/Telegram/avd/*")
        for _file in files:
            if os.path.getsize(_file) > 1000000000:
                os.remove(_file)
        await asyncio.sleep(600, loop=loop)