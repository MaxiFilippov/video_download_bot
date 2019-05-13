# # python3.7 -m pip install - installation packages
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

# packages import
from config import *
from download import download_video
import logging


from concurrent.futures import ProcessPoolExecutor, wait
from multiprocessing import cpu_count
logging.basicConfig(level=logging.INFO)
# Bot init
bot = Bot(token=API_TOKEN, proxy=PROXY, parse_mode='HTML')

# States init
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def show_start(message: types.Message):
    await bot.send_message(message.chat.id, 'Welcome to help')


@dp.message_handler(commands=['help'])
async def show_help(message: types.Message):
    await bot.send_message(message.chat.id, 'Welcome to help')


@dp.message_handler(commands=['settings'])
async def show_settings(message: types.Message):
    await bot.send_message(message.chat.id, 'Welcome to settings')


@dp.message_handler(commands=['language'])
async def show_language(message: types.Message):
    await bot.send_message(message.chat.id, 'Welcome to languge')


@dp.message_handler()
async def get_video(message: types.Message):
    await bot.send_message(message.chat.id, "Загрузка началась")
    print("Next step")
    # В другом месте сделать pool
    # try:
    #     workers = cpu_count()
    # except NotImplementedError:
    #     workers = 1
    # pool = ProcessPoolExecutor(max_workers=workers)
    await download_video(message.text, message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
