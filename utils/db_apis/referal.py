from pymongo import MongoClient

from data import config

from utils.message_queue import MessageQueue
message_queue = MessageQueue()

client = MongoClient(config.HOST, config.PORT)
storage = client[config.DB_NAME]
datastorage = storage[config.DB_DATA]

async def addReferal(user_id: int):
    try:
        data = datastorage.find_one({"user": user_id})
        id = data["referer"]
    except Exception as e:
        return False
    try:
        referals = datastorage.find_one({"user": id})["referals"]
    except Exception as e:
        await message_queue.add_message(priority=0, chat_id=id,
                                        text=f"🥳 По вашей ссылке зарегистрировался новый участник\n🪪 {user_id}\n\n📈 Ваше количество реферальных баллов увеличено на {1}. Всего у Вас {await addReferalCount(id,1)} баллов.")

        datastorage.find_one_and_update({'user': id}, {'$set': {"referals": [user_id]}})
        referals = [user_id]
    if user_id not in referals:
        referals.append(user_id)
        await message_queue.add_message(priority=0, chat_id=id,
                                        text=f"🥳 По вашей ссылке зарегистрировался новый участник\n🪪 {user_id}\n\n📈 Ваше количество реферальных баллов увеличено на {1}. Всего у Вас {await addReferalCount(id,1)} баллов.")
        datastorage.find_one_and_update({'user': id}, {'$set': {"referals": referals}})

async def setReferalID(user_id:int,referalid:int):
    datastorage.find_one_and_update({'user': user_id}, {'$set': {"referer": referalid}})

async def getReferals(user_id:int):
    return len(datastorage.find_one({"user": user_id})["referals"])

async def addReferalCount(user_id:int,count:int):
    try:
        referalScores =  datastorage.find_one({'user': user_id})["referalScores"]+count
        datastorage.find_one_and_update({'user': user_id}, {'$set': {"referalScores":referalScores}})
        return referalScores
    except KeyError:
        datastorage.find_one_and_update({'user': user_id}, {'$set': {"referalScores": 0}})
        return 0
    # TODO: включение/выключение уведомлений о увелечение баллов
    # Ваше количество реферальных баллов увеличено на {scores}. Всего у Вас {referalScores} баллов.

async def addReferalCountToReferer(user_id:int,count:int):
    try:
        data = datastorage.find_one({"user": user_id})
        id = data["referer"]
    except Exception as e:
        return False
    try:
        referalScores =  datastorage.find_one({'user': id})["referalScores"]+count
        datastorage.find_one_and_update({'user': id}, {'$set': {"referalScores":referalScores}})
        await message_queue.add_message(0,chat_id=id,text=f"📈 Ваше количество реферальных баллов увеличено на {count}. Всего у Вас {referalScores} баллов.")
        return referalScores
    except KeyError:
        datastorage.find_one_and_update({'user': id}, {'$set': {"referalScores": 0}})
        return 0
    # TODO: включение/выключение уведомлений о увелечение баллов
    # Ваше количество реферальных баллов увеличено на {scores}. Всего у Вас {referalScores} баллов.

async def getReferalCount(user_id:int):
    try:
        return datastorage.find_one({'user': user_id})["referalScores"]
    except KeyError:
        return 0

