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
from keyboards.inline import imei_confirmation

import os
import easyocr
import re

reader = easyocr.Reader(['en'])

DOWNLOAD_DIRECTORY = '/Users/bez/Desktop/IMEI bot2/utils/photos/'


@dp.message_handler(Command(["add_IMEI"]), state="*")
async def add(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    vba = await db.select_vba(telegram_id=telegram_id)
    if vba:
        await message.answer("IMEI ni rasmga olib jo'nating. \n\n*Iloji boricha yaqindan", reply_markup=types.ReplyKeyboardRemove())
        await AddIMEI.photo.set()
        await state.update_data({
            'telegram_id': telegram_id
        })
    else:
        await message.answer("You have no permission. \n\nSizda IMEI qo'shish uchun ruxsat yo'q.")


@dp.message_handler(state=AddIMEI.photo, content_types=types.ContentTypes.PHOTO)
async def add(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    # Perform OCR on the preprocessed image
    file_path = os.path.join(DOWNLOAD_DIRECTORY, "vivo.jpg")
    await message.photo[-1].download(destination_file=file_path)
    result = reader.readtext(file_path, detail=0, paragraph=True)
    text_str = ' '.join(result)
    match = re.search(r'\d{15}', text_str)
    if match is None:
        await message.answer("Rasmda IMEI ko'rsatilmagan! \n\nQaytadan rasmga oling!")
    else:
        IMEI = match.group(0)
        await state.update_data({
            "IMEI": IMEI,
            "sticker": photo_id
        })
        await message.answer(f"Rasmdagi shu raqammi? -> \n\n<b>IMEI1: {IMEI}</b> \n\n?",
                             reply_markup=imei_confirmation.confirmation_keyboard)
        await AddIMEI.IMEI_confirm.set()


@dp.message_handler(state=AddIMEI.photo, content_types=types.ContentTypes.ANY)
async def add(message: types.Message):
    await message.answer(f"Iltimos, faqatgina rasm jo'nating!")


@dp.callback_query_handler(state=AddIMEI.IMEI_confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
    callback_data = call.data
    if callback_data == "correct":
        await call.message.answer("Modelni tanlang:", reply_markup=imei_confirmation.model_type)
        await AddIMEI.model.set()
    elif callback_data == "incorrect":
        await call.message.answer("IMEI ni kiriting...")
        await AddIMEI.IMEI_manual.set()
    else:
        await call.message.answer("Iltimos, tugmalardan birini bosing!.",
                                  reply_markup=imei_confirmation.confirmation_keyboard)


@dp.message_handler(state=AddIMEI.IMEI_confirm, content_types=types.ContentTypes.ANY)
async def confirm(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!")


@dp.message_handler(state=AddIMEI.IMEI_manual, content_types=types.ContentTypes.TEXT)
async def imei_manual(message:  types.Message, state: FSMContext):
    IMEI = message.text
    if len(IMEI) < 15:
        await message.answer("Iltimos, IMEI ni <b>to'liq</b> kiriting!")
    else:
        await state.update_data({
            "IMEI": IMEI
        })
        await message.answer("Modelni tanlang:", reply_markup=imei_confirmation.model_type)
        await AddIMEI.model.set()


@dp.message_handler(state=AddIMEI.IMEI_manual, content_types=types.ContentTypes.ANY)
async def imei_manual(message:  types.Message):
    await message.answer("Iltimos, IMEI ni <b>text</b> formatida kiriting!")


@dp.callback_query_handler(state=AddIMEI.model)
async def phone_model(call: types.CallbackQuery):
    model = call.data
    if model == "V":
        await call.message.answer("Aniq modelni tanlang:", reply_markup=imei_confirmation.modelV)
        await AddIMEI.specific_model.set()
    elif model == "Y":
        await call.message.answer("Aniq modelni tanlang:", reply_markup=imei_confirmation.modelY)
        await AddIMEI.specific_model.set()
    elif model == "X":
        await call.message.answer("Aniq modelni tanlang:", reply_markup=imei_confirmation.modelX)
        await AddIMEI.specific_model.set()
    else:
        await call.message.answer("Iltimos, tugmalardan birini bosing!",  reply_markup=imei_confirmation.model_type)


@dp.message_handler(content_types=types.ContentTypes.ANY, state=AddIMEI.model)
async def fullname(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!")


@dp.callback_query_handler(state=AddIMEI.specific_model)
async def phone_model_specific(call: types.CallbackQuery, state: FSMContext):
    model_specific = call.data
    await state.update_data({
        "model": model_specific
    })

    data = await state.get_data()
    IMEI = data.get("IMEI")
    model = data.get("model")
    sticker = data.get("sticker")

    msg = "Iltimos, kiritilgan ma'lumot to'g'riligini tasdiqlang: \n\n"
    msg += f"IMEI raqami - <b>{IMEI}</b> \n\n"
    msg += f"Telefon modeli - <b>{model}</b> \n\n"

    await call.message.answer_photo(photo=sticker, caption=msg, reply_markup=imei_confirmation.confirmation_keyboard2)
    await AddIMEI.confirmation.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=AddIMEI.specific_model)
async def fullname(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!")


@dp.callback_query_handler(state=AddIMEI.confirmation, text="Tasdiqlash ✅")
async def phone_model_specific(call: types.CallbackQuery, state: FSMContext):
    today = date.today()
    now_time = datetime.now().time().strftime("%H:%M:%S")

    data = await state.get_data()
    Model = str(data.get("model"))
    Telegram_id = data.get("telegram_id")

    stock_count = await db.select_stock(telegram_id=Telegram_id, model_name=Model)
    model_key = Model.replace(" ", "_").replace("/", "_").lower()
    new_count = int(stock_count[model_key]) - 1
    if int(stock_count[model_key]) == 0:
        new_count = 0

    try:
        imei = await db.add_imei(
            IMEI=data.get("IMEI"),
            Model=Model,
            Sticker=data.get("sticker"),
            Date_month=str(today),
            Time_day=str(now_time),
            Telegram_id=data.get("telegram_id"),
        )
    except asyncpg.exceptions.UniqueViolationError:
        imei = await db.select_imei(IMEI=data.get("IMEI"))
        msg = f"IMEI '{imei[1]}' already exists! Watch out for monkey business! \n\nTelegram ID: {imei[6]}"
        await bot.send_message(chat_id=ADMINS[0], text=msg)
        await call.message.answer(f"Bu IMEI oldin kiritilgan. Qayta kiritish imkonsiz. \n\n@muhammadkodir_mahmudjanov ga aloqaga chiqing.")
        await state.finish()
    except Exception as e:
        await call.message.answer(f"Qandaydir xatolik yuz berdi. \n\nTahrirlash orqali qayta urinib ko'ring!", reply_markup=imei_confirmation.edit_keyboard)
    else:
        count = await db.count_imei()
        msg = f"IMEI '{imei[1]}' has been added to the database! We now have {count} IMEIs"
        await bot.send_message(chat_id=ADMINS[0], text=msg)

        try:
            await db.update_stock_count(
                model_name=Model,
                count=new_count,
                telegram_id=Telegram_id,
            )
        except Exception as e:
            msg = f"There has been some error in updating stock count! \n\n{e}"
            await bot.send_message(chat_id=ADMINS[0], text=msg)
        else:
            msg = f"Stock Count has been successfully decreased!"
            await bot.send_message(chat_id=ADMINS[0], text=msg)

        await call.message.answer("Rahmat, IMEI muvaffaqiyatli saqlandi! 🙂", reply_markup=ReplyKeyboardRemove(selective=True))
        await state.finish()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=AddIMEI.specific_model)
async def fullname(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!")

# @dp.message_handler(state=AddIMEI.IMEI, content_types=types.ContentTypes.TEXT)
# async def imei(message:  types.Message, state: FSMContext):
#     imei = message.text
#     if len(imei) < 15:
#         await message.answer("Iltimos, IMEI raqamini <b>to'liq</b> kiriting!")
#     else:
#         await state.update_data({
#             "imei": imei
#         })
#         await message.answer("Stickerni rasmga olib jo'nating!")
#         await AddIMEI.sticker.set()
#
#
# @dp.message_handler(content_types=types.ContentTypes.ANY, state=AddIMEI.IM)
# async def fullname(message: types.Message):
#     await message.answer("Iltimos, faqatgina harflardan foydalaning!")
#
#
# @dp.message_handler(state=AddIMEI.sticker, content_types=types.ContentTypes.PHOTO)
# async def imei(message:  types.Message, state: FSMContext):
#     sticker = message.photo[-1].file_id
#
#     await state.update_data({
#         "sticker": sticker
#     })
#
#     data = await state.get_data()
#     phonemodel = data.get("phonemodel")
#     imei = data.get("imei")
#     sticker = data.get("sticker")
#
#     msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang!"
#     msg += f"Telefon Modeli - <b>{phonemodel}</b> \n\n"
#     msg += f"IMEI raqami - <b>{imei}</b> \n\n"
#
#     await message.answer_photo(photo=sticker, caption=msg, reply_markup=UserKeyboard.confirmation)
#     await AddIMEI.confirmation.set()
#
#     @dp.message_handler(state=AddIMEI.sticker, content_types=types.ContentTypes.DOCUMENT)
#     async def imei(message: types.Message, state: FSMContext):
#         sticker = message.document.file_id
#
#         await state.update_data({
#             "sticker": sticker
#         })
#
#         data = await state.get_data()
#         phonemodel = data.get("phonemodel")
#         imei = data.get("imei")
#         sticker = data.get("sticker")
#
#         msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang!"
#         msg += f"Telefon Modeli - <b>{phonemodel}</b> \n\n"
#         msg += f"IMEI raqami - <b>{imei}</b> \n\n"
#
#         await message.answer_document(document=sticker, thumb=sticker, caption=msg, reply_markup=UserKeyboard.confirmation)
#         await AddIMEI.confirmation.set()
#
#
# @dp.message_handler(content_types=types.ContentTypes.ANY, state=AddIMEI.sticker)
# async def fullname(message: types.Message):
#     await message.answer("Iltimos, faqatgina rasm jo'nating!")
#
#
# @dp.message_handler(text="Tasdiqlash ✅", content_types=types.ContentTypes.TEXT, state=AddIMEI.confirmation)
# async def confirmation(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#
#     today = date.today()
#
#     now_time = datetime.now().time()
#
#     try:
#         imei = await db.add_imei(
#             model=data.get("phonemodel"),
#             imei=data.get("imei"),
#             sticker=data.get("sticker"),
#             now_date=f"{today}, {now_time}",
#             telegram_id=data.get("telegram_id"),
#         )
#     except asyncpg.exceptions.UniqueViolationError:
#         imei = await db.select_imei(telegram_id=data.get("telegram_id"))
#
#     count = await db.count_imei()
#     msg = f"IMEI '{imei[2]}' has been added to the database! We now have {count} IMEIs"
#     await bot.send_message(chat_id=ADMINS[0], text=msg)
#
#     await message.answer("Rahmat, IMEI muvaffaqiyatli saqlandi! 🙂", reply_markup=ReplyKeyboardRemove(selective=True))
#     await IMEISendAllowance.permission_granted.set()
#
#
# @dp.message_handler(tex t="Tahrirlash ✏️", content_types=types.ContentTypes.TEXT, state=AddIMEI.confirmation)
# async def edit(message: types.Message):
#     await message.answer("Telefon modelini kiriting...")
#     await AddIMEI.phonemodel.set()
#
#
# @dp.message_handler(content_types=types.ContentTypes.ANY, state=AddIMEI.confirmation)
# async def confirmation(message: types.Message):
#     await message.answer("Iltimos, tugmalardan birini bosing!", reply_markup=UserKeyboard.confirmation)
