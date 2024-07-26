import json

from aiogram.dispatcher import FSMContext
from barsdiary.aio import APIError, DiaryApi
from pymongo import MongoClient

from data.config import HOST, PORT, DB_NAME, DB_STUDENTS, DB_DATA
from data.text import message_auth_success, message_exclusive, message_unauth, message_unauth_force
from loader import dp
from utils.db_apis.subscriptions import set_subscription_info
from utils.db_apis.settings import deleteLoginPass,saveLoginPass
from utils.keyboards import inline_kb_auth
from utils.userstates import UserState
from utils.db_apis.referal import addReferal

from utils.message_queue import MessageQueue

message_queue = MessageQueue()

client = MongoClient(HOST, PORT)
db = client[DB_NAME]
collection = db[DB_STUDENTS]
data_collection = db[DB_DATA]


async def auth(chat_id: int, login: str, password: str, state: FSMContext):
    try:
        api = await DiaryApi.auth_by_login("sh-open.ris61edu.ru", login, password)
        await api.close_session()
        if api.user_information["success"]:
            post = {"diary_session": api.sessionid, "diary_information": json.dumps(api.user_information),
                    "chat": chat_id}
            data_collection.find_one_and_update({"chat": chat_id}, {
                '$set': {"name": api.user_information["childs"][0][1], "settings": {"notification": True}}})
            await message_queue.add_message(0, chat_id=chat_id,
                                            text=message_auth_success(api.user_information["childs"][0][1],
                                                                      api.user_information["childs"][0][2]))
            if collection.find_one({"user": chat_id}):
                collection.find_one_and_update({"chat": chat_id}, {
                    '$set': {"diary_session": post["diary_session"], "diary_information": post["diary_session"]}})
            else:
                collection.insert_one(post)

            await state.set_state(UserState.AUTH)
            await addReferal(chat_id)
            await saveLoginPass(chat_id, login, password)
            await set_subscription_info(chat_id)
    except APIError as e:
        await e.session.close()

        await message_queue.add_message(0, chat_id=chat_id,
                                        text="🚧 Неправильный логин или пароль. Повторите попытку ещё раз.\n\n"
                                             "🔒 Отправь первым сообщением логин.")


async def unauth(chat_id: int, force: bool = False, message: bool = True):
    if message:
        if force:
            print("force")
            await message_queue.add_message(0, chat_id=chat_id, text=message_unauth_force, reply_markup="inline_kb_auth")
        else: await message_queue.add_message(0, chat_id=chat_id, text=message_unauth)
    else:
        if force:return message_unauth_force
        else:return message_unauth
    state = dp.current_state(chat=chat_id, user=chat_id)
    await deleteLoginPass(chat_id)
    await state.set_state(UserState.NOT_AUTH)
    collection.find_one_and_delete({"chat": chat_id})
