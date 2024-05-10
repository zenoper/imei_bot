from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("To'g'ri ✅", callback_data="correct"),
            InlineKeyboardButton("Xato 🚫", callback_data="incorrect"),
        ],
    ],
)

confirmation_keyboard2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Tasdiqlash ✅", callback_data="Tasdiqlash ✅"),
            InlineKeyboardButton("Tahrirlash ✏️", callback_data="Tahrirlash ✏️"),
        ],
    ],
)


edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Tahrirlash 🚫", callback_data="Tahrirlash 🚫"),
        ],
    ],
)


model_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("V", callback_data="V"),
            InlineKeyboardButton("Y", callback_data="Y"),
            InlineKeyboardButton("X", callback_data="X")
        ],
    ]
)


modelX = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("X100", callback_data="X100"),

        ],
    ]
)


modelY = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Y02T", callback_data="Y02T"),
            InlineKeyboardButton("Y03 64GB", callback_data="Y03 64GB"),
            InlineKeyboardButton("Y03 128GB", callback_data="Y03 128GB"),
            InlineKeyboardButton(text="Y15S", callback_data="Y15S"),

        ],
        [
            InlineKeyboardButton(text="Y16", callback_data="Y16"),
            InlineKeyboardButton("Y17s 4/128", callback_data="Y17s 4/128"),
            InlineKeyboardButton("Y17s 6/128", callback_data="Y17s 6/128"),
            InlineKeyboardButton(text="Y22", callback_data="Y22"),

        ],
        [
            InlineKeyboardButton(text="Y27", callback_data="Y27"),
            InlineKeyboardButton("Y27s", callback_data="Y27s"),
            InlineKeyboardButton(text="Y33S 64GB", callback_data="Y33S 64GB"),
            InlineKeyboardButton(text="Y33S 128GB", callback_data="Y33S 128GB"),
        ],
        [
            InlineKeyboardButton(text="Y35", callback_data="Y35"),
            InlineKeyboardButton("Y36", callback_data="Y36"),
            InlineKeyboardButton(text="Y53S 6GB", callback_data="Y53S 6GB"),
            InlineKeyboardButton(text="Y53S 8GB", callback_data="Y53S 8GB"),
            InlineKeyboardButton("Y100", callback_data="Y100"),
        ],
    ],
    row_width=4
)


modelV = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="V30", callback_data="V30"),
            InlineKeyboardButton(text="V29", callback_data="V29"),
            InlineKeyboardButton(text="V29e", callback_data="V29e"),
        ],
        [
            InlineKeyboardButton(text="V27", callback_data="V27"),
            InlineKeyboardButton(text="V27e", callback_data="V27e"),
            InlineKeyboardButton(text="V25", callback_data="V25"),
        ],
        [
            InlineKeyboardButton(text="V25e", callback_data="V25e"),
            InlineKeyboardButton(text="V25pro", callback_data="V25pro"),
            InlineKeyboardButton(text="V23", callback_data="V23"),
            InlineKeyboardButton(text="V23e", callback_data="V23e"),
        ],
    ],
    row_width=4
)