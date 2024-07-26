import asyncio
import datetime
from multiprocessing import Process, freeze_support

from pymongo import MongoClient

from data.config import HOST, PORT, DB_NAME, DB_STUDENTS, API_TIMEOUT, COMP_TIMEOUT
from utils.logger import logging
from utils.db_apis.settings import get_setting, get_state
from barsdiary.aio import DiaryApi
import json
from barsdiary.types import APIError
from utils.auth import unauth

client = MongoClient(HOST, PORT)
db = client[DB_NAME]
collection_students = db[DB_STUDENTS]

from utils.message_queue import MessageQueue

message_queue = MessageQueue()


async def dict_compare(d1, d2):
    def recursive_dict_compare(d1, d2):
        added, removed, modified, same = {}, {}, {}, {}
        for key in d1:
            if key not in d2:
                removed[key] = d1[key]
            elif isinstance(d1[key], dict) and isinstance(d2[key], dict):
                added[key], removed[key], modified[key], same[key] = recursive_dict_compare(d1[key], d2[key])
            elif d1[key] != d2[key]:
                modified[key] = (d1[key], d2[key])
            else:
                same[key] = d1[key]
        for key in d2:
            if key not in d1:
                added[key] = d2[key]
        return added, removed, modified, same

    if d1 == d2: return {}, {}, {}, d1

    return recursive_dict_compare(d1, d2)


def _today() -> str:
    return datetime.date.today().strftime("%d.%m.%Y")


def run_in_parallel(*fns) -> None:
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


async def notify(chat_id: int):
    data = collection_students.find_one({"chat": chat_id})
    scores = data["scores"]
    try:
        prescores = data["prescores"]
    except KeyError:
        prescores = scores
    added, removed, modified, same = await dict_compare(prescores, scores)
    # print(added, removed, modified)  # TODO: если сразу несколько оценок, то объединить чтобы отправилось 1 сообщением
    # logging("debug", chat_id, added, removed, modified)
    if added:
        for lesson in added:
            for date, score in dict(added[lesson]).items():
                await message_queue.add_message(1, chat_id=chat_id,
                                                text=f'🔔 Новая оценка!\n\n🍏 Оценка {score} по предмету {lesson.capitalize()} на {date} число была поставлена.\n')
    if removed:
        for lesson in removed:
            for date, score in dict(removed[lesson]).items():
                await message_queue.add_message(1, chat_id=chat_id,
                                                text=f'🔔 Оценка удалена! \n\n🍎 Оценка {score} по предмету {lesson.capitalize()} на {date} число была удалена.\n')
    if modified:
        for lesson in modified:
            for date, scores in dict(modified[lesson]).items():
                await message_queue.add_message(1, chat_id=chat_id,
                                                text=f'🔔 Оценка исправлена!\n\n📚 Оценка по предмету {lesson.capitalize()} на {date} была изменена с {scores[1]} на {scores[0]}.\n')
    collection_students.find_one_and_update({"chat": chat_id}, {'$set': {"prescores": scores}})
    logging("success", f"User @{chat_id} is notificated")


async def refresh(chat_id: int) -> None:
    user = collection_students.find_one({"chat": chat_id})
    api = await DiaryApi.auth_by_diary_session("sh-open.ris61edu.ru",
                                               diary_session=user["diary_session"],
                                               diary_information=json.loads(user["diary_information"]))
    try:
        lessons_score = await api.lessons_scores(_today())
        scores = {}
        for lesson, data in lessons_score.data.items():
            score_array = {}
            for item in data:
                score_array[item.date] = int(''.join(repr(x) for x in item.marks.values())[2])
            scores.update({lesson: score_array})
        collection_students.find_one_and_update({"chat": chat_id}, {'$set': {"scores": scores}})
        await api.close_session()
    except APIError as error:
        if not error.json_success:
            await unauth(chat_id, True)
            await error.session.close()
        else:
            raise error
    logging("success", f"User @{chat_id} is refreshed")


async def mainloop():
    while 1:
        for obj in collection_students.find().sort([('$natural', 1)]):
            if await get_state(obj["chat"]) == "UserState:AUTH":
                await refresh(obj["chat"])
                if await get_setting(obj["chat"], "notification"):
                    await notify(obj["chat"])
        await asyncio.sleep(API_TIMEOUT)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def between_callback():
    loop.run_until_complete(mainloop())


def run():
    freeze_support()
    run_in_parallel(between_callback)


if __name__ == '__main__':
    run()
