from aiogram import types

from loader import dp
from utils.db_apis.support import add_appeal
from data.text import get_support_message

from utils.message_queue import MessageQueue

message_queue = MessageQueue()


@dp.message_handler(commands=['support'], state="*")
async def command_support(message: types.Message):
    if len(message.text.split()) > 2:
        await add_appeal(message.from_user.id, text=" ".join(message.text.split()[1:]), message=message)
        await message_queue.add_message(priority=0,chat_id=message.chat.id, text=f"📥 Спасибо за обращение, ожидайте ответа, он придет в диалог с ботом. \n\nВы отправили обращение с данным текстом: \n{' '.join(message.text.split()[1:])}")
    else:
        await message_queue.add_message(0, chat_id=message.chat.id, text=get_support_message(0,2))

@dp.callback_query_handler(text="support",state="*")
async def command_support(call: types.CallbackQuery):
    await call.answer()
    await message_queue.add_message(0, chat_id=call.from_user.id, text=get_support_message(0,2))