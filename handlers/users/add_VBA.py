import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.Userstates import VBAInfo, IMEISendAllowance
from keyboards.default import UserKeyboard
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS, HR
from aiogram.dispatcher.filters.builtin import Command


@dp.message_handler(Command(["add_VBA"]), chat_id=HR)
async def bot_start(message: types.Message):
    await message.answer(f"Assalamu alaykum, {message.from_user.full_name}! \n\nIltimos, VBA to'liq ismini kiriting!")
    await VBAInfo.fullname.set()


@dp.message_handler(state=VBAInfo.fullname)
async def fullname(message:  types.Message, state: FSMContext):
    full_name = message.text
    if len(full_name) <= 5:
        await message.answer("Iltimos, VBA ism va familiyasini <b>to'liq</b> kiriting!")
    else:
        username = message.from_user.username
        await state.update_data({
            "fullname": full_name,
            "username": username
        })
        await message.answer("Iltimos, Employee ID ni kiriting!")
        await VBAInfo.employee_id.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=VBAInfo.fullname)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning! \n\nPlease, only use letters!")


# @dp.message_handler(state=VBAInfo.region, text="Toshkent", content_types=types.ContentTypes.TEXT)
# @dp.message_handler(state=VBAInfo.region, text="Namangan", content_types=types.ContentTypes.TEXT)
# @dp.message_handler(state=VBAInfo.region, text="Andijon", content_types=types.ContentTypes.TEXT)
# @dp.message_handler(state=VBAInfo.region, text="Farg'ona", content_types=types.ContentTypes.TEXT)
# @dp.message_handler(state=VBAInfo.region, text="Sirdaryo", content_types=types.ContentTypes.TEXT)
# @dp.message_handler(state=VBAInfo.region, text="Navoiy", content_types=types.ContentTypes.TEXT)
# @dp.message_handler(state=VBAInfo.region, text="Samarqand", content_types=types.ContentTypes.TEXT)
# @dp.message_handler(state=VBAInfo.region, text="Surxondaryo", content_types=types.ContentTypes.TEXT)
# @dp.message_handler(state=VBAInfo.region, text="Buxoro", content_types=types.ContentTypes.TEXT)
# @dp.message_handler(state=VBAInfo.region, text="Xorazm", content_types=types.ContentTypes.TEXT)
# @dp.message_handler(state=VBAInfo.region, text="Qoraqolpog'iston", content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=VBAInfo.employee_id, content_types=types.ContentTypes.TEXT)
async def employee(message:  types.Message, state: FSMContext):
    employee_id = message.text
    if len(employee_id) < 9:
        await message.answer("Employee ID ni to'liq kiriting")
    else:
        await state.update_data({"employee_id": employee_id})
        await message.answer("Iltimos, VBA telegram ID kiriting!")
        await VBAInfo.telegram_id.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=VBAInfo.employee_id)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning!")


@dp.message_handler(state=VBAInfo.telegram_id, content_types=types.ContentTypes.TEXT)
async def employee(message:  types.Message, state: FSMContext):
    telegram_id = message.text
    if len(telegram_id) < 5:
        await message.answer("Telegram ID ni to'liq kiriting")
    else:
        await state.update_data({"telegram_id": telegram_id})
        await message.answer("Iltimos, VBA ishlaydigan shop (do'kon) nomini kiriting!")
        await VBAInfo.shopname.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=VBAInfo.telegram_id)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning!")



@dp.message_handler(state=VBAInfo.shopname)
async def shopname(message: types.Message, state: FSMContext):
    shopname = message.text
    if len(shopname) <= 3:
        await message.answer("Iltimos, shop (do'kon) nomini <b>to'liq</b> kiriting!")
    else:
        await state.update_data({"shopname": shopname})

        await message.answer("Iltimos, VBA telefon raqamini kiriting!")
        await VBAInfo.phonenumber.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=VBAInfo.shopname)
async def fullname(message: types.Message):
    await message.answer("Iltimos, faqatgina harflardan foydalaning!")


# @dp.message_handler(content_types=types.ContentType.CONTACT, state=VBAInfo.phonenumber)
# async def phone_number(message: types.Message, state: FSMContext):
#     contact = message.contact.phone_number
#     await state.update_data({'phone_number': contact})
#     await message.answer("Supervisor ismini kiriting!")
#     await VBAInfo.supervisorname.set()


phone_number_regexp = "^[+]998[389][012345789][0-9]{7}$"


@dp.message_handler(regexp=phone_number_regexp, content_types=types.ContentTypes.TEXT, state=VBAInfo.phonenumber)
async def phonen(message: types.Message, state: FSMContext):
    phonenumber = message.text
    await state.update_data({'phone_number': phonenumber})

    data = await state.get_data()
    full_name = data.get("fullname")
    employee_id = data.get("employee_id")
    telegram_id = data.get("telegram_id")
    shop = data.get("shopname")
    phone = data.get("phone_number")

    msg = "Iltimos, shaxsiy ma'lumotingiz to'g'riligini tasdiqlang! \n\n"
    msg += f"To'liq ism - <b>{full_name}</b> \n\n"
    msg += f"Employee ID - <b>{employee_id}</b> \n\n"
    msg += f"Telegram ID - <b>{telegram_id}</b> \n\n"
    msg += f"Shop (do'kon) - <b>{shop}</b> \n\n"
    msg += f"phone - <b>{phone}</b> \n\n"

    await message.answer(msg, reply_markup=UserKeyboard.confirmation)
    await VBAInfo.confirmation.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=VBAInfo.phonenumber)
async def phone(message: types.Message):
    await message.answer("Iltimos, to'g'ri formatdagi raqam kiriting!")


@dp.message_handler(content_types=types.ContentTypes.ANY, state=VBAInfo.phonenumber)
async def phone_number(message: types.Message):
    await message.answer("Iltimos, faqatgina raqamlardan foydalaning!")


@dp.message_handler(text="Tasdiqlash ✅", content_types=types.ContentTypes.TEXT, state=VBAInfo.confirmation)
async def confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = int(data.get("telegram_id"))
    shop_name = data.get("shopname")
    try:
        await db.add_stock_vba(
            telegram_id=telegram_id,
            shop_name=shop_name,
        )
    except Exception as e:
        msg = f"There has been some error in adding VBA telegram id to stock database! \n\n{e}"
        await bot.send_message(chat_id=ADMINS[0], text=msg)
    else:
        msg = f"A new VBA has been added to stock database!"
        await bot.send_message(chat_id=ADMINS[0], text=msg)
    try:
        user = await db.add_vba(
            full_name=data.get("fullname"),
            employee_id=data.get("employee_id"),
            shop_name=shop_name,
            phone_number=data.get("phone_number"),
            telegram_id=telegram_id,
        )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_vba(telegram_id=int(data.get("telegram_id")))
        await message.answer(f"Unique Violation error. Employee ID ({user[2]}) raqam ({user[4]}) yoki telegram id ({user[5]}) database da mavjud! \n\nTahrirlang...", reply_markup=UserKeyboard.confirmation)
    except Exception as e:
        await message.answer(f"Error : {e}. \n\nTry editing (Tahrirlang)", reply_markup=UserKeyboard.confirmation)
    else:
        count = await db.count_vbas()
        msg = f"User '{user[1]}' has been added to the VBA database! We have {count} VBAs."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

        await message.answer("Rahmat, endi VBA botdan foydalanishi mumkin 🙂", reply_markup=ReplyKeyboardRemove(selective=True))
        await state.finish()


@dp.message_handler(text="Tahrirlash ✏️", content_types=types.ContentTypes.TEXT, state=VBAInfo.confirmation)
async def edit(message: types.Message):
    await message.answer("Iltimos, VBA to'liq ismini kiriting!")
    await VBAInfo.fullname.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=VBAInfo.confirmation)
async def confirmation(message: types.Message):
    await message.answer("Iltimos, tugmalardan birini bosing!", reply_markup=UserKeyboard.confirmation)


