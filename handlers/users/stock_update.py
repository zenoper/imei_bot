from aiogram.dispatcher.filters.builtin import Command
import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from loader import db, bot, dp
from states.Userstates import StockCount


@dp.callback_query_handler(lambda c: ',' in c.data, state=StockCount.start)
async def handle_stock_callback(query: CallbackQuery):
    telegram_id = query.from_user.id
    models = [
        'V30', 'V29', 'V29e', 'V27', 'V27e', 'V25', 'V25pro', 'V25e',
        'V23', 'V23e', 'V21', 'V21e', 'Y100', 'Y53S 6GB', 'Y53S 8GB', 'Y36',
        'Y35', 'Y33S 128GB', 'Y33S 64GB', 'Y31', 'Y27', 'Y27s', 'Y22', 'Y21',
        'Y17s 4 128', 'Y17s 6 128', 'Y16', 'Y15S', 'Y12S', 'Y03 64GB', 'Y03 128GB',
        'Y02T', 'Y1S', 'X100'
    ]
    # Extracting model name, current count, and increment value from the callback data
    data = query.data.split(',')
    model_name, current_count, increment = data
    increment = int(increment)

    # Fetch the most current stock directly from the database instead of using the old count
    stock_record = await db.select_stock(telegram_id=query.from_user.id, model_name=model_name)
    model_key = model_name.replace(" ", "_").replace("/", "_").lower()
    new_count = stock_record[model_key] + increment

    # Update the database with the new stock count
    await db.update_stock_count(model_name=model_name, count=new_count, telegram_id=telegram_id)

    markup = InlineKeyboardMarkup(row_width=3)
    for model in models:
        record = await db.select_stock(telegram_id=telegram_id, model_name=model)
        model_edited = model.replace(" ", "_").replace("/", "_").lower()
        model_count = record[model_edited]
        # Buttons for decrementing, showing model name, and incrementing stock
        model_button = InlineKeyboardButton(f"{model} : {model_count}", callback_data="doesn't work")
        increment_button1 = InlineKeyboardButton("+1", callback_data=f'{model},{model_count},1')
        increment_button10 = InlineKeyboardButton("+10", callback_data=f'{model},{model_count},10')
        markup.add(model_button, increment_button1, increment_button10)

    # Edit the existing message to update text and buttons
    await query.message.edit_text(
        text="Agar yangi telefonlar kelgan bo'lsa, model miqdorini ko'paytiring! :",
        reply_markup=markup
    )
    await query.answer()
