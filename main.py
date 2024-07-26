from utils.logger import logging


async def on_startup(dp):
    from utils.admins import on_startup_notify
    await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    logging("debug", 'Aiogram запущен!')

#TODO: очередь сообщений
#TODO: систему рефералов и розыгрыш на 2к рублей
if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
