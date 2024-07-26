import json
import uuid
from datetime import datetime, timedelta

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.message import ContentType
from pymongo import MongoClient
from yookassa import Configuration, Payment

from data.config import PAYMENT_TOKEN, ACCOUNT_ID, SECRET_KEY, HOST, PORT, DB_NAME, DB_YOOKASSA
from loader import dp
from utils.db_apis.subscriptions import increase_subscription_2date, get_subscription_info
from utils.message_queue import MessageQueue
from utils.userstates import UserState
from utils.db_apis.settings import checkIfEmail
from utils.db_apis.referal import addReferalCountToReferer

print("Payment")

message_queue = MessageQueue()

client = MongoClient(HOST, PORT)
db = client[DB_NAME]
data_collection = db[DB_YOOKASSA]

Configuration.account_id = ACCOUNT_ID
Configuration.secret_key = SECRET_KEY


async def get_sub1month_keyboard(user_id: int):
    try:
        old_payment = data_collection.find_one_and_delete({"user_id": 0})
        idempotence_key = str(uuid.uuid4())
        Payment.cancel(
            old_payment["data"]["id"],
            idempotence_key
        )
    except Exception as e:
        pass

    email = await checkIfEmail(user_id, getemail=True)

    payment = Payment.create({
        "amount": {
            "value": "00.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "example.com"
        },
        "capture": True,
        "description": f"Предоставление доступа к сервису \"Оценки на ладони\" сроком на 1 мес. Для пользователя @{user_id}",
        "metadata": {
            "user_id": user_id,
            "type": "sub1month",
        },
        "receipt": {
            "customer": {
                "email": email
            },
            "items": [
                {
                    "description": f"Предоставление доступа к сервису \"Оценки на ладони\" сроком на 1 мес. Для пользователя @{user_id}",
                    "quantity": "1",
                    "amount": {
                        "value": "00.00",
                        "currency": "RUB"
                    },
                    "vat_code": "1"
                }
            ]
        }
    }, uuid.uuid4())
    print(payment)
    inline_btn_pay1mnth = InlineKeyboardButton("🔗 Оплатить",
                                               url=payment.confirmation.confirmation_url)
    inline_btn_checkpay1mnth = InlineKeyboardButton("✅ Проверить", callback_data="checkPay")
    inline_kb_pay1mnth = InlineKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
    inline_kb_pay1mnth.add(inline_btn_pay1mnth)
    inline_kb_pay1mnth.add(inline_btn_checkpay1mnth)
    data_collection.insert_one({"user_id": user_id, "data": json.loads(payment.json())})

    return inline_kb_pay1mnth


@dp.callback_query_handler(text="checkPay", state="*")
async def call_checkPay(call: types.CallbackQuery):
    paymentdata = data_collection.find_one({"user_id": call.from_user.id})

    payment_id = paymentdata["data"]["id"]
    payment = Payment.find_one(payment_id)

    if payment.paid:
        await call.answer()
        current_days_to_exp = (await get_subscription_info(call.from_user.id))["DAYS_TO_EXP_INT"]
        await message_queue.add_message(100, chat_id=call.from_user.id, text=f"""✅ Вы купили подписку на 1 месяц.\n
Она будет активна до {(datetime.now() + timedelta(days=(30 + current_days_to_exp))).strftime('%d.%m.%Y')} числа""",
                                        parse_mode='Markdown')
        await increase_subscription_2date(call.from_user.id,
                                          (datetime.now() + timedelta(days=(30 + current_days_to_exp))).strftime(
                                              '%d.%m.%Y'))
        await message_queue.add_message(0, chat_id=call.from_user.id, message_id=call.message.message_id,
                                        delete_reply_markup=True)
        await addReferalCountToReferer(call.from_user.id,1)
    else:
        await call.answer("Оплата не подтверждена")


async def send_3month_order(chat_id):
    await dp.bot.send_invoice(chat_id, title='Оплата подписки',
                              description='Приобритение подписки для телеграмм бота "Оценки на ладони" на 3 месяца',
                              provider_token=PAYMENT_TOKEN,
                              currency='rub',
                              prices=[types.LabeledPrice(label='Подписка на 3 месяца', amount=149 * 100)],
                              start_parameter='telegrammbot_name',
                              provider_data={
                                  "receipt": {
                                      "email": await checkIfEmail(chat_id, getemail=True),
                                      "items": [
                                          {

                                              "description": f"Предоставление доступа к сервису \"Оценки на ладони\" сроком на 3 мес. Для пользователя @{chat_id}",
                                              "quantity": "1",
                                              "amount": {
                                                  "value": "00.00",
                                                  "currency": "RUB"
                                              },
                                              "vat_code": "1"
                                          }
                                      ]
                                  }
                              },
                              payload='sub3month')


async def send_1year_order(chat_id):
    await dp.bot.send_invoice(chat_id, title='Оплата подписки',
                              description='Приобритение подписки для телеграмм бота "Оценки на ладони" на 9 месяцев',
                              provider_token=PAYMENT_TOKEN,
                              currency='rub',
                              prices=[types.LabeledPrice(label='Подписка на 9 месяцев', amount=399 * 100)],
                              start_parameter='telegrammbot_name',
                              provider_data={
                                  "receipt": {
                                      "email": await checkIfEmail(chat_id, getemail=True),
                                      "items": [
                                          {

                                              "description": f"Предоставление доступа к сервису \"Оценки на ладони\" сроком на 9 мес. Для пользователя @{chat_id}",
                                              "quantity": "1",
                                              "amount": {
                                                  "value": "00.00",
                                                  "currency": "RUB"
                                              },
                                              "vat_code": "1"
                                          }
                                      ]
                                  }
                              },
                              payload='sub1year')


@dp.pre_checkout_query_handler(lambda query: True, state=UserState.AUTH)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await dp.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state=UserState.AUTH)
async def got_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    print(payload)
    current_days_to_exp = (await get_subscription_info(message.from_user.id))["DAYS_TO_EXP_INT"]
    if payload == "sub3month":
        await message_queue.add_message(100, chat_id=message.chat.id, text=f"""✅ Вы купили подписку на 3 месяца.\n
Она будет активна до {(datetime.now() + timedelta(days=(90 + current_days_to_exp))).strftime('%d.%m.%Y')} числа""",
                                        parse_mode='Markdown')
        await increase_subscription_2date(message.from_user.id,
                                          (datetime.now() + timedelta(days=(90 + current_days_to_exp))).strftime(
                                              '%d.%m.%Y'))
        await addReferalCountToReferer(message.from_user.id,2)
    if payload == "sub1year":
        await message_queue.add_message(100, chat_id=message.chat.id, text=f"""✅ Вы купили подписку на 9 месяца.\n
Она будет активна до {(datetime.now() + timedelta(days=(270 + current_days_to_exp))).strftime('%d.%m.%Y')} числа""",
                                        parse_mode='Markdown')
        await increase_subscription_2date(message.from_user.id,
                                          (datetime.now() + timedelta(days=(270 + current_days_to_exp))).strftime(
                                              '%d.%m.%Y'))
        await addReferalCountToReferer(message.from_user.id,5)
