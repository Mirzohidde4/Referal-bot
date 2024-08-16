import asyncio, logging
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import (Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup)
from aiogram.filters import CommandStart, Command, and_f
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from config import TOKEN
from states import phone
from dt_baza import Add_db, Read_db, Add_Ref, Read_Ref
from buttons import btn, telefon, qaytish


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def smd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    bot_username = (await bot.get_me()).username
    
    if any(user[0] == user_id for user in Read_db()):
        await message.reply(
            text=f'{html.bold('☺️ Xush kelibsiz, siz allaqachon ro\'yxatdan o\'tgansiz!\nBotdan foydalanishingiz mumkin.')}\n\n@{bot_username}',
            reply_markup=btn.as_markup()
            )
    
    else:
        referal = message.text.split()[1:]
        if referal:
            referal_user_id = int(referal[0])
            new_user_id = message.from_user.id
            referal_user = await bot.get_chat(referal_user_id)
            referal_username = referal_user.username
            referal_fullname = referal_user.full_name

            await state.update_data(
                {
                    "referal_user_id": referal_user_id,
                    "new_user_id": new_user_id
                }
            )

            if referal_username:
                await message.reply(
                    text=f'{html.bold(f'☺️ Xush kelibsiz! Sizni @{referal_username} taklif qildi.\nBotdan foydalanish uchun ro\'yhatdan o\'tish tugmasini bosing.')}\n\n@{bot_username}',
                    reply_markup=telefon
                    )
            else:
                await message.reply(
                    text=f'{html.bold(f'☺️ Xush kelibsiz! Sizni {html.underline(referal_fullname)} taklif qildi.\nBotdan foydalanish uchun ro\'yhatdan o\'tish tugmasini bosing.')}\n\n@{bot_username}',
                    reply_markup=telefon    
                    )
        
        else: 
            await message.reply(
                text=f'{html.bold("☺️ Assalomu Alaykum xush kelibsiz.\nBotdan foydalanish uchun ro'yhatdan o'tish tugmasini bosing.")}\n\n@{bot_username}',
                reply_markup=telefon
            )
        await state.set_state(phone.telefon)


@dp.message(F.contact, phone.telefon)
async def telephon(message: Message, state: FSMContext):
    await message.delete()
    bot_username = (await bot.get_me()).username

    user_id = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username
    tel = message.contact.phone_number

    for user in Read_db():
        if (user[0] == user_id) and (user[1] == fullname or user[2] == username):
            await message.answer(text=f'{html.bold("Siz oldin ro'yhatdan o'tgansiz!")}')
            return
    else:    
        try:
            Add_db(user_id=user_id, fullname=fullname, username=username, phone=tel)

            data = await state.get_data()
            referal_user_id = data.get('referal_user_id')
            new_user_id = data.get('new_user_id')

            if user_id == new_user_id:
                Add_Ref(ref_user_id=referal_user_id, new_user_id=new_user_id)

                await bot.send_message(
                    chat_id=referal_user_id,
                    text=f'Siz botga @{username} ni taklif qildingiz!'
                )
            

            await message.answer(
                text=f'{html.bold("✅ Siz ro'yhatdan muvaffaqiyatli o'tdingiz.\nBotdan foydalanishingiz mumkin.")}\n\n@{bot_username}',
                reply_markup=btn.as_markup()
                )

        except Exception as ex:
            print(f"User saqlashda xatolik: {ex}")

    
@dp.callback_query(F.data.startswith("my_"))
async def havolam(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    action = call.data.split("_")[1]
    bot_username = (await bot.get_me()).username

    if action == "ssilka":
        user_id = call.message.chat.id
        link = f"https://t.me/{bot_username}?start={user_id}"
        
        await call.message.answer(
            text=f'{html.bold(f'''
✅ Balans yig'ish uchun havolangizni do'stlaringizga ulashing
❗️1 ta taklif qilingan do'stingiz uchun 1000 so'm (🇺🇿) balans oling !
👇Bu sizning havolangiz: 
{link}
        ''')}',
        reply_markup=qaytish
            )

    elif action == "ballans":
        await call.message.answer(
            text=f'<b>Sizning balansizngiz</b>:\n\n\n@{bot_username}',
            reply_markup=qaytish
        )

    elif action == "back":
        await call.message.answer(
            text=f'💥{html.bold("Botga do\'stlaringizni taklif qiling va pul ishlang!")}\n\n@{bot_username}',
            reply_markup=btn.as_markup()
    )   


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
