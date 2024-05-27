from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram import types
from loader import db, dp, bot
from states.Userstates import Sticker, AddVBAList, RemoveIMEI, UpdateTelegramID
from data.config import ADMINS


import pandas as pd
import asyncio
import os


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


@dp.message_handler(Command(["add_VBA_list"]), state='*', chat_id=ADMINS[0])
async def add(message: types.Message):
    await message.answer("Send file")
    await AddVBAList.file.set()


@dp.message_handler(state=AddVBAList.file, chat_id=ADMINS[0], content_types=types.ContentTypes.DOCUMENT)
async def add(message: types.Message, state: FSMContext):
    file_id = message.document.file_id

    # Download the file
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)

    # Save the downloaded file to a temporary location
    temp_file_path = 'temp_file.xlsx'
    with open(temp_file_path, 'wb') as f:
        f.write(downloaded_file.getvalue())

    df = pd.read_excel(temp_file_path)

    try:
        # Iterate over the rows
        for index, row in df.iterrows():
            # Extract data from the row
            full_name = row['full_name']
            employee_id = row['employee_id']
            shop_name = row['shop_name']
            phone_number = str(row['phone_number'])
            telegram_id = row['telegram_id']  # Assuming telegram_id is not provided in the Excel file

            # Call the add_vba function asynchronously
            await db.add_vba(full_name, employee_id, shop_name, phone_number, telegram_id)
            await db.add_stock_vba(
                telegram_id=telegram_id,
                shop_name=shop_name,
            )

            await asyncio.sleep(0.1)
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            await message.answer("File removed from server")
            # Finish the state
        await state.finish()
        # Send a confirmation message to the user
        await message.reply("Data has been successfully added to the database.")
    except Exception as e:
        await message.reply(f"Error: {e}")


@dp.message_handler(state=AddVBAList.file, chat_id=ADMINS[0], content_types=types.ContentTypes.ANY)
async def add(message: types.Message):
    await message.answer("Send file")


@dp.message_handler(Command(["remove_imei"]), state='*', chat_id=ADMINS[0])
async def search(message: types.Message):
    await message.answer("Send IMEI")
    await RemoveIMEI.IMEI.set()


@dp.message_handler(state=RemoveIMEI.IMEI, chat_id=ADMINS[0], content_types=types.ContentTypes.TEXT)
async def search(message: types.Message, state: FSMContext):
    IMEI = str(message.text)
    try:
        await db.delete_imei(IMEI=IMEI)
    except Exception as e:
        await message.reply(f"Error: {e}")
    else:
        await message.reply("IMEI successfully removed!")
        await state.finish()


@dp.message_handler(state=RemoveIMEI.IMEI, chat_id=ADMINS[0], content_types=types.ContentTypes.ANY)
async def search(message: types.Message):
    await message.answer("Send IMEI in text")


@dp.message_handler(Command(["update_telegramID"]), state='*', chat_id=ADMINS[0])
async def search(message: types.Message):
    await message.answer("Send Employee ID in text")
    await UpdateTelegramID.employeeID.set()


@dp.message_handler(state=UpdateTelegramID.employeeID, chat_id=ADMINS[0], content_types=types.ContentTypes.TEXT)
async def search(message: types.Message, state: FSMContext):
    employee_id = str(message.text)
    await state.update_data({
        "employeeID": employee_id
    })
    await message.answer("Send new telegram ID")
    await UpdateTelegramID.telegramID.set()


@dp.message_handler(state=UpdateTelegramID.employeeID, chat_id=ADMINS[0], content_types=types.ContentTypes.ANY)
async def search(message: types.Message):
    await message.answer("Send Employee ID in text")


@dp.message_handler(state=UpdateTelegramID.telegramID, chat_id=ADMINS[0], content_types=types.ContentTypes.TEXT)
async def search(message: types.Message, state: FSMContext):
    telegram_id = str(message.text)
    data = await state.get_data()
    employee_id = str(data.get("employeeID"))
    try:
        await db.update_vba_telegram_id(telegram_id=int(telegram_id), employee_id=employee_id)
    except Exception as e:
        await message.reply(f"Error: {e}")
    else:
        await message.reply("Telegram ID successfully updated!")
        await state.finish()


@dp.message_handler(state=UpdateTelegramID.telegramID, chat_id=ADMINS[0], content_types=types.ContentTypes.ANY)
async def search(message: types.Message):
    await message.answer("Send telegram ID in text")




