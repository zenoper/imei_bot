from aiogram.dispatcher.filters.builtin import Command
import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import db, bot, dp
from states.Userstates import AddIMEI, IMEISendAllowance
from keyboards.default import UserKeyboard
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS
from datetime import datetime, date

import os
import easyocr
import re

reader = easyocr.Reader(['en'])

DOWNLOAD_DIRECTORY = '/Users/bez/Desktop/IMEI bot2/utils/photos/'


@dp.message_handler(Command(["add_IMEI"]))
async def add(message: types.Message):
    telegram_id = message.from_user.id
    vba = await db.select_vba(telegram_id=telegram_id)
    if vba:
        await message.answer("IMEI ni rasmga olib jo'nating. \n\n*Iloji boricha yaqindan", reply_markup=types.ReplyKeyboardRemove())
        await AddIMEI.photo.set()
    else:
        await message.answer("You have no permission. \n\nSizda IMEI qo'shish uchun ruxsat yo'q.")


@dp.message_handler(state=AddIMEI.photo, content_types=types.ContentTypes.PHOTO)
async def add(message: types.Message):
    # Perform OCR on the preprocessed image
    file_path = os.path.join(DOWNLOAD_DIRECTORY, "vivo.jpg")
    await message.photo[-1].download(destination_file=file_path)
    result = reader.readtext(file_path, detail=0, paragraph=True)
    text_str = ' '.join(result)
    print(text_str)
    match = re.search(r'\d{15}', text_str)
    IMEI = match.group(0)
    await message.answer(f"Rasmdagi IMEI1 shu raqammi? -> \n\n<b>{IMEI}</b> \n\n?")


@dp.message_handler(state=AddIMEI.phonemodel, content_types=types.ContentTypes.TEXT)
async def phonemodel(message:  types.Message, state: FSMContext):
    phonemodel = message.text
    if len(phonemodel) <= 3:
        await message.answer("Iltimos, telefon modelini <b>to'liq</b> kiriting!")
    else:
        telegram_id = message.from_user.id
        await state.update_data({
            "phonemodel": phonemodel,
            "telegram_id": telegram_id,
        })
        await message.answer("IMEI raqamini kiriting")
        await AddIMEI.IMEI.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=AddIMEI.phonemodel)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning!")


@dp.message_handler(state=AddIMEI.IMEI, content_types=types.ContentTypes.TEXT)
async def imei(message:  types.Message, state: FSMContext):
    imei = message.text
    if len(imei) < 15:
        await message.answer("Iltimos, IMEI raqamini <b>to'liq</b> kiriting!")
    else:
        await state.update_data({
            "imei": imei
        })
        await message.answer("Stickerni rasmga olib jo'nating!")
        await AddIMEI.sticker.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=AddIMEI.IMEI)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning!")


@dp.message_handler(state=AddIMEI.sticker, content_types=types.ContentTypes.PHOTO)
async def imei(message:  types.Message, state: FSMContext):
    sticker = message.photo[-1].file_id

    await state.update_data({
        "sticker": sticker
    })

    data = await state.get_data()
    phonemodel = data.get("phonemodel")
    imei = data.get("imei")
    sticker = data.get("sticker")

    msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang!"
    msg += f"Telefon Modeli - <b>{phonemodel}</b> \n\n"
    msg += f"IMEI raqami - <b>{imei}</b> \n\n"

    await message.answer_photo(photo=sticker, caption=msg, reply_markup=UserKeyboard.confirmation)
    await AddIMEI.confirmation.set()

    @dp.message_handler(state=AddIMEI.sticker, content_types=types.ContentTypes.DOCUMENT)
    async def imei(message: types.Message, state: FSMContext):
        sticker = message.document.file_id

        await state.update_data({
            "sticker": sticker
        })

        data = await state.get_data()
        phonemodel = data.get("phonemodel")
        imei = data.get("imei")
        sticker = data.get("sticker")

        msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang!"
        msg += f"Telefon Modeli - <b>{phonemodel}</b> \n\n"
        msg += f"IMEI raqami - <b>{imei}</b> \n\n"

        await message.answer_document(document=sticker, thumb=sticker, caption=msg, reply_markup=UserKeyboard.confirmation)
        await AddIMEI.confirmation.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=AddIMEI.sticker)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina rasm jo'nating!")


@dp.message_handler(text="Tasdiqlash ✅", content_types=types.ContentTypes.TEXT, state=AddIMEI.confirmation)
async def confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()

    today = date.today()

    now_time = datetime.now().time()

    try:
        imei = await db.add_imei(
            model=data.get("phonemodel"),
            imei=data.get("imei"),
            sticker=data.get("sticker"),
            now_date=f"{today}, {now_time}",
            telegram_id=data.get("telegram_id"),
        )
    except asyncpg.exceptions.UniqueViolationError:
        imei = await db.select_imei(telegram_id=data.get("telegram_id"))

    count = await db.count_imei()
    msg = f"IMEI '{imei[2]}' has been added to the database! We now have {count} IMEIs"
    await bot.send_message(chat_id=ADMINS[0], text=msg)

    await message.answer("Rahmat, IMEI muvaffaqiyatli saqlandi! 🙂", reply_markup=ReplyKeyboardRemove(selective=True))
    await IMEISendAllowance.permission_granted.set()


@dp.message_handler(text="Tahrirlash ✏️", content_types=types.ContentTypes.TEXT, state=AddIMEI.confirmation)
async def edit(message: types.Message):
    await message.answer("Telefon modelini kiriting...")
    await AddIMEI.phonemodel.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=AddIMEI.confirmation)
async def confirmation(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!", reply_markup=UserKeyboard.confirmation)
