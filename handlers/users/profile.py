from aiogram import types

from utils.userstates import UserState

from utils.db_apis.subscriptions import get_subscription_info

from loader import dp

from data.config import HOST,PORT,DB_NAME,DB_DATA, END_OF_THE_YEAR
from pymongo import MongoClient
from utils.message_queue import MessageQueue
message_queue = MessageQueue()

client = MongoClient(HOST, PORT)
db = client[DB_NAME]
data_collection = db[DB_DATA]

@dp.message_handler(commands=['profile'], state=UserState.AUTH)
@dp.message_handler(text=['🧑‍🎓 Профиль'], state=UserState.AUTH)
async def command_profile(message: types.Message):
    sub_info = await get_subscription_info(message.from_user.id)
    name = data_collection.find_one({"chat": message.from_user.id})["name"]
    if sub_info is not None:
        if sub_info["DAYS_TO_EXP_INT"] > 0:
            text = f"""\n\n🤩 Подписка: Активна
       Дата истечения подписки: {sub_info["DATE_TO_EXP"]}
       Дней до истечения подписки: {sub_info["DAYS_TO_EXP_INT"]}"""
        else:
            text = f"\n\n😓 Подписка: Неактивна"
    else:
        text = f"\n\n😓 Подписка: Неактивна"
    if sub_info["DATE_TO_EXP"] == END_OF_THE_YEAR:
        await message_queue.add_message(0, chat_id=message.from_user.id, text=f"🧑‍🎓 {name} {text}")
    else:
        await message_queue.add_message(0, chat_id=message.from_user.id, text=f"🧑‍🎓 {name} {text} \n\nВы можете продлить свою подписку. Чтобы узнать больше отправьте команду /pay")
