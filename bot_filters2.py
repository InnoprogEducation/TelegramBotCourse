from aiogram import Bot, Dispatcher
from aiogram.types import Message

BOT_TOKEN = "6972762642:AAEQ5k5aI_QfR2UqSYhTUE5zhgZxXPjWv_Y"

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

from aiogram.enums import ContentType


@dp.message(
    lambda message: message.content_type
    in {ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT}
)
async def ans_file(message: Message):
    await message.answer("Вы отправили сообщение с вложением!")
