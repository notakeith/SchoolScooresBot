from aiogram import types

from loader import dp
from utils.userstates import UserState
from utils.message_queue import MessageQueue

message_queue = MessageQueue()


@dp.callback_query_handler(text="login", state=UserState.NOT_AUTH)
async def command_login(call: types.CallbackQuery):
    await message_queue.add_message(0, chat_id=call.from_user.id, text="""🔒 Отправь первым сообщением логин\n""")
    await UserState.LOGIN.set()

@dp.message_handler(commands=['login'], state=UserState.NOT_AUTH)
async def command_login(message: types.Message):
    await message_queue.add_message(0, chat_id=message.from_user.id, text="""🔒 Отправь первым сообщением логин\n""")
    await UserState.LOGIN.set()
