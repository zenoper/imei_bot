from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confirmation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Tasdiqlash ✅")
        ],
        [
            KeyboardButton(text="Tahrirlash ✏️")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

region = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Toshkent"),
            KeyboardButton(text="Namangan"),
            KeyboardButton(text="Andijon"),


        ],
        [
            KeyboardButton(text="Farg'ona"),
            KeyboardButton(text="Sirdaryo"),
            KeyboardButton(text="Navoiy"),
        ],
        [
            KeyboardButton(text="Samarqand"),
            KeyboardButton(text="Qashqadaryo"),
            KeyboardButton(text="Surxondaryo"),
        ],
        [
            KeyboardButton(text="Buxoro"),
            KeyboardButton(text="Xorazm"),
            KeyboardButton(text="Qoraqolpog'iston"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="raqam jo'natish 📱", request_contact=True)
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)