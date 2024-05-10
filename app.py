from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.send_report import schedule_daily_tasks, ask_daily_stock, send_daily_report


async def on_startup(dispatcher):
    await db.create()
    # await db.drop_vbas()
    # await db.drop_imei()
    # await db.drop_stock()
    await db.create_table_vba()
    await db.create_table_imei()
    await db.create_table_stock_count()

    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    schedule_daily_tasks()
    # await ask_daily_stock()
    await send_daily_report()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True, allowed_updates=["message", "callback_query"])
