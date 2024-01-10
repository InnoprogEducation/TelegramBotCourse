from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "6972762642:AAEQ5k5aI_QfR2UqSYhTUE5zhgZxXPjWv_Y"

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()


@dp.message(lambda message: message.text == "Inline Клавиатура")
async def send_inline_kb(message: Message):
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Кнопка 1", callback_data="button1")],
            [
                InlineKeyboardButton(text="Кнопка 2", callback_data="button2"),
                InlineKeyboardButton(text="Кнопка 3", callback_data="button3"),
            ],
        ]
    )

    await message.answer("Сообщение с Inline клавиатурой", reply_markup=inline_kb)


@dp.callback_query(lambda q: "button" in q.data)
async def check_query(query: CallbackQuery):
    await query.message.answer(query.data)


if __name__ == "__main__":
    dp.run_polling(bot)
