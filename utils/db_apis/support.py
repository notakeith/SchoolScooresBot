from pymongo import MongoClient

from data import config

from aiogram import types

import json

client = MongoClient(config.HOST, config.PORT)
storage = client[config.DB_NAME]
datastorage = storage[config.DB_SUPPORT]

async def add_appeal(user_id: int, text:str,message:types.Message):
     datastorage.insert_one({"user_id":user_id,"text":text,"message":dict(message)})