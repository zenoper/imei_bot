import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.Userstates import PersonalInfo
from keyboards.default import UserKeyboard
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS


@dp.message_handler(state=PersonalInfo.fullname)
async def fullname(message:  types.Message, state: FSMContext):
    full_name = message.text
    if len(full_name) <= 5:
        await message.answer("Iltimos, ism va familiyangizni <b>to'liq</b> kiriting!")
    else:
        username = message.from_user.username
        telegram_id = message.from_user.id
        await state.update_data({
            "fullname": full_name,
            "telegram_id": telegram_id,
            "username": username
        })
        await message.answer("Iltimos, viloyatingizni tanglang!", reply_markup=UserKeyboard.region)
        await PersonalInfo.region.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=PersonalInfo.fullname)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning! \n\nPlease, only use letters!")


@dp.message_handler(state=PersonalInfo.region, text="Toshkent", content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=PersonalInfo.region, text="Namangan", content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=PersonalInfo.region, text="Andijon", content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=PersonalInfo.region, text="Farg'ona", content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=PersonalInfo.region, text="Sirdaryo", content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=PersonalInfo.region, text="Navoiy", content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=PersonalInfo.region, text="Samarqand", content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=PersonalInfo.region, text="Surxondaryo", content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=PersonalInfo.region, text="Buxoro", content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=PersonalInfo.region, text="Xorazm", content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=PersonalInfo.region, text="Qoraqolpog'iston", content_types=types.ContentTypes.TEXT)
async def region(message:  types.Message, state: FSMContext):
    region = message.text

    await state.update_data({"region": region})
    await message.answer("Iltimos, siz ishlaydigan shop (do'kon) nomini kiriting!")
    await PersonalInfo.shopname.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=PersonalInfo.region)
async def fullname(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!")


@dp.message_handler(content_types=types.ContentTypes.ANY, state=PersonalInfo.region)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning!")


@dp.message_handler(state=PersonalInfo.shopname)
async def shopname(message: types.Message, state: FSMContext):
    shopname = message.text
    if len(shopname) <= 3:
        await message.answer("Iltimos, shop (do'kon) nomini <b>to'liq</b> kiriting!")
    else:
        await state.update_data({"shopname": shopname})

        data = await state.get_data()
        full_name = data.get("fullname")
        retailer = data.get("retailername")
        shop = data.get("shopname")

        msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang!"
        msg += f"To'liq ism - <b>{full_name}</b> \n\n"
        msg += f"Retailer - <b>{retailer}</b> \n\n"
        msg += f"Shop (do'kon) - <b>{shop}</b> \n\n"

        await message.answer("Iltimos, telefon raqamingizni kiriting!", reply_markup=UserKeyboard.phone_number)
        await PersonalInfo.phonenumber.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=PersonalInfo.shopname)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning!")


@dp.message_handler(content_types=types.ContentType.CONTACT, state=PersonalInfo.phonenumber)
async def phone_number(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    await state.update_data({'phone_number': contact})
    await message.answer("Supervisor ismini kiriting!")
    await PersonalInfo.supervisorname.set()


phone_number_regexp = "^[+]998[389][012345789][0-9]{7}$"


@dp.message_handler(regexp=phone_number_regexp, content_types=types.ContentTypes.TEXT, state=PersonalInfo.phonenumber)
async def phonen(message: types.Message, state: FSMContext):
    phonenumber = message.text
    await state.update_data({'phone_number': phonenumber})
    await message.answer("Supervisor ismini kiriting!")
    await PersonalInfo.supervisorname.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=PersonalInfo.phonenumber)
async def phone(message: types.Message):
    await message.answer("Iltimos, to'g'ri formatdagi raqam kiriting!", reply_markup=UserKeyboard.phone_number)


@dp.message_handler(content_types=types.ContentTypes.ANY, state=PersonalInfo.phonenumber)
async def phone_number(message: types.Message):
    await message.answer("Iltimos, faqatgina raqamlardan foydalaning!")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=PersonalInfo.supervisorname)
async def supervisor(message: types.Message, state: FSMContext):
    supervisor = message.text
    await state.update_data({'supervisor': supervisor})

    data = await state.get_data()
    full_name = data.get("fullname")
    region = data.get("region")
    shop = data.get("shopname")
    phone = data.get("phone_number")
    supervisorname = data.get("supervisor")

    msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang!"
    msg += f"To'liq ism - <b>{full_name}</b> \n\n"
    msg += f"Viloyat - <b>{region}</b> \n\n"
    msg += f"Shop (do'kon) - <b>{shop}</b> \n\n"
    msg += f"phone - <b>{phone}</b> \n\n"
    msg += f"Supervisor - <b>{supervisorname}</b> \n\n"

    await message.answer(msg, reply_markup=UserKeyboard.confirmation)
    await PersonalInfo.confirmation.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=PersonalInfo.supervisorname)
async def phone_number(message: types.Message):
    await message.answer("Iltimos, faqatgina raqamlardan foydalaning!")


@dp.message_handler(text="Tasdiqlash ✅", content_types=types.ContentTypes.TEXT, state=PersonalInfo.confirmation)
async def confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()

    try:
        user = await db.add_user(
            full_name=data.get("fullname"),
            region=data.get("region"),
            shop_name=data.get("shopname"),
            phone_number=data.get("phone_number"),
            supervisor=data.get("supervisor"),
            username=data.get("username"),
            telegram_id=data.get("telegram_id"),
        )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=data.get("telegram_id"))

    count = await db.count_users()
    msg = f"User '{user[1]}' has been added to the database! We now have {count} users."
    await bot.send_message(chat_id=ADMINS[0], text=msg)

    await message.answer("Rahmat, endi botdan foydalanishingiz mumkin 🙂", reply_markup=ReplyKeyboardRemove(selective=True))
    await state.finish()


@dp.message_handler(text="Tahrirlash ✏️", content_types=types.ContentTypes.TEXT, state=PersonalInfo.confirmation)
async def edit(message: types.Message):
    await message.answer("Iltimos, to'liq ismingizni kiriting!")
    await PersonalInfo.fullname.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=PersonalInfo.confirmation)
async def confirmation(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!", reply_markup=UserKeyboard.confirmation)


