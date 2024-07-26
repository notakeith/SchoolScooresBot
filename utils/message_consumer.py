import asyncio
from loader import dp
from utils.keyboards import inline_kb_payment, inline_kb_sub, inline_kb_auth
from utils.payments import get_sub1month_keyboard, send_1year_order, send_3month_order
from utils.keyboards import get_inline_btn_quit


async def getKeyboard(message_data):
    if message_data["reply_markup"]:
        if message_data["reply_markup"] == "inline_kb_payment": return inline_kb_payment
        if message_data["reply_markup"] == "inline_kb_sub": return inline_kb_sub
        if message_data["reply_markup"] == "inline_kb_auth": return inline_kb_auth
        if message_data["reply_markup"] == "await get_inline_btn_quit(False)": return await get_inline_btn_quit(False)
        if message_data["reply_markup"] == "await get_inline_btn_quit(True)": return await get_inline_btn_quit(True)
        if message_data["reply_markup"] == "inline_kb_sub1month": return await get_sub1month_keyboard(message_data["chat_id"])


async def send_message(message_data):
    if message_data["test"]:
        print(message_data)
    else:
        if message_data["invoceOrder"]:
            if message_data["invoceOrder"] == "sub3month": await send_3month_order(message_data["chat_id"])
            if message_data["invoceOrder"] == "sub1year": await send_1year_order(message_data["chat_id"])
        else:
            if message_data["photo_url"]:await dp.bot.send_photo(chat_id=message_data["chat_id"],
                                                                 caption=message_data["text"],
                                                                 reply_markup=await getKeyboard(message_data),
                                                                 parse_mode=message_data["parse_mode"],
                                                                 photo=message_data["photo_url"])
            else:
                if message_data["delete_reply_markup"]:
                    await dp.bot.edit_message_reply_markup(chat_id=message_data["chat_id"],
                                                           message_id=message_data["message_id"],
                                                           reply_markup=None)
                    return ""
                else:
                    if not message_data["edit"]:await dp.bot.send_message(chat_id=message_data["chat_id"],
                                                                          text=message_data["text"],
                                                                          reply_markup=await getKeyboard(message_data),
                                                                          parse_mode=message_data["parse_mode"])
                    else:await dp.bot.edit_message_text(chat_id=message_data["chat_id"],
                                                        message_id=message_data["message_id"],
                                                        text=message_data["text"],
                                                        reply_markup=await getKeyboard(message_data))
                print(message_data)


async def message_consumer(message_queue):
    while True:
        try:
            message = await message_queue.get_next_message()
            if message:
                try:
                    await send_message(message)
                except Exception:
                    pass
            else: await asyncio.sleep(0.1)
        except TypeError as e: print(e)
        await asyncio.sleep(0.1)
