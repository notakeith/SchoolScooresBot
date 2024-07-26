from pymongo import MongoClient

from data import config

client = MongoClient(config.HOST, config.PORT)
storage = client[config.DB_NAME]
datastorage = storage[config.DB_DATA]
statestorage = storage[config.DB_STATE]


async def get_settings(user_id: int) -> dict:
    return datastorage.find_one({"user": user_id})["settings"]


async def get_setting(user_id: int, setting: str) -> bool:
    return datastorage.find_one({"user": user_id})["settings"][setting]

async def get_state(user_id: int) -> str:
    return statestorage.find_one({"user": user_id})["state"]

async def switch_settings(user_id: int, setting: str) -> bool:
    settings = await get_settings(user_id)
    settings[setting] = not settings[setting]
    datastorage.find_one_and_update({'user': user_id}, {'$set': {"settings": settings}})
    return settings[setting]


async def isLoginPassUsed(login: str, password: str) -> bool:
    if datastorage.find_one({"password": password, "login": login}):
        return True
    else:
        return False


async def saveLoginPass(user_id: int, login: str, password: str) -> None:
    datastorage.find_one_and_update({'user': user_id}, {'$set': {"login": login, "password": password}})


async def deleteLoginPass(user_id: int) -> None:
    datastorage.find_one_and_update({'user': user_id}, {'$set': {"login": "", "password": ""}})


async def addRefererId(user_id: int, referer_id: int):
    datastorage.find_one_and_update({'user': user_id}, {'$set': {"referer": referer_id}})


async def addEmail(user_id: int, email: str):
    datastorage.find_one_and_update({'user': user_id}, {'$set': {"email": email}})

async def checkIfEmail(user_id: int, getemail:bool=False):
    data = datastorage.find_one({'user': user_id})
    try:
        if data["email"]:
            if getemail: return data["email"]
            else: return True
        else:
            return False
    except KeyError: return False
