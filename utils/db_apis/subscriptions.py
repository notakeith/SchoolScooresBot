from datetime import datetime, timedelta

from pymongo import MongoClient

from data import config
from data.config import FREE_PERIOD_INT,END_OF_THE_YEAR

client = MongoClient(config.HOST, config.PORT)
storage = client[config.DB_NAME]
storagesub = storage[config.DB_DATA]

from loader import dp   

async def set_subscription_info(user_id: int) -> None:
    a = storagesub.find_one({"user": user_id})
    if a:
        try:
            a["sub_exp_date"]
        except Exception as e:
            storagesub.find_one_and_update({'user':user_id},{ '$set': { "sub_exp_date" : END_OF_THE_YEAR}})

async def get_subscription_info(user_id: int) -> dict:
    try:
        data = storagesub.find_one({"user": user_id})
        if data["sub_exp_date"] != None != "0":
            days_to_exp = ((datetime.today() - datetime.strptime(data["sub_exp_date"],
                                                                 "%d.%m.%Y")).days) * -1
            date_to_exp = data["sub_exp_date"]
            return {"DATE_TO_EXP": date_to_exp, "DAYS_TO_EXP_INT": days_to_exp}
    except Exception as e:
        await set_subscription_info(user_id)
        await get_subscription_info(user_id)


async def validate(user_id:int) -> bool:
    data = storagesub.find_one({"user": user_id})
    if data is not None:
        if data["sub_exp_date"] != "0":
            days_to_exp = ((datetime.today() - datetime.strptime(data["sub_exp_date"],
                                                                 "%d.%m.%Y")).days) * -1
            return days_to_exp > 0

async def increase_subscription(user_id: int, amount: int) -> None:
    data = storagesub.find_one({"user": user_id})
    if data is not None:
        days_to_exp = (
                datetime.strptime(data["sub_exp_date"], "%d.%m.%Y") + timedelta(
            days=amount)).strftime("%d.%m.%Y")
        storagesub.update_one({"user": user_id}, {'$set': {"sub_exp_date": days_to_exp}})


async def decrease_subscription(user_id: int, amount: int) -> None:
    data = storagesub.find_one({"user": user_id})
    if data is not None:
        days_to_exp = (
                datetime.strptime(data["sub_exp_date"], "%d.%m.%Y") - timedelta(
            days=amount)).strftime("%d.%m.%Y")
        storagesub.update_one({"user": user_id}, {'$set': {"sub_exp_date": days_to_exp}})

async def increase_subscription_2date(user_id: int, date: str) -> None:
    if storagesub.find_one({"user": user_id}) is not None:
        days_to_exp = (storagesub.update_one({"user": user_id}, {'$set': {"sub_exp_date": date}}))