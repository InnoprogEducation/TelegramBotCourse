from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.types import FSInputFile

from aiohttp import BasicAuth
from aiogram.client.session.aiohttp import AiohttpSession

session = AiohttpSession(proxy='http://proxy.server:3128')

BOT_TOKEN = "6972762642:AAEQ5k5aI_QfR2UqSYhTUE5zhgZxXPjWv_Y"

bot = Bot(BOT_TOKEN, parse_mode="HTML", session=session)
dp = Dispatcher()


@dp.message()
async def send_echo(message: Message):
    await message.answer(
        text=message.text
    )


if __name__ == "__main__":
    dp.run_polling(bot)
