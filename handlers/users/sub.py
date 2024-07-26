from aiogram import types

from loader import dp

from utils.userstates import UserState

from utils.message_queue import MessageQueue
message_queue = MessageQueue()

@dp.callback_query_handler(text="checkSub",state="*")
async def callback_checkSub(call: types.CallbackQuery):
    user_channel_status = await dp.bot.get_chat_member(chat_id=-1001925624749, user_id=int(call.from_user.id))
    if user_channel_status.status != types.ChatMemberStatus.LEFT:
        await call.answer("Вы подписаны")
        await message_queue.add_message(0, chat_id=call.from_user.id, message_id=call.message.message_id,delete_reply_markup=True)
        await message_queue.add_message(0, chat_id=call.from_user.id, text="🔒 Отправь первым сообщением логин")

        await UserState.LOGIN.set()
    else:
        await call.answer("Вы не подписаны")