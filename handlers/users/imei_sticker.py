from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram import types
from loader import db, dp
from states.Userstates import Sticker
from data.config import ADMINS


@dp.message_handler(Command(["search_sticker"]), state='*', chat_id=ADMINS[0])
async def search(message: types.Message):
    await message.answer("Send IMEI")
    await Sticker.ask.set()


@dp.message_handler(state=Sticker.ask, chat_id=ADMINS[0])
async def search(message: types.Message, state: FSMContext):
    sticker = await db.select_imei(imei=message.text)
    if sticker:
        await message.answer_photo(photo=sticker[3])
        await state.finish()
    else:
        await message.answer("Doesn't exist")
 