#не работает, создано для сбора email для последующей рассылки
from aiogram import types
import re
from loader import dp
from utils.userstates import UserState
from utils.message_queue import MessageQueue
from utils.db_apis.settings import addEmail
message_queue = MessageQueue()


async def is_valid_email_format(email):
    email_pattern = r'^[\w\.-]+@[\w\.-]+$'
    if re.match(email_pattern, email):
        return True
    else:
        return False

@dp.message_handler(commands=['email'], state=UserState.AUTH)
async def command_email(message: types.Message):
    data = message.text.split()
    if len(data) == 2:
        if await is_valid_email_format(data[1]):
            await message_queue.add_message(0,chat_id=message.from_user.id,text=f"✅ Вы привязали следующий Email: {data[1]}")
            await addEmail(message.from_user.id,data[1])
        else:
            await message_queue.add_message(0,chat_id=message.from_user.id,text=f"❌ Email адресс указан неверно.")
    else:
        await message_queue.add_message(0,chat_id=message.from_user.id,text=f"🚧 Email адресс не привязан. Вы не указали email или указали что-то лишнее. \n\nПример использования функции: \n/email mail123@example.com")
