import asyncio, logging
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import (Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup)
from aiogram.filters import CommandStart, Command, and_f
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from config import TOKEN
from states import phone
from dt_baza import Add_db, Read_db
from buttons import havola, telefon


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def smd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    if any(user[0] == user_id for user in Read_db()):
        await message.reply(
            text=f'{html.bold('Xush kelibsiz, siz allaqachon ro\'yxatdan o\'tgansiz!\nBotdan foydalanishingiz mumkin.')}',
            reply_markup=havola
            )
        await state.set_state(phone.havola)
    
    else:
        args = message.text.split()[1:]
        if args:
            referal_user_id = int(args[0])
            new_user_id = message.from_user.id
            referal_user = await bot.get_chat(referal_user_id)
            referal_username = referal_user.username
            referal_fullname = referal_user.full_name

            if referal_username:
                await message.reply(
                    text=f'{html.bold(f'Xush kelibsiz! Sizni @{referal_username} taklif qildi.\nBotdan foydalanish uchun ro\'yhatdan o\'tish tugmasini bosing')}.',
                    reply_markup=telefon
                    )
            else:
                await message.reply(
                    text=f'{html.bold(f'Xush kelibsiz! Sizni {html.underline(referal_fullname)} taklif qildi.\nBotdan foydalanish uchun ro\'yhatdan o\'tish tugmasini bosing.')}',
                    reply_markup=telefon    
                    )
        
        else: 
            await message.reply(
                text=f'{html.bold("Assalomu Alaykum xush kelibsiz.\nBotdan foydalanish uchun ro'yhatdan o'tish tugmasini bosing.")}',
                reply_markup=telefon
            )
        await state.set_state(phone.telefon)


@dp.message(F.contact, phone.telefon)
async def telephon(message: Message, state: FSMContext):
    await message.delete()

    user_id = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username
    tel = message.contact.phone_number

    try:
        Add_db(user_id=user_id, fullname=fullname, username=username, phone=tel)
        await message.answer(
            text="Botdan foydalanishingiz mumkin",
            reply_markup=havola
            )
        await state.set_state(phone.havola)

    except Exception as ex:
        print(f"User saqlashda xatolik: {ex}")


@dp.callback_query(F.data == "ssilka", phone.havola)
async def havolam(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    bot_username = (await bot.get_me()).username
    link = f"https://t.me/{bot_username}?start={user_id}"
    await call.message.reply(f"Bu sizning havolangiz: {link}")








@dp.message(F.text)
async def echo(message: Message):
    await message.reply(text="Botni qayta ishga tushirish uchun /start ni bosing.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot o`chdi")
