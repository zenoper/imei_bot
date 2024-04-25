from aiogram.dispatcher.filters.state import StatesGroup, State


class VBAInfo(StatesGroup):
    fullname = State()
    employee_id = State()
    telegram_id = State()
    shopname = State()
    phonenumber = State()
    # supervisorname = State()
    confirmation = State()


class SendIMEI(StatesGroup):
    photo = State()
    phonemodel = State()
    IMEI = State()
    sticker = State()
    confirmation = State()


class IMEISendAllowance(StatesGroup):
    permission_granted = State()


class Sticker(StatesGroup):
    ask = State()
