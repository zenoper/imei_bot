from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
import asyncio
from aiogram.types import InputFile

import pandas as pd
from io import BytesIO

from data.config import HR


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


def schedule_daily_tasks():
    scheduler = AsyncIOScheduler()
    uzb_timezone = timezone('Asia/Tashkent')

    scheduler.add_job(
        send_daily_report,
        trigger=CronTrigger(hour=15, minute=37, second=0, timezone=uzb_timezone),
        replace_existing=True
    )

    scheduler.start()
