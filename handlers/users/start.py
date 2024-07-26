from aiogram import types
from aiogram.dispatcher import FSMContext

from data.text import message_start, message_start2, message_sub
from loader import dp
from utils.auth import auth
from utils.userstates import UserState
from aiogram.utils.deep_linking import decode_payload
from utils.message_queue import MessageQueue
from utils.db_apis.settings import isLoginPassUsed
from utils.db_apis.referal import setReferalID,addReferal
message_queue = MessageQueue()

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message, state: FSMContext):
    await message_queue.add_message(0, chat_id=message.from_user.id, text=message_start(message.from_user.first_name),parse_mode='Markdown')
    await message_queue.add_message(0, chat_id=message.from_user.id, text=message_sub(), reply_markup="inline_kb_sub")

    await UserState.NOT_SUB.set()

    args = message.get_args()
    if args:
        refererID = decode_payload(args)
        print(refererID)
        await setReferalID(message.from_user.id,int(refererID))
        await addReferal(message.from_user.id)

@dp.message_handler(commands=['start'], state=UserState.NOT_SUB)
async def command_start(message: types.Message, state: FSMContext):
    await message_queue.add_message(0, chat_id=message.from_user.id, text=message_start(message.from_user.first_name),parse_mode='Markdown')
    await message_queue.add_message(0, chat_id=message.from_user.id, text=message_sub(), reply_markup="inline_kb_sub")

    await UserState.NOT_SUB.set()

    args = message.get_args()
    if args:
        refererID = decode_payload(args)
        print(refererID)
        await setReferalID(message.from_user.id,int(refererID))
        await addReferal(message.from_user.id)

@dp.message_handler(commands=['start'], state=UserState.AUTH)
async def command_start(message: types.Message):
    await message_queue.add_message(0, chat_id=message.from_user.id, text=message_start2(message.from_user.first_name),parse_mode='Markdown')


@dp.message_handler(state=UserState.LOGIN)
async def command_start(message: types.Message, state: FSMContext):
    await message_queue.add_message(0, chat_id=message.from_user.id, text="""🔐 Отправьте пароль\n""")
    if message.text == "/support":
        await UserState.NOT_AUTH.set()
    else:
        await UserState.PASSWORD.set()
        await state.update_data({"newlogin": message.text})


@dp.message_handler(state=UserState.PASSWORD)
async def command_start(message: types.Message, state: FSMContext):
    await state.update_data({"newpassword": message.text})
    await UserState.LOGIN.set()
    data = await state.get_data()
    if not await isLoginPassUsed(login=data["newlogin"], password=data["newpassword"]):
        await auth(message.chat.id, data["newlogin"], data["newpassword"], state)
    else:
        await message_queue.add_message(0, chat_id=message.from_user.id,
                                        text="""🚧 Данный дневник привязан к другому телеграмм аккаунту. Попробуйте ввести дргуие данные или поменяйте пароль. Если вы считаете что данное сообщение ошибочное - напишите в поддержку - /support\n
🔒 Отправь первым сообщением логин.""")

