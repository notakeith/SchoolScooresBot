from aiogram import types

from loader import dp
from utils.db_apis.support import add_appeal
from data.text import get_support_message
from  utils.db_apis.referal import getReferalCount,addReferalCount, addReferal

from utils.message_queue import MessageQueue
from pymongo import MongoClient

from data import config

client = MongoClient(config.HOST, config.PORT)
storage = client[config.DB_NAME]
datastorage = storage[config.DB_STUDENTS]

message_queue = MessageQueue()
def calc_to_3_5(scores):
    scores2 = scores[:]
    avg_scores2 = sum(scores) / len(scores)
    if avg_scores2 >= 4.6: return 0
    fives_to_3_5 = 0
    while avg_scores2 < 3.6:
        scores2.append(5)
        avg_scores2 = sum(scores2) / len(scores2)
        fives_to_3_5 += 1
    return fives_to_3_5
def calc_to_4_5(scores):
    scores1 = scores[:]
    avg_scores1 = sum(scores) / len(scores)
    if avg_scores1 >= 4.6:return 0
    fives_to_4_5 = 0
    while avg_scores1 < 4.6:
        scores1.append(5)
        avg_scores1 = sum(scores1) / len(scores1)
        fives_to_4_5 += 1
    return fives_to_4_5
def format_grades(data):
    # Эмодзи для предметов (замените их на соответствующие предметам)
    subject_emojis = {
        'Физика': '📕',
        'Химия': '🧪',
        'Математика': '🧮',
        'Алгебра': '🧮',
        'Геометрия': '🧮',
        'История': '📜',
        'Литература': '📖',
        'Биология': '🌿',
        'География': '🌍',
        'Иностранный язык': '🗣️',
        'Информатика': '💻',
    }

    result = ""

    result += "5  |  4  |  3  |  2  | ср.   | до 4 | до 5 \n"
    for subject, grades_data in data.items():
        result += f"{subject_emojis.get(subject, '📚')} {subject}\n"

        grade_counts = [0, 0, 0, 0]

        total_points = 0
        total_grades = 0
        grades = []
        for date, grade in grades_data.items():
            if 1 <= grade <= 5:
                grade_counts[5 - grade] += 1
                total_points += grade
                total_grades += 1
                grades.append(grade)

        result += f"{grade_counts[0]}  |  {grade_counts[1]}  |  {grade_counts[2]}  |  {grade_counts[3]}  |"

        if total_grades > 0:
            average_grade = total_points / total_grades
            result += f"{average_grade:.2f} | {(calc_to_3_5(grades))}       | {(calc_to_4_5(grades))}"
        result += "\n"

    return result


@dp.message_handler(commands=['scores'], state="*")
async def command_scores(message: types.Message):
    try:
        data = datastorage.find_one({"chat": message.from_user.id})["scores"]
        await message_queue.add_message(priority=0, chat_id=message.from_user.id, text=format_grades(data),
                                        parse_mode="Markdown")
    except KeyError:
        await message_queue.add_message(priority=0,chat_id=message.from_user.id,text="🚧 Происходит обновление информации. Пожалуйста, подождите. Обычно это происходит до 5 минут")
