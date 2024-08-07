import asyncio, logging
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from aiogram.filters import CommandStart, Command, and_f
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from config import TOKEN
from states import phone


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def smd_start(message: Message, state: FSMContext):
    await message.reply(
        text=f"{html.bold("Assalomu Alaykum xush kelibsiz.\nbotdan foydalanish uchun telefon raqamingizni yuboring.")}",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Telefon raqam yuborish", request_contact=True)]
            ], 
            resize_keyboard=True, one_time_keyboard=True,
            input_field_placeholder="telefon raqamingizni yuboring"
        )
    )
    await state.set_state(phone.telefon)


@dp.message(F.contact, phone.telefon)
async def telefon(message: Message):
    tel = message.contact.phone_number
    # phone = message.text
    print(type(tel))
    await message.answer(text="Botdan foydalanishingiz mumkin")


@dp.message(phone.telefon)
async def telephone(message: Message):
    phone = message.text
    print(phone)
    if phone.startswith("+998"):
        await message.answer(text="Botdan foydalanishingiz mumkin")
    else:
        await message.answer(text="xato")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot o`chdi")
