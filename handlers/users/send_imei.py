from aiogram.dispatcher.filters.builtin import Command
import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import db, bot, dp
from states.Userstates import PersonalInfo, SendIMEI, Add
from keyboards.default import UserKeyboard
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS
from datetime import datetime, date


@dp.message_handler(Command(["add_imei"]), state=Add.add)
async def add(message: types.Message):
    await message.answer("Telefon modelini kiriting...\n\n(Model nomi, RAM, ROM)", reply_markup=types.ReplyKeyboardRemove())
    await SendIMEI.phonemodel.set()


@dp.message_handler(state=SendIMEI.phonemodel, content_types=types.ContentTypes.TEXT)
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
        await SendIMEI.IMEI.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=SendIMEI.phonemodel)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning!")


@dp.message_handler(state=SendIMEI.IMEI, content_types=types.ContentTypes.TEXT)
async def imei(message:  types.Message, state: FSMContext):
    imei = message.text
    if len(imei) < 15:
        await message.answer("Iltimos, IMEI raqamini <b>to'liq</b> kiriting!")
    else:
        await state.update_data({
            "imei": imei
        })
        await message.answer("Stickerni rasmga olib jo'nating!")
        await SendIMEI.sticker.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=SendIMEI.IMEI)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning!")


@dp.message_handler(state=SendIMEI.sticker, content_types=types.ContentTypes.PHOTO)
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
    await SendIMEI.confirmation.set()

    @dp.message_handler(state=SendIMEI.sticker, content_types=types.ContentTypes.DOCUMENT)
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
        await SendIMEI.confirmation.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=SendIMEI.sticker)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina rasm jo'nating!")


@dp.message_handler(text="Tasdiqlash ✅", content_types=types.ContentTypes.TEXT, state=SendIMEI.confirmation)
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
    await Add.add.set()


@dp.message_handler(text="Tahrirlash ✏️", content_types=types.ContentTypes.TEXT, state=SendIMEI.confirmation)
async def edit(message: types.Message):
    await message.answer("Telefon modelini kiriting...")
    await SendIMEI.phonemodel.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=SendIMEI.confirmation)
async def confirmation(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!", reply_markup=UserKeyboard.confirmation)
