from aiogram.dispatcher.filters.builtin import Command
import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from loader import db, bot, dp
from states.Userstates import StockCount
from utils.send_report import stock_keyboard


@dp.callback_query_handler(lambda c: c.data == 'confirmation', state=StockCount.start)
async def confirmation_handler(callback_query: types.CallbackQuery, state: FSMContext):
    # Deleting the message
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    await state.finish()


@dp.callback_query_handler(lambda c: ',' in c.data, state=StockCount.start)
async def handle_stock_callback(query: CallbackQuery):
    telegram_id = query.from_user.id
    # Extracting model name, current count, and increment value from the callback data
    data = query.data.split(',')
    model, current_count, increment = data
    increment = int(increment)

    # Fetch the most current stock directly from the database instead of using the old count
    stock_record = await db.select_stock(telegram_id=telegram_id, model_name=model)
    model_key = model.replace(" ", "_").replace("/", "_").lower()
    new_count = stock_record[model_key] + increment

    # Update the database with the new stock count
    await db.update_stock_count(model_name=model, count=new_count, telegram_id=telegram_id)

    # Edit the existing message to update text and buttons
    await query.message.edit_text(
        text="Agar yangi telefonlar kelgan bo'lsa, model miqdorini ko'paytiring! :",
        reply_markup=await stock_keyboard(telegram_id=telegram_id)
    )
    await query.answer()
