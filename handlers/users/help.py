from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp, db
from data.config import ADMINS, HR


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    user = await db.select_vba(telegram_id=message.from_user.id)
    ad_hr_id = str(message.from_user.id)
    if ad_hr_id in ADMINS:
        text = ("Buyruqlar: ",
                "/start - Botni ishga tushirish",
                "/help - Yordam",
                "/add_VBA - VBA qo'shish",
                "/add_IMEI - IMEI qo'shish",
                "/add_VBA_list - VBA list qo'shish",
                "/search_sticker - Search sticker",
                "/remove_imei - Remove IMEI",
                "/update_telegramID - You know it",
                "/get_all_IMEI - Export all IMEI",
                "/add_stock_model - Add new model to stock database",
                "/ask_daily_stock_me - Stock update override"
                )
        await message.answer("\n".join(text))
    elif ad_hr_id in HR:
        text = ("Buyruqlar: ",
                "/start - Botni ishga tushirish",
                "/help - Yordam",
                "/add_VBA - VBA qo'shish"
                )
        await message.answer("\n".join(text))
    elif user:
        text = ("Buyruqlar: ",
                "/start - Botni ishga tushirish",
                "/help - Yordam",
                "/add_IMEI - IMEI qo'shish"
                )
        await message.answer("\n".join(text))
    else:
        await message.answer("You have no permission")
