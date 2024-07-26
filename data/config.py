import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
PAYMENT_TOKEN = str(os.getenv("PAYMENT_TOKEN"))
ACCOUNT_ID = int(os.getenv("ACCOUNT_ID"))
SECRET_KEY = str(os.getenv("SECRET_KEY"))

DEBUG = 0

HOST = "localhost"
PORT = 27017
DB_NAME = "schoolscoores"
DB_STUDENTS = "students"
DB_SUB = "aiogram_sub"
DB_DATA = "aiogram_data"
DB_STATE = "aiogram_state"
DB_SUPPORT = "aiogram_support"
DB_YOOKASSA = "aiogram_yookassa"
DB_MESSAGE = "message_queue"


COMP_TIMEOUT = 5
API_TIMEOUT = 5 * 60

admins_id = [
    0,
]

END_OF_THE_YEAR = "01.06.2024"

PRICE_9_MONTHS = 0
PRICE_3_MONTHS = 0
PRICE_1_MONTH = 0

FREE_PERIOD_INT = 0
FREE_PERIOD_STR = "0 недели"

VERSION = "1.0.4r"
