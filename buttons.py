from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


telefon = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ro'yhatdan o'tish", request_contact=True)]
    ], 
    resize_keyboard=True, one_time_keyboard=True,
)


havola = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🖇 Havolam", callback_data="ssilka")]
    ]
)