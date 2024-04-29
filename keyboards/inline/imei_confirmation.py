from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="To'g'ri ✅", callback_data="correct"),
            InlineKeyboardButton(text="Xato 🚫", callback_data="incorrect")
        ],
    ]
)


model_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="V", callback_data="V"),
            InlineKeyboardButton(text="Y", callback_data="Y"),
            InlineKeyboardButton(text="X", callback_data="X")
        ],
    ]
)


modelX = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="X100, 16+512", callback_data="X100"),

        ],
    ]
)


modelY = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Y17s", callback_data="Y53"),
            InlineKeyboardButton(text="Y100", callback_data="Y53"),
            InlineKeyboardButton(text="Y03", callback_data="Y53"),
            InlineKeyboardButton(text="Y27s", callback_data="Y53"),
            InlineKeyboardButton(text="Y02T", callback_data="Y53"),
            InlineKeyboardButton(text="Y36", callback_data="Y53"),
        ],
        [
            InlineKeyboardButton(text="Y53S", callback_data="Y53"),
            InlineKeyboardButton(text="Y35", callback_data="Y53"),
            InlineKeyboardButton(text="Y33S", callback_data="Y53"),
            InlineKeyboardButton(text="Y12S", callback_data="Y53"),
            InlineKeyboardButton(text="Y1S", callback_data="Y53"),
            InlineKeyboardButton(text="Y31", callback_data="Y53"),
        ],
        [
            InlineKeyboardButton(text="Y27", callback_data="Y53"),
            InlineKeyboardButton(text="Y22", callback_data="Y53"),
            InlineKeyboardButton(text="Y21", callback_data="Y53"),
            InlineKeyboardButton(text="Y16", callback_data="Y53"),
            InlineKeyboardButton(text="Y15S", callback_data="Y53"),
        ],
    ]
)



modelV = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="V30", callback_data="Y53"),
            InlineKeyboardButton(text="V29", callback_data="Y53"),
            InlineKeyboardButton(text="V29e", callback_data="Y53"),
            InlineKeyboardButton(text="V27", callback_data="Y53"),
        ],
        [
            InlineKeyboardButton(text="V21E", callback_data="Y53"),
            InlineKeyboardButton(text="V21", callback_data="Y53"),
            InlineKeyboardButton(text="V23E", callback_data="Y53"),
            InlineKeyboardButton(text="V23", callback_data="Y53"),
        ],
        [
            InlineKeyboardButton(text="V25e", callback_data="Y53"),
            InlineKeyboardButton(text="V25", callback_data="Y53"),
            InlineKeyboardButton(text="V25pro", callback_data="Y53"),
            InlineKeyboardButton(text="V27e", callback_data="Y53"),
        ],
    ]
)