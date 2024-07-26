from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    NOT_AUTH = State()
    NOT_SUB = State()
    SUB = State()
    AUTH = State()
    LOGIN = State()
    PASSWORD = State()
    SUPPORT = State
