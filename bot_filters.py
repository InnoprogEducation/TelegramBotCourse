from aiogram import Bot, Dispatcher
from aiogram.types import Message

BOT_TOKEN = "6972762642:AAEQ5k5aI_QfR2UqSYhTUE5zhgZxXPjWv_Y"

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

ADMINS = [
    1591962902,  # ... Список который хранит админов бота
]


# То фильтр будет выглядеть примерно так
@dp.message(lambda message: message.from_user.id in ADMINS)
async def talk_admin(message: Message):
    await message.answer("Приветсвую администрацию!")
    # На каждое сообщение мы будем приветсвовать админов
