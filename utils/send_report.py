from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
import asyncio

from aiogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
from io import BytesIO

from data.config import ADMINS, HR
from states.Userstates import StockCount


async def send_daily_report_imei():
    from loader import db, bot
    # Generate an in-memory Excel file
    excel_file = await db.imei_report()
    if excel_file is not None:
        # Create a BytesIO object to store the Excel file in memory
        output = BytesIO()
        # Use the ExcelWriter context manager to write the DataFrame to Excel
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            excel_file.to_excel(writer, index=False)
        output.seek(0)

        # Extract bytes to reuse for each user
        excel_bytes = output.getvalue()

        # Send the document to all users in HR
        user_output = BytesIO(excel_bytes)  # Create a new BytesIO object for each user
        user_output.seek(0)
        document = InputFile(user_output, filename="DailyIMEIReport.xlsx")
        await bot.send_document(chat_id=ADMINS[0], document=document, caption="Here's your daily report.")
        user_output.close()  # Close the BytesIO object
    else:
        await bot.send_message(chat_id=ADMINS[0], text="No IMEI submitted today for Sales Volume Upload :(")


async def send_daily_report():
    user = int(HR[1])
    from loader import db, bot
    # Generate an in-memory Excel file
    excel_file = await db.join_tables_and_export()
    if excel_file is not None:
        # Create a BytesIO object to store the Excel file in memory
        output = BytesIO()
        # Use the ExcelWriter context manager to write the DataFrame to Excel
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            excel_file.to_excel(writer, index=False)
        output.seek(0)

        # Extract bytes to reuse for each user
        excel_bytes = output.getvalue()

        # Send the document to all users in HR
        user_output = BytesIO(excel_bytes)  # Create a new BytesIO object for each user
        user_output.seek(0)
        document = InputFile(user_output, filename="DailyReport.xlsx")
        await bot.send_document(chat_id=user, document=document, caption="Here's your daily report.")
        user_output.close()  # Close the BytesIO object
    else:
        await bot.send_message(chat_id=user, text="No IMEI was submitted yesterday :(")


async def stock_keyboard(telegram_id):
    from loader import db
    markup = InlineKeyboardMarkup(row_width=3)
    # Add a button for each model
    models = [
        'X100', 'V30', 'V30e', 'V29', 'V29e', 'V27', 'V27e', 'V25', 'V25pro', 'V25e',
        'V23', 'V23e', 'Y100', 'Y53S 6GB', 'Y53S 8GB', 'Y36',
        'Y35', 'Y33S 128GB', 'Y33S 64GB', 'Y28 128GB', 'Y28 256GB', 'Y27', 'Y27s', 'Y22', 'Y18',
        'Y17s 4 128', 'Y17s 6 128', 'Y16', 'Y15S', 'Y03 64GB', 'Y03 128GB',
        'Y02T'
    ]

    for model_name in models:
        record = await db.select_stock(telegram_id=telegram_id, model_name=model_name)
        model_edited = model_name.replace(" ", "_").replace("/", "_").lower()
        model_count = record[model_edited]
        model_button = InlineKeyboardButton(f"{model_name} : {model_count}", callback_data="doesn't work")
        increment_button1 = InlineKeyboardButton("+1", callback_data=f'{model_name},{model_count},1')
        increment_button10 = InlineKeyboardButton("+10", callback_data=f'{model_name},{model_count},10')
        markup.add(model_button, increment_button1, increment_button10)
    confirmation = InlineKeyboardMarkup(text="Tasdiqlash ✅", callback_data="confirmation")
    markup.add(confirmation)
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
            await asyncio.sleep(0.2)  # Sleep for 100ms between messages
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")


async def ask_daily_stock_me():
    from loader import dp, db, bot
    message_text = "Agar yangi telefonlar kelgan bo'lsa, model miqdorini ko'paytiring me! :"
    try:
        user_id = int(ADMINS[0])  # Assuming vba[5] contains the correct user_id
        chat_id = user_id  # In private chats, user_id and chat_id are usually the same
        await bot.send_message(user_id, message_text, reply_markup=await stock_keyboard(user_id))
        # Properly set the state for the user and chat
        state = dp.current_state(user=user_id, chat=chat_id)
        await state.set_state(StockCount.start)
    except Exception as e:
        print(f"Failed to send message to {user_id}: {e}")


def schedule_daily_tasks():
    scheduler = AsyncIOScheduler()
    uzb_timezone = timezone('Asia/Tashkent')

    scheduler.add_job(
        send_daily_report,
        trigger=CronTrigger(hour=9, minute=0, second=0, timezone=uzb_timezone),
        replace_existing=True,
        id="send_daily_report"
    )

    scheduler.add_job(
        ask_daily_stock,
        trigger=CronTrigger(hour=19, minute=00, second=0, timezone=uzb_timezone),
        replace_existing=True,
        id="ask_daily_stock"
    )

    scheduler.add_job(
        send_daily_report_imei,
        trigger=CronTrigger(hour=9, minute=0, second=0, timezone=uzb_timezone),
        replace_existing=True,
        id="send_daily_report_imei"
    )

    scheduler.start()
