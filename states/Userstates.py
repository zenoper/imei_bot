from aiogram.dispatcher.filters.state import StatesGroup, State


class PersonalInfo(StatesGroup):
    fullname = State()
    region = State()
    shopname = State()
    phonenumber = State()
    supervisorname = State()
    confirmation = State()
