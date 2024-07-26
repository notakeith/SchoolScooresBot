from utils.logger import logging


async def on_startup(dp):
    from utils.admins import on_startup_notify
    await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    logging("debug", 'Aiogram запущен!')

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)



from utils.message_consumer import message_consumer
from utils.message_queue import MessageQueue
import asyncio



if __name__ == '__main__':
    message_queue = MessageQueue()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(message_consumer(message_queue))


from utils.scrapper import run
from multiprocessing import freeze_support
from utils.logger import logging

if __name__ == '__main__':
    run()
    freeze_support()
    logging("debug", 'Scores longpool запущен!')



