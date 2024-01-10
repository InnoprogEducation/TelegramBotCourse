from requests import get

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import json

BOT_TOKEN = "6972762642:AAEQ5k5aI_QfR2UqSYhTUE5zhgZxXPjWv_Y"

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()


@dp.message(lambda msg: msg.text == "Напиши цитату дня")
@dp.message(Command(commands=["quote_of_the_day"]))
async def send_qod(message: Message):
    message_loading = await message.answer("Цитата загружается...")
    response = json.loads(get("https://favqs.com/api/qotd").text)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_loading.message_id,
        text=response["quote"]["body"],
    )


if __name__ == "__main__":
    dp.run_polling(bot)
