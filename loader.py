from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from data import config

bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MongoStorage(host=config.HOST, port=config.PORT, db_name=config.DB_NAME)

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
