from aiogram.dispatcher.filters.builtin import Command
import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import db, bot, dp
from states.Userstates import StockCount
from states.Userstates import AddIMEI, IMEISendAllowance
from keyboards.default import UserKeyboard
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS
from datetime import datetime, date
from keyboards.inline import imei_confirmation
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dp.callback_query_handler(lambda c: c.data and 'increment' in c.data)
async def process_stock_adjustment(callback_query: types.CallbackQuery):
    # Split the callback data into model name, current count, and increment value
    print(callback_query.data)
    model_name, model_count, increment = callback_query.data.split(',')
    new_count = int(model_count) + int(increment)

    await db.update_stock_count(model_name=model_name, count=new_count, telegram_id=callback_query.from_user.id)

    # Update the inline buttons to reflect the new count
    markup = InlineKeyboardMarkup()
    model_button = InlineKeyboardButton(f"{model_name}: {new_count}", callback_data=f'show:{model_name}:{new_count}')
    increment_button1 = InlineKeyboardButton("+1", callback_data=f'{model_name},{model_count},1')
    increment_button10 = InlineKeyboardButton("+10", callback_data=f'{model_name},{model_count},10')
    markup.add(increment_button1, model_button, increment_button10)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Agar yangi telefonlar kelgan bo'lsa, model miqdorini ko'paytiring! :",
        reply_markup=markup
    )
    await callback_query.answer()