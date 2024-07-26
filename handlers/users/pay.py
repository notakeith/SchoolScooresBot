from aiogram import types

from loader import dp
from utils.userstates import UserState
from utils.message_queue import MessageQueue
from utils.db_apis.settings import checkIfEmail

message_queue = MessageQueue()


@dp.message_handler(commands=['pay'], state=UserState.AUTH)
async def command_pay(message: types.Message):
    if await checkIfEmail(message.from_user.id):
        #(но в телеграмме 70% ботов сделаны на немилинге или подобном, где деньги поступают на киви, который сейчас заблокирован, да-да..) и
        text = """Вы можете купить следующие варианты подписки:\n"""
        await message_queue.add_message(0, chat_id=message.chat.id, text=text, parse_mode="MarkdownV2",
                                        reply_markup="inline_kb_payment", photo_url="https://i.ibb.co/8DqFRq8/image.jpg")
    else:
        text = """📧 Перед тем как купить подписку, вам нужно указать адрес электронной почты. Это обычное дело, он нам нужен для отправки чеков. Чтобы привязать почту напишите /email.\n
Пример: /email example123@yandex.ru"""
        await message_queue.add_message(0, chat_id=message.chat.id, text=text)

@dp.callback_query_handler(text=['sub1month'], state=UserState.AUTH)
async def got_sub1month(call: types.CallbackQuery):
    await message_queue.add_message(3, chat_id=call.from_user.id,
                                    text="Приобритение подписки для телеграмм бота \"Оценки на ладони\" на 1 месяц", reply_markup="inline_kb_sub1month")
    await message_queue.add_message(0, chat_id=call.from_user.id, message_id=call.message.message_id,
                                    delete_reply_markup=True)


@dp.callback_query_handler(text=['sub3month'], state=UserState.AUTH)
async def got_sub3month(call: types.CallbackQuery):
    await message_queue.add_message(3, chat_id=call.from_user.id, invoceOrder="sub3month")
    await message_queue.add_message(0, chat_id=call.from_user.id, message_id=call.message.message_id,
                                    delete_reply_markup=True)


@dp.callback_query_handler(text=['sub1year'], state=UserState.AUTH)
async def got_sub1year(call: types.CallbackQuery):
    await message_queue.add_message(3, chat_id=call.from_user.id, invoceOrder="sub1year")
    await message_queue.add_message(0, chat_id=call.from_user.id, message_id=call.message.message_id,
                                    delete_reply_markup=True)
