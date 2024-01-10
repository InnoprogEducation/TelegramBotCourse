from aiogram.filters import Command
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram import Bot, Dispatcher
from aiogram.types import Message, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup

BOT_TOKEN = "6972762642:AAEQ5k5aI_QfR2UqSYhTUE5zhgZxXPjWv_Y"

bot = Bot(BOT_TOKEN, parse_mode="HTML")
redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)
dp = Dispatcher(storage=storage)


@dp.message(Command("kb"))
async def send_keyboard(message: Message):
    web_app = WebAppInfo(url="https://rafailvv.github.io/innoprog_landing/")
    keyboard = ReplyKeyboardMarkup(
        row_width=1,
        keyboard=[
            [KeyboardButton(text="Веб приложение", web_app=web_app)],
        ])
    await message.answer(
        "Кнопка ниже откроет веб приложение",
        reply_markup=keyboard
    )


@dp.message(Command("ib"))
async def send_keyboard(message: Message):
    web_app = WebAppInfo(url="https://rafailvv.github.io/innoprog_landing/")
    keyboard = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [InlineKeyboardButton(text="Веб приложение", web_app=web_app)],
        ])
    await message.answer(
        "Кнопка ниже откроет веб приложение",
        reply_markup=keyboard
    )


if __name__ == "__main__":
    dp.run_polling(bot)
