# # python3.7 -m pip install - installation packages
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

# packages import
from config import *
#from download import download_video
import logging
from helpers import language_markup, bot_language
from translations import *
from allocate import Allocate
from advirt import Advirt
from stats import Stats
from db import send_lang, send_username, return_list_of_users
from helpers import regex, re, check_for_big_files
from concurrent.futures import ProcessPoolExecutor, wait
from multiprocessing import cpu_count
logging.basicConfig(level=logging.INFO)
# Class instances init
adv = Advirt()
al = Allocate()
stats = Stats()
# Bot init
bot = Bot(token=API_TOKEN, proxy=PROXY, parse_mode='HTML')

# States init
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'], state="*")
async def show_start(message: types.Message):
    await bot.send_message(message.chat.id, 'Please select language', reply_markup=language_markup)
    state = dp.current_state(user=message.chat.id)
    await state.set_state('main_language')
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, send_username, message.chat.id)


@dp.callback_query_handler(state="main_language")
async def set_main_lang_at_first(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    print("Inside main_language ", callback_query)
    if callback_query.data == 'rus' or callback_query.data == 'eng':
        bot_language[str(callback_query.from_user.id)] = callback_query.data
        await bot.send_message(callback_query.from_user.id, start[bot_language[str(callback_query.from_user.id)]])
    await state.reset_state()
    await callback_query.answer()


@dp.callback_query_handler(state="change_language")
async def set_main_lang(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    print("Inside change_language ", callback_query)
    if callback_query.data == 'rus' or callback_query.data == 'eng':
        bot_language[str(callback_query.from_user.id)] = callback_query.data
        await bot.send_message(callback_query.from_user.id, common_messages[bot_language[str(callback_query.from_user.id)]][2])
    await state.reset_state()
    await callback_query.answer()


@dp.message_handler(commands=['help'], state="*")
async def show_help(message: types.Message):
    if await check_lang(message.chat.id):
        await bot.send_message(message.chat.id, help_message[bot_language[str(message.chat.id)]])
    else:
        await bot.send_message(message.chat.id, 'Please select language', reply_markup=language_markup)
        state = dp.current_state(user=message.chat.id)
        await state.set_state('main_language')


@dp.message_handler(commands=['contact'], state="*")
async def show_settings(message: types.Message):
    if await check_lang(message.chat.id):
        await bot.send_message(message.chat.id, contact[bot_language[str(message.chat.id)]])
    else:
        await bot.send_message(message.chat.id, 'Please select language', reply_markup=language_markup)
        state = dp.current_state(user=message.chat.id)
        await state.set_state('main_language')

@dp.message_handler(commands=['evaluate'], state="*")
async def show_users(message: types.Message):
    if await check_lang(message.chat.id):
        users_amount = await loop.run_in_executor(None, return_list_of_users)
        await bot.send_message(message.chat.id, users[bot_language[str(message.chat.id)]] + str(len(users_amount)))
    else:
        await bot.send_message(message.chat.id, 'Please select language', reply_markup=language_markup)
        state = dp.current_state(user=message.chat.id)
        await state.set_state('main_language')

@dp.message_handler(commands=['language'], state="*")
async def show_language(message: types.Message):
    if await check_lang(message.chat.id):
        await bot.send_message(message.chat.id, common_messages[bot_language[str(message.chat.id)]][3], reply_markup=language_markup)
        state = dp.current_state(user=message.chat.id)
        await state.set_state('main_language')
    else:
        await bot.send_message(message.chat.id, 'Please select language', reply_markup=language_markup)
        state = dp.current_state(user=message.chat.id)
        await state.set_state('change_language')


async def check_lang(user):
    if str(user) in bot_language:
        return True
    return False


@dp.message_handler()
async def get_video(message: types.Message):

    print("Next step", message)
    # В другом месте сделать pool
    # try:
    #     workers = cpu_count()
    # except NotImplementedError:
    #     workers = 1
    # pool = ProcessPoolExecutor(max_workers=workers)
    # await download_video(message.text, message.chat.id)
    
    # !!! Call method allocate server
    if re.match(regex, message.text) is not None and 'reddit' not in message.text and 'porn' not in message.text:
        if await check_lang(message.chat.id):
            if al.check_user_in_single_queue(message.chat.id):
                srv = al.get_server()
                await bot.send_message(message.chat.id, common_messages[bot_language[str(message.chat.id)]][0])
                if srv == "Queue":
                    al.add_to_single_queue(message.chat.id)
                    al.add_to_queue(
                        {'id': message.chat.id, 'url': message.text})
                else:
                    al.add_to_single_queue(message.chat.id)
                    await al.send_to_server(message.chat.id, message.text, srv)

            else:
                await bot.send_message(message.chat.id, common_messages[bot_language[str(message.chat.id)]][1])
        else:
            await bot.send_message(message.chat.id, 'Please select language', reply_markup=language_markup)
            state = dp.current_state(user=message.chat.id)
            await state.set_state('main_language')

    if 'reddit' in message.text:
        raise Exception("Reddit")
        await bot.send_message(message.chat.id, error_messages[bot_language[str(message.chat.id)]][1])


loop = asyncio.get_event_loop()
loop.create_task(send_lang(bot_language, loop))
loop.create_task(stats.check_and_send_stats(loop))
loop.create_task(adv.check_new_session(loop))
loop.create_task(check_for_big_files(loop))
loop.create_task(stats.check_active_users(loop))
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
