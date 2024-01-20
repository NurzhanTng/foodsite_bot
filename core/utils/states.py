from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    SHOW_MENU = State()
    MY_DATA = State()
    CONTACTS = State()
