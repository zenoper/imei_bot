from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from states.Userstates import PersonalInfo


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalamu alaykum, {message.from_user.full_name}! \n\nIltimos, to'liq ismingizni kiriting!")
    await PersonalInfo.fullname.set()
