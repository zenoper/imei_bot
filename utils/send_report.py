from aiogram.dispatcher import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
import asyncio

from aiogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from aiogram.dispatcher import FSMContext
import pandas as pd
from io import BytesIO

from data.config import HR
from states.Userstates import StockCount


async def send_daily_report():
    from loader import db, bot
    # Generate an in-memory Excel file
    excel_file = await db.join_tables_and_export()

    # Create a BytesIO object to store the Excel file in memory
    output = BytesIO()
    # Use the ExcelWriter context manager to write the DataFrame to Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        excel_file.to_excel(writer, index=False)
    output.seek(0)

    # Extract bytes to reuse for each user
    excel_bytes = output.getvalue()

    # Send the document to all users in HR
    for user in HR:
        user_output = BytesIO(excel_bytes)  # Create a new BytesIO object for each user
        user_output.seek(0)
        document = InputFile(user_output, filename="DailyReport.xlsx")
        await bot.send_document(chat_id=user, document=document, caption="Here's your daily report.")
        user_output.close()  # Close the BytesIO object


async def stock_keyboard(telegram_id):
    from loader import db, bot
    markup = InlineKeyboardMarkup(row_width=3)
    # Add a button for each model
    models = [
        'V30', 'V29', 'V29e', 'V27', 'V27e', 'V25', 'V25pro', 'V25e',
        'V23', 'V23e', 'V21', 'V21e', 'Y100', 'Y53S 6GB', 'Y53S 8GB', 'Y36',
        'Y35', 'Y33S 128GB', 'Y33S 64GB', 'Y31', 'Y27', 'Y27s', 'Y22', 'Y21',
        'Y17s 4 128', 'Y17s 6 128', 'Y16', 'Y15S', 'Y12S', 'Y03 64GB', 'Y03 128GB',
        'Y02T', 'Y1S', 'X100'
    ]

    for model_name in models:
        record = await db.select_stock(telegram_id=telegram_id, model_name=model_name)
        model_edited = model_name.replace(" ", "_").replace("/", "_").lower()
        model_count = record[model_edited]
        # Buttons for decrementing, showing model name, and incrementing stock
        model_button = InlineKeyboardButton(f"{model_name} : {model_count}", callback_data="doesn't work")
        increment_button1 = InlineKeyboardButton("+1", callback_data=f'{model_name},{model_count},1')
        increment_button10 = InlineKeyboardButton("+10", callback_data=f'{model_name},{model_count},10')
        markup.add(model_button, increment_button1, increment_button10)
    return markup


async def ask_daily_stock():
    from loader import dp, db, bot
    vbas = await db.select_all_vbas()  # Up to 200 user IDs
    message_text = "Agar yangi telefonlar kelgan bo'lsa, model miqdorini ko'paytiring! :"
    for vba in vbas:
        try:
            user_id = vba[5]  # Assuming vba[5] contains the correct user_id
            chat_id = user_id  # In private chats, user_id and chat_id are usually the same
            await bot.send_message(user_id, message_text, reply_markup=await stock_keyboard(user_id))
            # Properly set the state for the user and chat
            state = dp.current_state(user=user_id, chat=chat_id)
            await state.set_state(StockCount.start)
            await asyncio.sleep(0.1)  # Sleep for 100ms between messages
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")


def schedule_daily_tasks():
    scheduler = AsyncIOScheduler()
    uzb_timezone = timezone('Asia/Tashkent')

    scheduler.add_job(
        send_daily_report,
        trigger=CronTrigger(hour=9, minute=4, second=0, timezone=uzb_timezone),
        replace_existing=True,
        id="send_daily_report"
    )

    # scheduler.add_job(
    #     ask_daily_stock,
    #     trigger=CronTrigger(hour=17, minute=20, second=0, timezone=uzb_timezone),
    #     replace_existing=True,
    #     id="ask_daily_stock"
    # )

    scheduler.start()
