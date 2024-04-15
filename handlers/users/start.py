from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from states.Userstates import PersonalInfo, Add


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await db.select_user(telegram_id=message.from_user.id)
    if user and user[7] == message.from_user.id:
        await message.answer(f"Welcome back, {user[1]}! \n\n/add_imei orqali IMEI qo'shishingiz mumkin!")
        await Add.add.set()
    else:
        await message.answer(f"Assalamu alaykum, {message.from_user.full_name}! \n\nIltimos, to'liq ismingizni kiriting!")
        await PersonalInfo.fullname.set()
