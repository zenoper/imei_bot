from aiogram.dispatcher.filters.state import StatesGroup, State


class VBAInfo(StatesGroup):
    fullname = State()
    employee_id = State()
    telegram_id = State()
    shopname = State()
    phonenumber = State()
    # supervisorname = State()
    confirmation = State()


class AddIMEI(StatesGroup):
    photo = State()
    IMEI_confirm = State()
    IMEI_manual = State()
    model = State()
    specific_model = State()
    confirmation = State()


class AddVBAList(StatesGroup):
    file = State()
    finish = State()


class StockCount(StatesGroup):
    start = State()
    confirmation = State()


class IMEISendAllowance(StatesGroup):
    permission_granted = State()


class Sticker(StatesGroup):
    ask = State()
