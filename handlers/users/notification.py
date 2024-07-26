from aiogram import types
from loader import dp
from utils.userstates import UserState
from utils.db_apis.settings import switch_settings
from utils.message_queue import MessageQueue

message_queue = MessageQueue()


@dp.message_handler(commands=['notification'], state=UserState.AUTH)
async def command_notification(message: types.Message):
    if await switch_settings(message.from_user.id, "notification"):
        await message_queue.add_message(0, chat_id=message.chat.id,text="🍏 Уведомления о изменениях оценок были включены")
    else:
        await message_queue.add_message(0, chat_id=message.chat.id,text="🍎 Уведомления о изменениях оценок были выключены")
