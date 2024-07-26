from aiogram import types

from data.text import message_settings
from loader import dp
from utils.userstates import UserState
from data.config import HOST, PORT, DB_NAME, DB_DATA
from pymongo import MongoClient
from utils.db_apis.settings import get_setting, switch_settings
from utils.auth import unauth

client = MongoClient(HOST, PORT)
db = client[DB_NAME]
data_collection = db[DB_DATA]

from utils.message_queue import MessageQueue
message_queue = MessageQueue()


@dp.message_handler(commands=['settings'], state=UserState.AUTH)
@dp.message_handler(text=['⚙ Настройки'], state=UserState.AUTH)
async def command_settings(message: types.Message):
    name = data_collection.find_one({"chat": message.from_user.id})["name"]
    notification_state = await get_setting(message.from_user.id, "notification")
    await message_queue.add_message(0, chat_id=message.from_user.id, text=message_settings(name,not notification_state),reply_markup=f"await get_inline_btn_quit({notification_state})")

@dp.callback_query_handler(text="notificationOFF",state=UserState.AUTH)
async def f_notificationOFF(call: types.CallbackQuery):
    await switch_settings(call.from_user.id,"notification")
    name = data_collection.find_one({"chat": call.from_user.id})["name"]
    await message_queue.add_message(0, chat_id=call.from_user.id, edit=True, message_id=call.message.message_id, text=message_settings(name,False), reply_markup="await get_inline_btn_quit(True)")

@dp.callback_query_handler(text="notificationON",state=UserState.AUTH)
async def f_notificationON(call: types.CallbackQuery):
    await switch_settings(call.from_user.id,"notification")
    name = data_collection.find_one({"chat": call.from_user.id})["name"]
    await message_queue.add_message(0, chat_id=call.from_user.id, edit=True, message_id=call.message.message_id, text=message_settings(name,True), reply_markup="await get_inline_btn_quit(False)")



@dp.callback_query_handler(text="quit",state=UserState.AUTH)
async def f_quit(call: types.CallbackQuery):
    await call.answer(await unauth(call.from_user.id,force=False))
