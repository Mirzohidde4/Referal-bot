from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


telefon = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✔️ Ro'yhatdan o'tish", request_contact=True)]
    ], 
    resize_keyboard=True, one_time_keyboard=True,
)


btn = InlineKeyboardBuilder()
btn.add(InlineKeyboardButton(text="🖇 Havolam", callback_data="my_ssilka"))
btn.add(InlineKeyboardButton(text="💰 Balans", callback_data="my_ballans"))
btn.adjust(2)


qaytish = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="my_back")]
    ]
)