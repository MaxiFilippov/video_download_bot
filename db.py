import pymongo
import asyncio
from config import CLUSTER_TOKEN


def get_lang():
    print('Gettins langs')
    dict_of_langs = {

    }
    myclient = pymongo.MongoClient(CLUSTER_TOKEN)
    mydb = myclient["VideoDownloadBot"]
    mycol = mydb["Data"]
    for x in mycol.find({'Languages': 'dict_of_langs'}):
        try:
            dict_of_langs = x['languages']
        except:
            dict_of_langs = {

            }
    return dict_of_langs


async def send_lang(langs, loop):
    while True:
        print('Sending to DB', langs)
        myclient = pymongo.MongoClient(
            CLUSTER_TOKEN)
        mydb = myclient["VideoDownloadBot"]
        mycol = mydb["Data"]
        mycol.update_one({'Languages': 'dict_of_langs'}, {
            "$set": {
                'languages': langs
            }
        })
        await asyncio.sleep(10800, loop=loop)


def get_user(username):
    myclient = pymongo.MongoClient(
        CLUSTER_TOKEN)
    mydb = myclient["VideoDownloadBot"]
    mycol = mydb['Chat_IDS']
    for x in mycol.find({"username": username}):
        if username == x['username']:
            print('Returning false')
            return False
    return True


def send_username(username):
    myclient = pymongo.MongoClient(
        CLUSTER_TOKEN)
    mydb = myclient["VideoDownloadBot"]
    mycol = mydb["Chat_IDS"]
    post = {
        'username': username
    }
    if get_user(username):
        mycol.insert_one(post)


def send_stats(stats):
    myclient = pymongo.MongoClient(
        CLUSTER_TOKEN)
    mydb = myclient["VideoDownloadBot"]
    mycol = mydb["Stats"]
    post = {
        'Statistics': stats
    }
    mycol.insert_one(post)


def send_active(amount_of_users):
    myclient = pymongo.MongoClient(
        CLUSTER_TOKEN)
    mydb = myclient["VideoDownloadBot"]
    mycol = mydb["Stats"]
    post = {
        'Active Users': amount_of_users
    }
    mycol.insert_one(post)


def get_adv():
    myclient = pymongo.MongoClient(
        CLUSTER_TOKEN)
    adv = {}
    mydb = myclient["VideoDownloadBot"]
    mycol = mydb["Advirt"]
    for x in mycol.find({}):
        adv = x
    return adv


def reset_session(count_of_shows):
    myclient = pymongo.MongoClient(
        CLUSTER_TOKEN)
    mydb = myclient["VideoDownloadBot"]
    mycol = mydb["Advirt"]

    print('User exists')
    mycol.update_one({'session': 'active'}, {
        "$set": {
            'session': 'inactive',
            'text': '',
            'max_shows': '0',
            'count_of_users': str(count_of_shows)
        }
    })


def return_list_of_users():
    users = []
    myclient = pymongo.MongoClient(
        CLUSTER_TOKEN)
    mydb = myclient["VideoDownloadBot"]
    mycol = mydb["Chat_IDS"]
    for x in mycol.find({}):
        users.append(x['username'])
    return users


def get_info_about_servers():
    print('Gettins Max_Servers')
    dict_of_servers = {

    }
    myclient = pymongo.MongoClient(
        CLUSTER_TOKEN)
    mydb = myclient["VideoDownloadBot"]
    mycol = mydb["Manage"]
    for x in mycol.find({'Servers': 'dict_of_servers'}):
        try:
            dict_of_servers = x['servers']
        except:
            dict_of_servers = {

            }
    return dict_of_servers
