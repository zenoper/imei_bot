from aiogram.dispatcher.filters.state import StatesGroup, State


class PersonalInfo(StatesGroup):
    fullname = State()
    region = State()
    shopname = State()
    phonenumber = State()
    supervisorname = State()
    confirmation = State()


class SendIMEI(StatesGroup):
    photo = State()
    phonemodel = State()
    IMEI = State()
    sticker = State()
    confirmation = State()


class Add(StatesGroup):
    add = State()


class Sticker(StatesGroup):
    ask = State()
