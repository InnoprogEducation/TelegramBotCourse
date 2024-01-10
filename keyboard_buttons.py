from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

BOT_TOKEN = "6972762642:AAEQ5k5aI_QfR2UqSYhTUE5zhgZxXPjWv_Y"

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()


@dp.message(lambda message: message.text == "Клавиатура")
async def send_kb(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Кнопка 1")],
            [KeyboardButton(text="Кнопка 2"), KeyboardButton(text="Кнопка 3")],
        ]
    )

    await message.answer("Сообщение с Reply клавиатурой", reply_markup=kb)


@dp.message(lambda message: "Кнопка" in message.text)
async def check_kb(message: Message):
    await message.answer("Вы нажали на <i>" + message.text + "</i>")


if __name__ == "__main__":
    dp.run_polling(bot)
