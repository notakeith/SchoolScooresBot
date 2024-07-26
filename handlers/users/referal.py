from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.message_queue import MessageQueue
from utils.userstates import UserState
from utils.db_apis.referal import getReferals,getReferalCount

message_queue = MessageQueue()

from loader import dp

@dp.message_handler(commands=["referal"],state=UserState.AUTH)
async def get_ref(message: types.Message, state: FSMContext):
  link = await get_start_link(str(message.from_user.id), encode=True)
  try:text = f"Количество ваших рефералов: 🎓{await getReferals(message.from_user.id)}\nКоличество ваших баллов: {await getReferalCount(message.from_user.id)}\n"
  except Exception:text = ""
  await message_queue.add_message(priority=0,text=f"""{text}
Ваша реф. ссылка 🔗 {link}\n
Больше информации о текущем розыгрыше""",chat_id=message.from_user.id)